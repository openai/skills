#!/usr/bin/env bash
set -euo pipefail

resolve_npx() {
  if command -v npx >/dev/null 2>&1; then
    command -v npx
    return 0
  fi

  local candidate
  local -a candidates=()

  if [[ -n "${NODE_VIRTUAL_ENV:-}" ]]; then
    candidates+=("${NODE_VIRTUAL_ENV}/bin/npx")
  fi
  if [[ -n "${NODEENV_ROOT:-}" ]]; then
    candidates+=("${NODEENV_ROOT}/bin/npx")
  fi
  if [[ -n "${VIRTUAL_ENV:-}" ]]; then
    candidates+=("${VIRTUAL_ENV}/bin/npx")
  fi

  for candidate in "${candidates[@]}"; do
    if [[ -x "${candidate}" ]]; then
      printf '%s\n' "${candidate}"
      return 0
    fi
  done

  return 1
}

npx_bin="$(resolve_npx || true)"
if [[ -z "${npx_bin}" ]]; then
  echo "Error: npx is required but was not found on PATH or in nodeenv locations." >&2
  echo "Hint: activate a nodeenv, or set NODEENV_ROOT=/path/to/nodeenv." >&2
  exit 1
fi

if [[ "${npx_bin}" == */* ]]; then
  npx_dir="$(dirname "${npx_bin}")"
  export PATH="${npx_dir}:${PATH}"
fi

has_session_flag="false"
for arg in "$@"; do
  case "$arg" in
    --session|--session=*)
      has_session_flag="true"
      break
      ;;
  esac
done

cmd=("${npx_bin}" --yes --package @playwright/cli playwright-cli)
if [[ "${has_session_flag}" != "true" && -n "${PLAYWRIGHT_CLI_SESSION:-}" ]]; then
  cmd+=(--session "${PLAYWRIGHT_CLI_SESSION}")
fi
cmd+=("$@")

exec "${cmd[@]}"
