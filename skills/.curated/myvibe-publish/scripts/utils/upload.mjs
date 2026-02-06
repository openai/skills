import { createReadStream } from "node:fs";
import { stat } from "node:fs/promises";
import { basename, extname } from "node:path";
import crypto from "node:crypto";
import chalk from "chalk";
import { joinURL } from "ufo";

import { API_PATHS } from "./constants.mjs";
import { handleAuthError } from "./auth.mjs";

/**
 * Upload a file to MyVibe using TUS protocol
 * @param {string} filePath - Path to the file to upload
 * @param {string} hubUrl - MyVibe URL
 * @param {string} accessToken - Access token
 * @param {Object} options - Upload options
 * @param {string} [options.did] - Existing Vibe DID for version update
 * @returns {Promise<{did: string, id: string, status: string}>} - Upload result
 */
export async function uploadFile(filePath, hubUrl, accessToken, options = {}) {
  const { did } = options;
  const { origin } = new URL(hubUrl);

  // Build upload endpoint with optional did query parameter
  let uploadEndpoint = joinURL(origin, API_PATHS.UPLOAD);
  if (did) {
    uploadEndpoint = `${uploadEndpoint}?did=${encodeURIComponent(did)}`;
  }

  // Get file info
  const fileStat = await stat(filePath);
  const fileSize = fileStat.size;
  const fileName = basename(filePath);
  const fileExt = extname(filePath).slice(1).toLowerCase();

  // Determine MIME type
  let mimeType = "application/octet-stream";
  if (fileExt === "zip") {
    mimeType = "application/zip";
  } else if (fileExt === "html" || fileExt === "htm") {
    mimeType = "text/html";
  }

  // Generate file ID
  const fileHash = crypto.randomBytes(16).toString("hex");
  const uploaderId = "MyVibePublish";
  const fileId = `${uploaderId}-${fileHash}`;

  console.log(chalk.cyan(`\nUploading: ${fileName} (${(fileSize / 1024).toFixed(2)} KB)`));

  // Use random hash prefix to avoid filename collision
  const uniqueFileName = `${fileHash.slice(0, 8)}-${fileName}`;

  // TUS metadata
  const tusMetadata = {
    uploaderId,
    relativePath: uniqueFileName,
    name: uniqueFileName,
    type: mimeType,
    filetype: mimeType,
    filename: uniqueFileName,
  };

  const encodedMetadata = Object.entries(tusMetadata)
    .map(([key, value]) => `${key} ${Buffer.from(String(value)).toString("base64")}`)
    .join(",");

  const endpointPath = new URL(uploadEndpoint).pathname;

  // Step 1: Create upload
  const createResponse = await fetch(uploadEndpoint, {
    method: "POST",
    headers: {
      "Tus-Resumable": "1.0.0",
      "Upload-Length": fileSize.toString(),
      "Upload-Metadata": encodedMetadata,
      Authorization: `Bearer ${accessToken}`,
      "x-uploader-file-name": uniqueFileName,
      "x-uploader-file-id": fileId,
      "x-uploader-file-ext": fileExt,
      "x-uploader-base-url": endpointPath,
      "x-uploader-endpoint-url": uploadEndpoint,
      "x-uploader-metadata": JSON.stringify({
        uploaderId,
        relativePath: uniqueFileName,
        name: uniqueFileName,
        type: mimeType,
      }),
    },
  });

  if (!createResponse.ok) {
    if (createResponse.status === 401 || createResponse.status === 403) {
      await handleAuthError(hubUrl, createResponse.status);
    }
    const errorText = await createResponse.text();
    throw new Error(`Failed to create upload: ${createResponse.status} ${createResponse.statusText}\n${errorText}`);
  }

  const uploadUrl = createResponse.headers.get("Location");
  if (!uploadUrl) {
    throw new Error("No upload URL received from server");
  }
  console.log(chalk.gray(`  Upload URL: ${uploadUrl}`));

  console.log(chalk.gray("  Upload created, sending file data..."));

  // Step 2: Read file and upload content
  const fileBuffer = await readFileAsBuffer(filePath);

  const uploadResponse = await fetch(`${origin}${uploadUrl}`, {
    method: "PATCH",
    headers: {
      "Tus-Resumable": "1.0.0",
      "Upload-Offset": "0",
      "Content-Type": "application/offset+octet-stream",
      Authorization: `Bearer ${accessToken}`,
      "x-uploader-file-name": uniqueFileName,
      "x-uploader-file-id": fileId,
      "x-uploader-file-ext": fileExt,
      "x-uploader-base-url": endpointPath,
      "x-uploader-endpoint-url": uploadEndpoint,
      "x-uploader-metadata": JSON.stringify({
        uploaderId,
        relativePath: uniqueFileName,
        name: uniqueFileName,
        type: mimeType,
      }),
      "x-uploader-file-exist": "true",
    },
    body: fileBuffer,
  });

  if (!uploadResponse.ok) {
    if (uploadResponse.status === 401 || uploadResponse.status === 403) {
      await handleAuthError(hubUrl, uploadResponse.status);
    }
    const errorText = await uploadResponse.text();
    throw new Error(`Failed to upload file: ${uploadResponse.status} ${uploadResponse.statusText}\n${errorText}`);
  }

  let result;
  try {
    result = await uploadResponse.json();
  } catch {
    throw new Error("Invalid response from server after upload");
  }

  // Check for upload errors
  if (result.error) {
    throw new Error(`Upload error: ${result.error.code || result.error.message || JSON.stringify(result.error)}`);
  }

  // Extract blocklet info from result
  const blocklet = result.blocklet;
  if (!blocklet) {
    throw new Error("No blocklet info in upload response");
  }

  console.log(chalk.green(`✅ Upload complete! DID: ${blocklet.did}`));

  return {
    did: blocklet.did,
    id: blocklet.id,
    status: blocklet.status,
    isNewUpload: blocklet.isNewUpload,
    versionHistoryEnabled: blocklet.versionHistoryEnabled,
  };
}

/**
 * Read file as buffer
 * @param {string} filePath - File path
 * @returns {Promise<Buffer>}
 */
async function readFileAsBuffer(filePath) {
  const chunks = [];
  const stream = createReadStream(filePath);

  return new Promise((resolve, reject) => {
    stream.on("data", (chunk) => chunks.push(chunk));
    stream.on("end", () => resolve(Buffer.concat(chunks)));
    stream.on("error", reject);
  });
}

/**
 * Create a vibe from URL
 * @param {string} url - URL to import
 * @param {string} hubUrl - MyVibe URL
 * @param {string} accessToken - Access token
 * @param {Object} metadata - Vibe metadata
 * @returns {Promise<{did: string, id: string}>}
 */
export async function createVibeFromUrl(url, hubUrl, accessToken, metadata = {}) {
  const { origin } = new URL(hubUrl);
  const apiUrl = joinURL(origin, API_PATHS.VIBES_FROM_URL);

  console.log(chalk.cyan(`\nImporting URL: ${url}`));

  const response = await fetch(apiUrl, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      url,
    }),
  });

  if (!response.ok) {
    if (response.status === 401 || response.status === 403) {
      await handleAuthError(hubUrl, response.status);
    }
    let errorMessage;
    try {
      const errorData = await response.json();
      errorMessage = errorData.error || errorData.message || response.statusText;
    } catch {
      errorMessage = response.statusText;
    }
    throw new Error(`Failed to create vibe from URL: ${errorMessage}`);
  }

  const result = await response.json();
  const blocklet = result.blocklet;

  if (!blocklet || !blocklet.did) {
    throw new Error("No blocklet info in response");
  }

  console.log(chalk.green(`✅ Vibe created! DID: ${blocklet.did}`));

  return {
    did: blocklet.did,
    id: blocklet.id,
    status: blocklet.status,
  };
}
