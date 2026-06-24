import chalk from "chalk";
import { handleAuthError } from "./auth.mjs";

/**
 * Make an authenticated API request
 * @param {string} url - Request URL
 * @param {Object} options - Fetch options
 * @param {string} accessToken - Access token
 * @param {string} hubUrl - Hub URL (for error handling)
 * @returns {Promise<Object>} - Response data
 */
export async function apiRequest(url, options, accessToken, hubUrl) {
  const response = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    let errorMessage;
    let errorCode;
    try {
      const errorData = await response.json();
      errorMessage = errorData.error || errorData.message || response.statusText;
      errorCode = errorData.code;
    } catch {
      errorMessage = response.statusText;
    }

    // Handle auth errors specially, but not subscription-related 403s
    if (response.status === 401 || response.status === 403) {
      // Don't clear auth for subscription-related errors
      if (errorCode !== "PRIVATE_MODE_REQUIRES_SUBSCRIPTION") {
        await handleAuthError(hubUrl, response.status);
      }
    }

    const error = new Error(errorMessage);
    error.status = response.status;
    error.code = errorCode;
    throw error;
  }

  return response.json();
}

/**
 * Make a GET request
 */
export async function apiGet(url, accessToken, hubUrl) {
  return apiRequest(url, { method: "GET" }, accessToken, hubUrl);
}

/**
 * Make a POST request
 */
export async function apiPost(url, data, accessToken, hubUrl) {
  return apiRequest(
    url,
    {
      method: "POST",
      body: JSON.stringify(data),
    },
    accessToken,
    hubUrl
  );
}

/**
 * Make a PATCH request
 */
export async function apiPatch(url, data, accessToken, hubUrl) {
  return apiRequest(
    url,
    {
      method: "PATCH",
      body: JSON.stringify(data),
    },
    accessToken,
    hubUrl
  );
}

/**
 * Subscribe to SSE stream for conversion progress
 * @param {string} url - SSE endpoint URL
 * @param {string} accessToken - Access token
 * @param {string} hubUrl - Hub URL (for error handling)
 * @param {Object} callbacks - Event callbacks
 * @param {Function} callbacks.onMessage - Called on message event
 * @param {Function} callbacks.onProgress - Called on progress event
 * @param {Function} callbacks.onCompleted - Called on completion
 * @param {Function} callbacks.onError - Called on error
 * @returns {Promise<void>}
 */
export async function subscribeToSSE(url, accessToken, hubUrl, callbacks) {
  const { onMessage, onProgress, onCompleted, onError } = callbacks;

  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${accessToken}`,
        Accept: "text/event-stream",
        "Cache-Control": "no-cache",
      },
    });

    if (!response.ok) {
      if (response.status === 401 || response.status === 403) {
        await handleAuthError(hubUrl, response.status);
      }
      throw new Error(`SSE connection failed: ${response.status} ${response.statusText}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();

      if (done) {
        break;
      }

      buffer += decoder.decode(value, { stream: true });

      // Process complete events in buffer
      const lines = buffer.split("\n");
      buffer = lines.pop() || ""; // Keep incomplete line in buffer

      let currentEvent = null;

      for (const line of lines) {
        if (line.startsWith("event: ")) {
          currentEvent = line.slice(7).trim();
        } else if (line.startsWith("data: ")) {
          const dataStr = line.slice(6);
          try {
            const data = JSON.parse(dataStr);

            switch (currentEvent) {
              case "message":
                onMessage?.(data.message || data);
                break;
              case "progress":
                onProgress?.(data);
                break;
              case "completed":
                onCompleted?.(data);
                return; // End stream on completion
              case "error":
                onError?.(data.error || data);
                return; // End stream on error
              default:
                // Handle data without event type
                if (data.message) {
                  onMessage?.(data.message);
                }
            }
          } catch {
            // Non-JSON data, treat as message
            onMessage?.(dataStr);
          }
          currentEvent = null;
        }
      }
    }
  } catch (error) {
    onError?.(error.message || error);
    throw error;
  }
}

/**
 * Poll for conversion status (fallback if SSE doesn't work)
 * @param {string} url - Status endpoint URL
 * @param {string} accessToken - Access token
 * @param {string} hubUrl - Hub URL
 * @param {Object} callbacks - Callbacks
 * @param {number} interval - Poll interval in ms
 * @param {number} timeout - Timeout in ms
 */
export async function pollConversionStatus(
  url,
  accessToken,
  hubUrl,
  callbacks,
  interval = 3000,
  timeout = 300000
) {
  const { onProgress, onCompleted, onError } = callbacks;
  const startTime = Date.now();

  while (Date.now() - startTime < timeout) {
    try {
      const status = await apiGet(url, accessToken, hubUrl);

      onProgress?.(status);

      if (status.status === "COMPLETED") {
        onCompleted?.(status);
        return;
      }

      if (
        status.status === "FAILED" ||
        status.status === "FAILED_VALIDATE_BUNDLE" ||
        status.status === "FAILED_CONVERSION"
      ) {
        onError?.(status.conversionError || "Conversion failed");
        return;
      }

      // Wait before next poll
      await new Promise((resolve) => setTimeout(resolve, interval));
    } catch (error) {
      onError?.(error.message || error);
      throw error;
    }
  }

  onError?.("Conversion timeout");
  throw new Error("Conversion timeout");
}
