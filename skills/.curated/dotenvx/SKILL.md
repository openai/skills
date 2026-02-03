---
name: dotenvx
description: Secure dotenv CLI and library for loading, encrypting, and managing .env files across languages and environments. Use when setting up dotenvx, running commands with dotenvx run, composing multiple env files, using encryption/decryption and keys, advanced CLI flags, or dotenvx ops workflows.
---

# Dotenvx

## Overview

Use dotenvx to inject environment variables at runtime, manage multiple .env files, encrypt secrets, and support ops workflows. Prefer the CLI for cross-language usage and the library for Node.js integration.

## Quickstart

### CLI

1. Install the CLI (curl, brew, docker, winget) or use `npx @dotenvx/dotenvx` for ad hoc runs.
2. Create a `.env` file and run a command with injected envs.

```sh
echo "HELLO=World" > .env
dotenvx run -- node index.js
```

### Node.js library

```js
require('@dotenvx/dotenvx').config()
```

When using Deno, install the CLI binary instead of the npm module to avoid cipher support issues.

## Run Anywhere

Use `dotenvx run -- <command>` to inject envs for any runtime or framework.

```sh
dotenvx run -- python3 index.py
dotenvx run -- bun index.js
dotenvx run -- next dev
```

Use `-f` to point at non-default env files:

```sh
dotenvx run -f .env.production -- node index.js
```

## Multiple Environments

- Load multiple files with repeated `-f` flags.
- Earlier files win by default; use `--overload` to let later files override.
- Use `--convention=nextjs` or `--convention=flow` to match framework load order.
- Prefer `DOTENV_ENV` over `NODE_ENV` when using flow conventions across runtimes.

```sh
dotenvx run -f .env.local -f .env -- node index.js
dotenvx run -f .env.local -f .env --overload -- node index.js
```

## Encryption

- Encrypt `.env` files with `dotenvx encrypt` and keep `.env.keys` out of git.
- Decrypt at runtime by setting `DOTENV_PRIVATE_KEY` or `DOTENV_PRIVATE_KEY_<ENV>`.
- Combine multiple encrypted files by setting multiple private keys.

```sh
dotenvx encrypt
dotenvx ext gitignore --pattern .env.keys
DOTENV_PRIVATE_KEY="..." dotenvx run -- node index.js
DOTENV_PRIVATE_KEY_PRODUCTION="..." dotenvx run -- node index.js
```

## Advanced CLI

- `dotenvx get` and `dotenvx set` manage individual keys.
- `dotenvx encrypt`, `decrypt`, `rotate`, `keypair`, and `ls` manage encrypted envs.
- `--env` sets inline variables, `--quiet/--verbose/--debug` tune output.
- `--strict` fails on missing files or decryption errors; `--ignore` suppresses specific errors.
- Variable expansion, default/alternate values, command substitution, and multiline values are supported.

Use `dotenvx help` and `dotenvx help <command>` for command-specific details.

## Ops

Dotenvx Ops adds operational primitives for teams (backups, access controls, status).

```sh
curl -sfS https://dotenvx.sh/ops | sh
dotenvx ops login
dotenvx ops backup
dotenvx ops status
```

## References

Use `references/cheatsheet.md` for common command snippets and patterns.
