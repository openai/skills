---
name: payme
description: Send and receive USDC/USDT crypto payments via PayMe smart wallets. Use when the user wants to check their crypto balance, send stablecoins to someone, view transaction history, manage contacts, sell crypto for naira via P2P, or do anything related to PayMe wallet operations. Supports Base, Arbitrum, Polygon, BNB Chain, and Avalanche.
---

# PayMe - Crypto Payments Skill

PayMe provides gasless USDC/USDT payments through ERC-4337 smart wallets on Base, Arbitrum, Polygon, BNB Chain, and Avalanche.

**API Base URL:** `https://payme.feedom.tech`

## Installation

Copy this skill folder into your agent's skills directory:
- **Codex:** `~/.codex/skills/payme/`
- **Cursor:** `~/.cursor/skills/payme/`

## Getting a PayMe Account

If the user does not have a PayMe account yet, they need to create one first:

1. Open the PayMe Telegram bot: [@veedombot](https://t.me/veedombot)
2. Send `/start` to create a wallet
3. Set a PIN with `/setpin`
4. Use the resulting username and PIN to connect below

Alternatively, sign up at [payme.feedom.tech](https://payme.feedom.tech).

## Setup (one-time)

Connect the user's PayMe account to get an agent token:

```bash
curl -X POST https://payme.feedom.tech/api/agent/connect \
  -H "Content-Type: application/json" \
  -d '{"identifier": "USERNAME_OR_ADDRESS", "pin": "USER_PIN"}'
```

Alternatively, restore by master private key: `{"masterPrivateKey": "0x..."}`.

The response contains an `agentToken`. Store it and use it as `Authorization: Bearer <agentToken>` on all subsequent requests. Tokens last 90 days.

## Available Actions

All endpoints use base URL `https://payme.feedom.tech` and require `Authorization: Bearer <agentToken>`.

### Check Balances

```
GET /api/agent/balances
```

Returns total USDC/USDT across all chains plus per-chain breakdown.

### Send Payment (two-step)

**Step 1 — Prepare:**

```
POST /api/agent/send
{ "recipient": "username, email, or 0x address", "amount": "10", "token": "USDC" }
```

Returns a `confirmationId` and a `preview` with fee breakdown. Always show the preview to the user before confirming.

**Step 2 — Confirm:**

```
POST /api/agent/confirm
{ "confirmationId": "uuid-from-step-1" }
```

Returns `txHash` on success. Confirmations expire after 5 minutes.

### View Transaction History

```
GET /api/agent/history?limit=20
```

### Manage Contacts

```
GET /api/agent/contacts
POST /api/agent/contacts  { "name": "Alice", "address": "0x..." }
DELETE /api/agent/contacts/:name
```

### Wallet Info

```
GET /api/agent/wallet
```

Returns kernel address, supported chains, and supported tokens.

### Revoke Token

```
POST /api/agent/revoke
```

Revokes the current agent token immediately.

## Sell Crypto for Naira (P2P)

Convert USDC/USDT to Nigerian naira. Your crypto goes into escrow, a vendor sends naira to your bank, you confirm receipt, escrow releases to vendor.

### 1. Save bank account (one-time)

```
POST /api/agent/p2p/bank-accounts
{ "bankName": "GTBank", "accountNumber": "0123456789", "accountName": "John Doe" }
```

List saved accounts: `GET /api/agent/p2p/bank-accounts`

### 2. Check rates

```
GET /api/agent/p2p/rates?token=USDC&currency=NGN
```

Returns vendor rates sorted by best rate. Each entry includes `vendorId`, `vendorName`, `rate` (NGN per USD), `avgRating`, and order limits.

### 3. Sell (create order)

Before calling this endpoint, **always compute and show the user a preview**: amount x rate = naira they'll receive. Get explicit approval.

```
POST /api/agent/p2p/sell
{ "token": "USDC", "amount": 50, "bankAccountId": 1 }
```

Optionally pass `vendorId` to pick a specific vendor; otherwise the best available vendor is auto-selected. This locks crypto in escrow immediately.

### 4. Track order

```
GET /api/agent/p2p/orders/:id
```

Poll this endpoint to check status. Key statuses:
- `escrow_locked` — waiting for vendor to accept
- `accepted` — vendor accepted, will send naira soon
- `fiat_sent` — vendor says naira was sent, check your bank
- `completed` — you confirmed, escrow released
- `disputed` — dispute opened, admin reviewing

### 5. Confirm naira received

Once the user confirms money arrived in their bank:

```
POST /api/agent/p2p/orders/:id/confirm
```

This releases escrow to the vendor. **Irreversible.**

### 6. Dispute (if needed)

If naira was not received or something is wrong:

```
POST /api/agent/p2p/orders/:id/dispute
{ "reason": "Vendor marked paid but naira not received after 1 hour" }
```

This cancels auto-release and triggers admin investigation.

### 7. Rate vendor (optional)

```
POST /api/agent/p2p/orders/:id/rate
{ "rating": 5, "comment": "Fast payment" }
```

## Important Rules

1. **Always confirm payments.** Never skip the two-step send flow. Show the preview (amount, fee, chain, recipient) and get explicit user approval before calling `/api/agent/confirm`.
2. **Always preview P2P sells.** Compute amount x rate and show the naira total before calling `/api/agent/p2p/sell`. Get explicit user approval.
3. **Confirm fiat is irreversible.** Only call `/api/agent/p2p/orders/:id/confirm` after the user verifies naira is in their bank.
4. **Token is USDC or USDT.** No other tokens are supported.
5. **Recipients** can be a PayMe username, email, or `0x` wallet address.
6. **Fees** are shown in the send preview. The net amount (after fee) is what the recipient gets.
7. **Do not** expose or log the agent token, master keys, or private keys.

## Full API Reference

For complete request/response schemas and error codes, see [references/api-reference.md](references/api-reference.md).
