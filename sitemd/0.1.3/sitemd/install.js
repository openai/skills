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
  // On-disk name is sitemd-bin so it doesn't collide with the sitemd/sitemd
  // JS wrapper (which npm's bin shim points at). The release archive still
  // contains the native binary as `sitemd` / `sitemd.exe` — we rename on
  // extraction to sitemd-bin / sitemd-bin.exe.
  const binaryName = platform === 'win' ? 'sitemd-bin.exe' : 'sitemd-bin'
  const archiveBinaryName = platform === 'win' ? 'sitemd.exe' : 'sitemd'
  return { platform, arch, ext, binaryName, archiveBinaryName }
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

// ---------------------------------------------------------------------------
// End-of-install next-steps message (dep-install flow)
// ---------------------------------------------------------------------------

function printNextSteps(projectRoot) {
  const hasScaffold = fs.existsSync(path.join(projectRoot, 'sitemd', 'sitemd'))
  console.log()
  console.log(`  sitemd ready${hasScaffold ? ' at ./sitemd/' : ''}`)
  console.log()
  console.log(`  Launch the dev server:`)
  console.log(`    Restart your agent session so it picks up the sitemd MCP server,`)
  console.log(`    then ask: "launch sitemd" — your agent runs the /launch skill.`)
  console.log()
  if (hasScaffold) {
    console.log(`    Or from shell:`)
    console.log(`      cd sitemd && npm install && ./sitemd/sitemd launch`)
    console.log()
  }
  console.log(`  Docs: https://sitemd.cc/docs`)
  console.log()
}

// ---------------------------------------------------------------------------
// Agent file setup — delegates to the shared non-destructive writer.
// ---------------------------------------------------------------------------

async function setupAgentFiles(sitemdDir, projectRoot) {
  const agentRes = path.join(sitemdDir, 'agent-resources')
  if (!fs.existsSync(agentRes)) return

  // Binary command in .mcp.json:
  //   1. Prefer `./sitemd/sitemd` — the Phase-4 scaffolded wrapper at
  //      <projectRoot>/sitemd/sitemd. Stable, self-contained.
  //   2. Fall back to `./node_modules/.bin/sitemd` — npm's bin shim, which
  //      always exists after install and survives hoisting.
  //   3. Final fallback: relative path from projectRoot into the package.
  const scaffoldedWrapper = path.join(projectRoot, 'sitemd', 'sitemd')
  const binShim = path.join(projectRoot, 'node_modules', '.bin', 'sitemd')
  const binaryRel = fs.existsSync(scaffoldedWrapper)
    ? './sitemd/sitemd'
    : fs.existsSync(binShim)
      ? './node_modules/.bin/sitemd'
      : './' + path.relative(projectRoot, path.join(sitemdDir, 'sitemd')).split(path.sep).join('/')

  const { copyAgentFiles } = require('./engine/cli/agent-files')
  await copyAgentFiles(sitemdDir, projectRoot, { binaryRel })
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  const { platform, arch, ext, binaryName, archiveBinaryName } = detectPlatform()
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
    const extractedBinary = path.join(sourceRoot, archiveBinaryName)
    if (!fs.existsSync(extractedBinary)) {
      throw new Error(`Binary not found in archive: ${archiveBinaryName}`)
    }

    fs.rmSync(binaryPath, { force: true })
    fs.copyFileSync(extractedBinary, binaryPath)
    if (platform !== 'win') fs.chmodSync(binaryPath, 0o755)

    console.log(`  sitemd v${wanted} installed`)

    // Propagate agent files to the project root (where npm install was invoked).
    // Three flows:
    //   - npx one-shot: __dirname is in the ephemeral npx cache (path contains
    //     `_npx`). `init` writes agent files itself with the correct scaffold
    //     path; this postinstall pre-scaffold can't know the target dir, and
    //     anything it wrote would point into the cache (broken on prune).
    //     → skip.
    //   - source-repo dev (maintainers running `npm install` inside
    //     /Users/.../sitemd): don't pollute the source tree. → skip.
    //   - dep install (`npm install @sitemd-cc/sitemd` in a user project):
    //     write agent files at INIT_CWD pointing at the Phase-4 scaffold
    //     (./sitemd/sitemd) or the bin shim fallback. → run.
    const projectRoot = process.env.INIT_CWD
    const isNpxCache = __dirname.split(path.sep).includes('_npx')
    const isSourceRepo = projectRoot && path.resolve(projectRoot) === path.resolve(__dirname, '..')
    if (projectRoot && !isNpxCache && !isSourceRepo) {
      // Phase 4: auto-scaffold `./sitemd/` so `npm install @sitemd-cc/sitemd`
      // produces the same end state as `npx init sitemd`. Shell out to the
      // binary we just downloaded; `--skip-agent-files` keeps init from
      // writing a cwd-level pass (postinstall owns that via setupAgentFiles
      // below). `--quiet` suppresses init's Next-Steps output; this
      // postinstall prints its own unified message.
      const scaffoldDir = path.join(projectRoot, 'sitemd')
      if (!fs.existsSync(scaffoldDir)) {
        try {
          execFileSync(binaryPath, ['init', 'sitemd', '--skip-agent-files', '--quiet'], {
            stdio: 'inherit',
            cwd: projectRoot,
          })
        } catch (err) {
          console.error(`  sitemd: scaffold failed (${err.message})`)
          console.error(`  To retry manually: ./node_modules/.bin/sitemd init sitemd`)
        }
      } else {
        console.log(`  sitemd: ./sitemd/ already exists — skipped scaffolding`)
      }

      await setupAgentFiles(__dirname, projectRoot)

      printNextSteps(projectRoot)
    }
  } catch (err) {
    console.error(`  sitemd install failed: ${err.message}`)
    console.error(`  To retry: node sitemd/install.js   (or ./sitemd/install on Unix)`)
  } finally {
    try { fs.rmSync(tmpDir, { recursive: true, force: true }) } catch {}
  }
}

// Run main() only when invoked directly (e.g. `node sitemd/install.js` or
// npm's postinstall hook). When required from cli.js as a recovery path,
// the caller invokes main() itself and handles errors.
if (require.main === module) {
  main().catch(err => {
    console.error(`  sitemd install failed: ${err.message}`)
    console.error(`  To retry: node sitemd/install.js   (or ./sitemd/install on Unix)`)
    // Always exit 0 — npm install must not fail because of binary download trouble
    process.exit(0)
  })
}

module.exports = { main, detectPlatform }
