#!/usr/bin/env node

import crypto from "node:crypto";
import { existsSync, readFileSync, statSync } from "node:fs";
import path from "node:path";
import chalk from "chalk";
import { joinURL } from "ufo";

import { VIBE_HUB_URL_DEFAULT, isMainModule } from "./constants.mjs";
import { getAccessToken } from "./auth.mjs";

// Media Kit component DID for image uploads
const MEDIA_KIT_DID = "z8ia1mAXo8ZE7ytGF36L5uBf9kD2kenhqFGp9";

/**
 * Get component mount point from blocklet info
 * @param {string} appUrl - Application URL
 * @param {string} did - Component DID
 * @returns {Promise<string>} Mount point path
 */
async function getComponentMountPoint(appUrl, did) {
  const blockletJsUrl = joinURL(appUrl, "__blocklet__.js?type=json");

  const response = await fetch(blockletJsUrl, {
    method: "GET",
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch blocklet info: ${response.status} ${response.statusText}`);
  }

  const config = await response.json();
  const component = config.componentMountPoints?.find((c) => c.did === did);

  if (!component) {
    throw new Error(`Media component not found. The MyVibe instance may not support image uploads.`);
  }

  return component.mountPoint;
}

/**
 * Get MIME type from file extension
 * @param {string} filePath - File path
 * @returns {string} MIME type
 */
function getMimeType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const mimeTypes = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
  };
  return mimeTypes[ext] || "application/octet-stream";
}

/**
 * Upload an image file using TUS protocol
 * @param {string} filePath - Path to image file
 * @param {string} hubUrl - MyVibe hub URL
 * @param {string} accessToken - Access token
 * @returns {Promise<{url: string}>} Upload result with image URL
 */
async function uploadImageFile(filePath, hubUrl, accessToken) {
  const url = new URL(hubUrl);
  const mountPoint = await getComponentMountPoint(hubUrl, MEDIA_KIT_DID);
  const uploadEndpoint = `${url.origin}${mountPoint}/api/uploads`;

  // Read file info
  const fileBuffer = readFileSync(filePath);
  const stats = statSync(filePath);
  const fileSize = stats.size;
  const fileExt = path.extname(filePath).substring(1);
  const mimeType = getMimeType(filePath);

  // Generate hash-based filename
  const fileHash = crypto.createHash("sha256").update(fileBuffer).digest("hex");
  const hashBasedFilename = `${fileHash.substring(0, 16)}.${fileExt}`;

  const uploaderId = "MyVibeImageUpload";
  const fileId = `${uploaderId}-${fileHash.substring(0, 16)}`;

  // TUS metadata
  const tusMetadata = {
    uploaderId,
    relativePath: hashBasedFilename,
    name: hashBasedFilename,
    type: mimeType,
    filetype: mimeType,
    filename: hashBasedFilename,
  };

  const encodedMetadata = Object.entries(tusMetadata)
    .map(([key, value]) => `${key} ${Buffer.from(value).toString("base64")}`)
    .join(",");

  const endpointPath = new URL(uploadEndpoint).pathname;

  console.log(chalk.cyan(`Uploading image: ${path.basename(filePath)} (${(fileSize / 1024).toFixed(2)} KB)`));

  // Step 1: Create upload
  const createResponse = await fetch(uploadEndpoint, {
    method: "POST",
    headers: {
      "Tus-Resumable": "1.0.0",
      "Upload-Length": fileSize.toString(),
      "Upload-Metadata": encodedMetadata,
      Authorization: `Bearer ${accessToken}`,
      "x-uploader-file-name": hashBasedFilename,
      "x-uploader-file-id": fileId,
      "x-uploader-file-ext": fileExt,
      "x-uploader-base-url": endpointPath,
      "x-uploader-endpoint-url": uploadEndpoint,
      "x-uploader-metadata": JSON.stringify({
        uploaderId,
        relativePath: hashBasedFilename,
        name: hashBasedFilename,
        type: mimeType,
      }),
      "x-component-did": MEDIA_KIT_DID,
    },
  });

  if (!createResponse.ok) {
    const errorText = await createResponse.text();
    throw new Error(`Failed to create upload: ${createResponse.status} ${createResponse.statusText}\n${errorText}`);
  }

  const uploadUrl = createResponse.headers.get("Location");
  if (!uploadUrl) {
    throw new Error("No upload URL received from server");
  }

  // Step 2: Upload file content
  const uploadResponse = await fetch(`${url.origin}${uploadUrl}`, {
    method: "PATCH",
    headers: {
      "Tus-Resumable": "1.0.0",
      "Upload-Offset": "0",
      "Content-Type": "application/offset+octet-stream",
      Authorization: `Bearer ${accessToken}`,
      "x-uploader-file-name": hashBasedFilename,
      "x-uploader-file-id": fileId,
      "x-uploader-file-ext": fileExt,
      "x-uploader-base-url": endpointPath,
      "x-uploader-endpoint-url": uploadEndpoint,
      "x-uploader-metadata": JSON.stringify({
        uploaderId,
        relativePath: hashBasedFilename,
        name: hashBasedFilename,
        type: mimeType,
      }),
      "x-component-did": MEDIA_KIT_DID,
      "x-uploader-file-exist": "true",
    },
    body: fileBuffer,
  });

  if (!uploadResponse.ok) {
    const errorText = await uploadResponse.text();
    throw new Error(`Failed to upload file: ${uploadResponse.status} ${uploadResponse.statusText}\n${errorText}`);
  }

  const result = await uploadResponse.json();

  // Get the uploaded file URL
  let uploadedUrl = result.url;
  if (!uploadedUrl && result?.size) {
    uploadedUrl = uploadResponse.url;
  }

  if (!uploadedUrl) {
    throw new Error("No URL found in the upload response");
  }

  console.log(chalk.green(`✅ Image uploaded: ${uploadedUrl}`));

  return { url: uploadedUrl };
}

/**
 * Upload image to MyVibe
 * @param {Object} options - Upload options
 * @param {string} options.file - Path to image file
 * @param {string} [options.hub] - MyVibe hub URL
 * @returns {Promise<{success: boolean, url?: string, error?: string}>}
 */
export async function uploadImage(options) {
  const { file, hub = VIBE_HUB_URL_DEFAULT } = options;

  try {
    if (!file) {
      throw new Error("Please provide --file <path> to specify the image file");
    }

    const filePath = path.resolve(file);
    if (!existsSync(filePath)) {
      throw new Error(`File not found: ${filePath}`);
    }

    // Validate file type
    const mimeType = getMimeType(filePath);
    if (!mimeType.startsWith("image/")) {
      throw new Error(`Not an image file: ${filePath}`);
    }

    console.log(chalk.bold("\n📷 MyVibe Image Upload\n"));
    console.log(chalk.gray(`Hub: ${hub}`));

    // Get authorization
    const accessToken = await getAccessToken(hub);

    // Upload image
    const result = await uploadImageFile(filePath, hub, accessToken);

    console.log(chalk.green.bold("\n✅ Upload complete!\n"));
    console.log(chalk.cyan(`🔗 ${result.url}\n`));

    return {
      success: true,
      url: result.url,
    };
  } catch (error) {
    console.error(chalk.red(`\n❌ Error: ${error.message}\n`));
    return {
      success: false,
      error: error.message,
    };
  }
}

/**
 * Parse command line arguments
 */
function parseArgs(args) {
  const options = {};

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const nextArg = args[i + 1];

    switch (arg) {
      case "--file":
      case "-f":
        options.file = nextArg;
        i++;
        break;
      case "--hub":
      case "-h":
        options.hub = nextArg;
        i++;
        break;
      case "--help":
        printHelp();
        process.exit(0);
        break;
    }
  }

  return options;
}

/**
 * Print help message
 */
function printHelp() {
  console.log(`
${chalk.bold("MyVibe Image Upload")}

Upload an image to MyVibe and get the URL.

${chalk.bold("Usage:")}
  node upload-image.mjs --file <path> [options]

${chalk.bold("Options:")}
  --file, -f <path>   Path to image file (PNG, JPG, GIF, WebP, SVG)
  --hub, -h <url>     MyVibe URL (default: ${VIBE_HUB_URL_DEFAULT})
  --help              Show this help message

${chalk.bold("Examples:")}
  # Upload a screenshot
  node upload-image.mjs --file ./screenshot.png

  # Upload to specific hub
  node upload-image.mjs --file ./cover.jpg --hub https://myvibe.example.com
`);
}

// CLI entry point
if (isMainModule(import.meta.url)) {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    printHelp();
    process.exit(1);
  }

  const options = parseArgs(args);

  uploadImage(options)
    .then((result) => {
      if (result.success) {
        // Output just the URL for easy script consumption
        console.log(result.url);
      }
      process.exit(result.success ? 0 : 1);
    })
    .catch((error) => {
      console.error(chalk.red(`Fatal error: ${error.message}`));
      process.exit(1);
    });
}

export default uploadImage;
