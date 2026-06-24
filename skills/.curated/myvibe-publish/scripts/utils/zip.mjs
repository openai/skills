import { createWriteStream } from "node:fs";
import { stat, mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, basename } from "node:path";
import archiver from "archiver";
import chalk from "chalk";

/**
 * Compress a directory into a ZIP file
 * @param {string} dirPath - Path to the directory to compress
 * @param {string} [outputPath] - Optional output path for the ZIP file
 * @returns {Promise<{zipPath: string, cleanup: Function}>} - Path to the created ZIP and cleanup function
 */
export async function zipDirectory(dirPath, outputPath) {
  // Verify directory exists
  const dirStat = await stat(dirPath);
  if (!dirStat.isDirectory()) {
    throw new Error(`Not a directory: ${dirPath}`);
  }

  // Create temp directory if no output path specified
  let tempDir = null;
  let zipPath = outputPath;

  if (!zipPath) {
    tempDir = await mkdtemp(join(tmpdir(), "myvibe-publish-"));
    const dirName = basename(dirPath);
    zipPath = join(tempDir, `${dirName}.zip`);
  }

  console.log(chalk.cyan(`Compressing directory: ${dirPath}`));

  return new Promise((resolve, reject) => {
    const output = createWriteStream(zipPath);
    const archive = archiver("zip", {
      zlib: { level: 9 }, // Maximum compression
    });

    output.on("close", () => {
      const sizeKB = (archive.pointer() / 1024).toFixed(2);
      console.log(chalk.green(`✅ Created ZIP: ${zipPath} (${sizeKB} KB)`));

      resolve({
        zipPath,
        size: archive.pointer(),
        cleanup: async () => {
          if (tempDir) {
            try {
              await rm(tempDir, { recursive: true, force: true });
            } catch {
              // Ignore cleanup errors
            }
          }
        },
      });
    });

    archive.on("error", (err) => {
      reject(new Error(`Failed to create ZIP: ${err.message}`));
    });

    archive.on("warning", (err) => {
      if (err.code === "ENOENT") {
        console.warn(chalk.yellow(`Warning: ${err.message}`));
      } else {
        reject(err);
      }
    });

    // Progress logging
    let lastPercent = 0;
    archive.on("progress", (progress) => {
      const percent = Math.floor((progress.fs.processedBytes / progress.fs.totalBytes) * 100);
      if (percent >= lastPercent + 20) {
        console.log(chalk.gray(`  Compressing... ${percent}%`));
        lastPercent = percent;
      }
    });

    archive.pipe(output);

    // Add directory contents to ZIP (not the directory itself)
    archive.directory(dirPath, false);

    archive.finalize();
  });
}

/**
 * Get file info for upload
 * @param {string} filePath - Path to the file
 * @returns {Promise<{path: string, size: number, name: string, type: string}>}
 */
export async function getFileInfo(filePath) {
  const fileStat = await stat(filePath);

  if (!fileStat.isFile()) {
    throw new Error(`Not a file: ${filePath}`);
  }

  const name = basename(filePath);
  const ext = name.split(".").pop()?.toLowerCase();

  let type = "application/octet-stream";
  if (ext === "zip") {
    type = "application/zip";
  } else if (ext === "html" || ext === "htm") {
    type = "text/html";
  }

  return {
    path: filePath,
    size: fileStat.size,
    name,
    type,
  };
}
