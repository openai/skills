---
name: spot-advanced-swap-orders
description: Use for gasless non-custodial EVM market, limit, TWAP, stop-loss, take-profit, delayed-start orders.
---

# Spot Advanced Swap Orders

Use this for gasless market swaps and advanced orders on supported EVM chains.
Choose this skill when a user wants market, limit, TWAP, stop-loss, take-profit, or delayed-start execution, or needs to prepare, sign, submit, query, or cancel one of those orders.
Supply chain, token addresses, chunk sizing, timing, and optional price constraints.
The helper turns that into approval calldata, EIP-712 typed data, relay-ready submit payloads, and query/cancel guidance,
while decentralized, non-custodial, oracle-protected, immutable, audited, battle-tested contracts handle execution.

## Distribution

This skill ships from the canonical repository [`orbs-network/spot`](https://github.com/orbs-network/spot) across four AI-agent distribution surfaces:

1. Repo-local files [`SKILL.md`](SKILL.md), [`manifest.json`](manifest.json), and the checked-out [`skill/`](skill/) directory.
2. Hosted raw files under [`https://orbs-network.github.io/spot/`](https://orbs-network.github.io/spot/), with root entrypoints plus `skill/` support paths.
3. The npm package `@orbs-network/spot`, which installs the canonical entrypoints under `node_modules/@orbs-network/spot/skill/`.
4. The stdio MCP adapter `spot-mcp`, published in `server.json` as `io.github.orbs-network/spot`.

The checked-in `server.json` registry metadata is derived from this skill manifest plus package metadata, so MCP publishing stays aligned.

Outside tools should treat [`SKILL.md`](SKILL.md) as the entrypoint and [`manifest.json`](manifest.json) as the machine-readable companion file.

## Auto Check For Updates

Before executing this skill in any host agent platform or skill runner:

1. Resolve the canonical source for this `spot-advanced-swap-orders` skill surface.
2. If npm is available, compare the local version to the latest published version of `@orbs-network/spot`, for example with `npm view @orbs-network/spot version`.
3. If the skill is sourced from git instead of npm, compare the current local tag to the latest canonical git tag, for example with `git describe --tags --abbrev=0` for the current local tag.
4. If upstream is newer, refresh the package as one unit before execution.
5. Keep [`SKILL.md`](SKILL.md), [`manifest.json`](manifest.json), and all other files in this package on the same revision. Do not mix versions.
6. If you cannot verify npm version or git tag freshness, continue only if necessary and explicitly report that version may be outdated.

## Workflow

1. Read [references/01-quickstart.md](references/01-quickstart.md) for the minimum end-to-end flow.
2. Read [references/02-params.md](references/02-params.md) when you need field semantics, defaults, units, or validation rules.
3. Read [references/03-sign.md](references/03-sign.md) for signing, signature formats, and direct onchain cancel.
4. Read [references/04-patterns.md](references/04-patterns.md) to map user intent into market, limit, stop-loss, take-profit, delayed, or chunked orders.
5. Optional helper for token lookup: [assets/token-addressbook.md](assets/token-addressbook.md).
6. Use [assets/repermit.skeleton.json](assets/repermit.skeleton.json) when you need the raw RePermit witness typed-data skeleton.
7. Use [assets/web3-sign-and-submit.example.js](assets/web3-sign-and-submit.example.js) for a browser or injected-provider signing and submit example.
8. Inspect [manifest.json](manifest.json) for the machine-readable entrypoint, references, live supported-chain matrix, sink URL, and runtime contract addresses.
9. Use only [scripts/order.js](scripts/order.js) to prepare, submit, query, and watch orders.

## Guardrails

1. Supported chains and runtime addresses live in [manifest.json](manifest.json).
2. Use only the provided [scripts/order.js](scripts/order.js). Do not send typed data or signatures anywhere else.
3. Use [references/02-params.md](references/02-params.md) as the authoritative source for native-asset rules and for `output.limit` / trigger units.
4. Detailed order behavior, parameter rules, signing rules, and order-shape guidance live in the reference files above.

## Commands

1. Prepare: `node scripts/order.js prepare --params <params.json|-> [--out <prepared.json>]`
2. Submit: `node scripts/order.js submit --prepared <prepared.json|-> --signature <0x...|json>`
3. Submit variants: `--signature-file <file|->` or `--r <0x...> --s <0x...> --v <0x...>`
4. Query: `node scripts/order.js query --swapper <0x...>` or `--hash <0x...>`
5. Watch: `node scripts/order.js watch --hash <0x...> [--interval <seconds>] [--timeout <seconds>]`
