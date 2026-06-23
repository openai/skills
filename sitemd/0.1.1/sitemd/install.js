#!/usr/bin/env node
/**
 * sitemd install — downloads the platform binary from GitHub Releases.
 *
 * Cross-platform Node bootstrap. Used as the npm postinstall hook and as a
 * manual recovery command when --ignore-scripts was used. The shell script
 * `install` next to this file does the same job for environments without Node.
 *
 * Idempotent: re-running with a matching binary version is a no-op.
 *
 * Source of truth for the wanted version is the sibling `../package.json`.
 * That works in both contexts where this script ships:
 *   - npm package: ../package.json is the published @sitemd-cc/sitemd version
 *   - sitemd init project: ../package.json is the version copied at init time
 */

const fs = require('fs')
const path = require('path')
const os = require('os')
const https = require('https')
const { execFileSync } = require('child_process')

const GITHUB_RELEASE_URL = 'https://github.com/sitemd-cc/sitemd/releases/download'

const FORCE = process.argv.includes('--force')

function detectPlatform() {
  const platform = process.platform === 'darwin' ? 'darwin'
    : process.platform === 'linux' ? 'linux'
    : process.platform === 'win32' ? 'win' : null
  if (!platform) throw new Error(`Unsupported platform: ${process.platform}`)
  const arch = process.arch === 'arm64' ? 'arm64' : 'x64'
  const ext = platform === 'win' ? '.zip' : '.tar.gz'
  const binaryName = platform === 'win' ? 'sitemd.exe' : 'sitemd'
  return { platform, arch, ext, binaryName }
}

function readWantedVersion() {
  const pkgPath = path.join(__dirname, '..', 'package.json')
  if (!fs.existsSync(pkgPath)) return null
  try {
    const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'))
    return pkg.version || null
  } catch {
    return null
  }
}

function readExistingVersion(binaryPath) {
  if (!fs.existsSync(binaryPath)) return null
  try {
    const out = execFileSync(binaryPath, ['--version'], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] })
    const match = out.match(/(\d+\.\d+\.\d+)/)
    return match ? match[1] : null
  } catch {
    return null
  }
}

function download(url, dest) {
  return new Promise((resolve, reject) => {
    const follow = (u) => {
      https.get(u, { headers: { 'User-Agent': 'sitemd-install' } }, res => {
        if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
          return follow(res.headers.location)
        }
        if (res.statusCode !== 200) {
          return reject(new Error(`Download failed: HTTP ${res.statusCode} ${u}`))
        }
        const file = fs.createWriteStream(dest)
        res.pipe(file)
        file.on('finish', () => { file.close(); resolve() })
        file.on('error', reject)
      }).on('error', reject)
    }
    follow(url)
  })
}

async function main() {
  const { platform, arch, ext, binaryName } = detectPlatform()
  const binaryPath = path.join(__dirname, binaryName)
  const wanted = readWantedVersion()

  if (!wanted) {
    console.error(`  sitemd install: could not read version from ../package.json`)
    console.error(`  Try the shell installer instead: ./sitemd/install`)
    return
  }

  // Idempotency: skip if existing binary matches wanted version
  if (!FORCE) {
    const existing = readExistingVersion(binaryPath)
    if (existing && existing === wanted) {
      // Silent no-op — common case for re-runs
      return
    }
    if (existing && existing !== wanted) {
      console.log(`  sitemd: upgrading ${existing} → ${wanted}`)
    }
  }

  const archive = `sitemd-${wanted}-${platform}-${arch}${ext}`
  const url = `${GITHUB_RELEASE_URL}/v${wanted}/${archive}`
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'sitemd-install-'))
  const archivePath = path.join(tmpDir, archive)
  const extractDir = path.join(tmpDir, 'extracted')

  try {
    console.log(`  sitemd: downloading v${wanted} (${platform}-${arch})...`)
    await download(url, archivePath)

    fs.mkdirSync(extractDir, { recursive: true })
    if (ext === '.zip') {
      // Windows 10 1803+ ships tar.exe which handles zip files
      execFileSync('tar', ['-xf', archivePath, '-C', extractDir], { stdio: 'ignore' })
    } else {
      execFileSync('tar', ['-xzf', archivePath, '-C', extractDir], { stdio: 'ignore' })
    }

    // Find the binary inside the extracted archive (under sitemd/)
    let sourceRoot = extractDir
    if (fs.existsSync(path.join(extractDir, 'sitemd'))) {
      sourceRoot = path.join(extractDir, 'sitemd')
    } else {
      const entries = fs.readdirSync(extractDir)
      if (entries.length === 1 && fs.statSync(path.join(extractDir, entries[0])).isDirectory()) {
        sourceRoot = path.join(extractDir, entries[0])
        if (fs.existsSync(path.join(sourceRoot, 'sitemd'))) {
          sourceRoot = path.join(sourceRoot, 'sitemd')
        }
      }
    }
    const extractedBinary = path.join(sourceRoot, binaryName)
    if (!fs.existsSync(extractedBinary)) {
      throw new Error(`Binary not found in archive: ${binaryName}`)
    }

    fs.rmSync(binaryPath, { force: true })
    fs.copyFileSync(extractedBinary, binaryPath)
    if (platform !== 'win') fs.chmodSync(binaryPath, 0o755)

    console.log(`  sitemd v${wanted} installed`)
  } catch (err) {
    console.error(`  sitemd install failed: ${err.message}`)
    console.error(`  To retry: node sitemd/install.js   (or ./sitemd/install on Unix)`)
  } finally {
    try { fs.rmSync(tmpDir, { recursive: true, force: true }) } catch {}
  }
}

main().catch(err => {
  console.error(`  sitemd install failed: ${err.message}`)
  console.error(`  To retry: node sitemd/install.js   (or ./sitemd/install on Unix)`)
  // Always exit 0 — npm install must not fail because of binary download trouble
  process.exit(0)
})
