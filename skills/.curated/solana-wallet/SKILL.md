---
name: solana-wallet
description: Create and manage Solana wallets, check balances, and run SOL/SPL transfers for agent workflows.
metadata:
  short-description: Manage Solana wallets and execute basic on-chain transactions.
---

# Solana Wallet Skill

Use this skill when the user asks to:

- Create a new Solana wallet.
- Import an existing Solana wallet keypair.
- Fetch wallet SOL/SPL balance.
- Send SOL or SPL tokens.
- Request airdrop on devnet/testnet.

## Purpose

This skill gives a low-friction path for on-chain wallet actions without hardcoding private keys in prompts.
It is intentionally focused on safe, deterministic operations and explicit, auditable output.

## Prerequisites

- Node.js 18+
- Install dependencies in the skill folder:

```bash
cd skills/solana-wallet/scripts
npm install
```

Dependencies (via `package.json`):

- `@solana/web3.js`
- `@solana/spl-token`
- `bs58`

## Environment

Either pass `--rpc-url`, or set one of:

- `SOLANA_RPC_URL`
- `RPC_URL`

If omitted, the default is `https://api.devnet.solana.com`.

For wallet actions requiring signing, provide one of:

- `SOLANA_PRIVATE_KEY` env var, or
- `--wallet` argument.

`SOLANA_PRIVATE_KEY` may be:

- Base58 secret key string, or
- A filesystem path to a Base58 or JSON secret-key file.

## Available command

`node solana-wallet.mjs <command> [options]`

### `create-wallet`

Create a new wallet keypair and print base58 secret key output.

Examples:

```bash
node solana-wallet.mjs create-wallet
node solana-wallet.mjs create-wallet --save ./my-wallet.txt
node solana-wallet.mjs create-wallet --save ./my-wallet.json --save-format json-array
```

Output includes:

- `command`
- `publicKey`
- `secretKeyBase58`
- optional `savedTo` path

### `import-wallet`

Load and validate a wallet from inline key bytes or file.

```bash
node solana-wallet.mjs import-wallet --wallet 7x... --print-public-only
node solana-wallet.mjs import-wallet --wallet ./my-wallet.txt
```

### `address`

Print the wallet public address.

```bash
node solana-wallet.mjs address --wallet ./my-wallet.txt
```

### `balance`

Get SOL or SPL balance.

```bash
node solana-wallet.mjs balance
node solana-wallet.mjs balance --public-key 9J7... --rpc-url https://api.devnet.solana.com
node solana-wallet.mjs balance --token-mint EPjFW... --wallet ./my-wallet.txt
```

### `transfer`

Transfer SOL or SPL tokens.

```bash
node solana-wallet.mjs transfer --wallet ./my-wallet.txt --to 8x2... --amount 1.25
node solana-wallet.mjs transfer --wallet ./my-wallet.txt --to 8x2... --amount 100 --token-mint EPjFW...
```

Output includes:

- `signature`
- `from`
- `to`
- `amount`
- `token` (`SOL` or mint address)

### `request-faucet`

Request airdrop (devnet/testnet only).

```bash
node solana-wallet.mjs request-faucet --wallet ./my-wallet.txt --amount 5
node solana-wallet.mjs request-faucet --wallet ./my-wallet.txt --rpc-url https://api.devnet.solana.com
```

`mainnet-beta` requires `--allow-mainnet-faucet` to run, and still fails if your RPC disallows it.

## Script workflow

- Keep secrets out of conversation logs when possible.
- Validate recipient addresses and mint addresses before transfer.
- Confirm network and amounts in any manual transfer review.
- Never commit or print secret keys in generated artifacts.

## Notes

This skill is intentionally lightweight and MCP-ready. It uses direct Solana Web3 calls for deterministic behavior and avoids hidden state.

