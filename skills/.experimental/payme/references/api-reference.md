# PayMe Agent API Reference

Base URL: `https://payme.feedom.tech`

All authenticated endpoints require: `Authorization: Bearer <agentToken>`

---

## POST /api/agent/connect

Connect or link a PayMe account. No auth header needed.

**Request (login):**
```json
{ "identifier": "username, email, or 0x address", "pin": "1234" }
```

**Request (restore by key):**
```json
{ "masterPrivateKey": "0x..." }
```

**Response (200):**
```json
{
  "agentToken": "64-char hex string",
  "kernelAddress": "0x...",
  "username": "alice",
  "scopes": ["wallet:read", "contacts:read", "contacts:write", "payments:prepare", "payments:execute"]
}
```

**Errors:**
- `400` — Missing fields
- `401` — Invalid PIN
- `404` — User not found

---

## GET /api/agent/wallet

**Scope:** `wallet:read`

**Response (200):**
```json
{
  "kernelAddress": "0x...",
  "username": "alice",
  "supportedChains": ["arbitrum", "base", "polygon", "bsc", "avalanche"],
  "supportedTokens": ["USDC", "USDT"]
}
```

---

## GET /api/agent/balances

**Scope:** `wallet:read`

**Response (200):**
```json
{
  "balances": { "USDC": "150.00", "USDT": "25.50" },
  "chainBalances": [
    { "chain": "base", "chainName": "Base", "USDC": "100.00", "USDT": "0.00" },
    { "chain": "arbitrum", "chainName": "Arbitrum One", "USDC": "50.00", "USDT": "25.50" }
  ]
}
```

---

## POST /api/agent/send

Prepare a payment. Returns a preview for user confirmation.

**Scope:** `payments:prepare`

**Request:**
```json
{
  "recipient": "username, email, or 0x address",
  "amount": 10,
  "token": "USDC"
}
```

- `amount`: number or string, must be > 0 and <= 1,000,000
- `token`: `"USDC"` or `"USDT"` (case-insensitive)

**Response (200):**
```json
{
  "confirmationId": "uuid",
  "preview": {
    "recipient": "alice",
    "resolvedAddress": "0x...",
    "amount": "10.00",
    "token": "USDC",
    "chain": "base",
    "chainName": "Base",
    "fee": "0.05 USDC",
    "feePercent": "0.50%",
    "netAmount": "9.95 USDC"
  }
}
```

**Errors:**
- `400` — Invalid amount, token, or recipient
- `400` — Insufficient balance or no available chain

---

## POST /api/agent/confirm

Execute a previously prepared payment.

**Scope:** `payments:execute`

**Request:**
```json
{ "confirmationId": "uuid-from-send" }
```

**Response (200):**
```json
{
  "success": true,
  "txHash": "0x...",
  "fee": "50000",
  "netAmount": "9950000",
  "chain": "base"
}
```

- `fee` and `netAmount` are raw uint256 strings (6 decimals for USDC/USDT)

**Errors:**
- `404` — Confirmation not found or expired
- `403` — Payment does not belong to this token holder
- `410` — Confirmation expired (>5 min)

---

## GET /api/agent/history

**Scope:** `wallet:read`

**Query params:**
- `limit` (optional, default 20, max 50)

**Response (200):**
```json
{
  "transactions": [
    {
      "id": "123-0",
      "type": "sent",
      "recipient": "0x...",
      "amount": "10.00",
      "token": "USDC",
      "chain": "base",
      "txHash": "0x...",
      "createdAt": "2025-01-15T10:30:00Z"
    }
  ]
}
```

---

## GET /api/agent/contacts

**Scope:** `contacts:read`

**Response (200):**
```json
{
  "contacts": [
    { "name": "Alice", "address": "0x..." },
    { "name": "Bob", "address": "0x..." }
  ]
}
```

---

## POST /api/agent/contacts

**Scope:** `contacts:write`

**Request:**
```json
{ "name": "Alice", "address": "0x..." }
```

**Response (200):**
```json
{ "success": true }
```

**Errors:**
- `400` — Missing name or address, or invalid address

---

## DELETE /api/agent/contacts/:name

**Scope:** `contacts:write`

**Response (200):**
```json
{ "success": true }
```

---

## POST /api/agent/revoke

Revokes the current agent token. Only requires a valid Bearer token (no scope needed).

**Response (200):**
```json
{ "success": true, "revoked": true }
```

---

---

# P2P Endpoints — Sell Crypto for Naira

## GET /api/agent/p2p/rates

Public endpoint (no auth required).

**Query params:**
- `token` (optional, default `USDC`)
- `currency` (optional, default `NGN`)

**Response (200):**
```json
{
  "rates": [
    {
      "vendorId": 1,
      "vendorName": "FastPay",
      "rate": 1580.00,
      "avgRating": 4.8,
      "completionRate": 0.97,
      "responseTimeAvg": 120,
      "totalTrades": 350,
      "minOrderUsd": 5,
      "maxOrderUsd": 500,
      "totalDisputes": 2,
      "disputesWon": 1,
      "disputesLost": 1
    }
  ]
}
```

---

## GET /api/agent/p2p/bank-accounts

**Scope:** `wallet:read`

**Response (200):**
```json
{
  "accounts": [
    {
      "id": 1,
      "user_id": 4,
      "bank_name": "GTBank",
      "account_number": "0123456789",
      "account_name": "John Doe",
      "is_default": 1,
      "created_at": "2025-01-15T10:00:00Z"
    }
  ]
}
```

---

## POST /api/agent/p2p/bank-accounts

**Scope:** `wallet:read`

**Request:**
```json
{ "bankName": "GTBank", "accountNumber": "0123456789", "accountName": "John Doe" }
```

**Response (200):**
```json
{ "success": true, "account": { "id": 1, "bank_name": "GTBank", "account_number": "0123456789", "account_name": "John Doe", "is_default": 1 } }
```

**Errors:**
- `400` — Missing fields
- `409` — Bank account number already registered to another user

---

## DELETE /api/agent/p2p/bank-accounts/:id

**Scope:** `wallet:read`

**Response (200):**
```json
{ "success": true, "removed": true }
```

---

## POST /api/agent/p2p/sell

Create a sell order. Locks crypto in escrow immediately.

**Scope:** `payments:prepare` + `payments:execute`

**Request:**
```json
{
  "token": "USDC",
  "amount": 50,
  "bankAccountId": 1,
  "vendorId": null
}
```

- `token`: `"USDC"` or `"USDT"`
- `amount`: number, must be > 0
- `bankAccountId`: from `/api/agent/p2p/bank-accounts`
- `vendorId` (optional): pick a specific vendor from `/api/agent/p2p/rates`, or omit for auto-selection

**Response (200):**
```json
{
  "success": true,
  "order": {
    "id": "uuid",
    "status": "escrow_locked",
    "token": "USDC",
    "cryptoAmount": 50.0,
    "fiatAmount": 79000.0,
    "fiatCurrency": "NGN",
    "rate": 1580.0,
    "chain": "arbitrum",
    "expiresAt": "2025-01-15T16:00:00Z"
  },
  "vendor": {
    "id": 1,
    "name": "FastPay"
  }
}
```

**Errors:**
- `400` — Missing fields, insufficient balance, no vendors available, email not verified
- `400` with `suggestBridge: true` — Balance exists on wrong chain, user should bridge first

---

## GET /api/agent/p2p/orders

**Scope:** `wallet:read`

**Query params:**
- `limit` (optional, default 20, max 50)

**Response (200):**
```json
{
  "orders": [
    {
      "id": "uuid",
      "status": "completed",
      "token": "USDC",
      "cryptoAmount": 50.0,
      "fiatAmount": 79000.0,
      "fiatCurrency": "NGN",
      "rate": 1580.0,
      "chain": "arbitrum",
      "vendorName": "FastPay",
      "bankName": "GTBank",
      "createdAt": "2025-01-15T10:00:00Z",
      "completedAt": "2025-01-15T10:35:00Z"
    }
  ]
}
```

---

## GET /api/agent/p2p/orders/:id

**Scope:** `wallet:read`

**Response (200):**
```json
{
  "order": {
    "id": "uuid",
    "status": "fiat_sent",
    "token": "USDC",
    "cryptoAmount": 50.0,
    "fiatAmount": 79000.0,
    "fiatCurrency": "NGN",
    "rate": 1580.0,
    "chain": "arbitrum",
    "escrowTxHash": "0x...",
    "releaseTxHash": null,
    "vendorName": "FastPay",
    "bankName": "GTBank",
    "bankAccountNumber": "0123456789",
    "bankAccountName": "John Doe",
    "createdAt": "2025-01-15T10:00:00Z",
    "vendorAcceptedAt": "2025-01-15T10:02:00Z",
    "vendorPaidAt": "2025-01-15T10:15:00Z",
    "userConfirmedAt": null,
    "completedAt": null,
    "expiresAt": "2025-01-15T16:00:00Z"
  }
}
```

**Errors:**
- `404` — Order not found
- `403` — Order does not belong to you

---

## POST /api/agent/p2p/orders/:id/confirm

Confirm naira received. Releases escrow to vendor on-chain. **Irreversible.**

**Scope:** `payments:execute`

**Response (200):**
```json
{
  "success": true,
  "order": {
    "id": "uuid",
    "status": "completed",
    "releaseTxHash": "0x...",
    "completedAt": "2025-01-15T10:35:00Z"
  }
}
```

**Errors:**
- `400` — Order not in `fiat_sent` status

---

## POST /api/agent/p2p/orders/:id/dispute

Open a dispute. Cancels auto-release, admin investigates.

**Scope:** `payments:execute`

**Request:**
```json
{ "reason": "Vendor marked paid but naira not received" }
```

**Response (200):**
```json
{ "success": true, "orderId": "uuid", "status": "disputed" }
```

**Errors:**
- `400` — Order not in disputable state, or cooldown not elapsed (10 min after vendor acceptance)

---

## POST /api/agent/p2p/orders/:id/rate

Rate the vendor after a completed trade.

**Scope:** `wallet:read`

**Request:**
```json
{ "rating": 5, "comment": "Fast payment" }
```

**Response (200):**
```json
{ "success": true }
```

**Errors:**
- `400` — Invalid rating (must be 1-5), order not completed, or already rated

---

## P2P Order Statuses

| Status | Meaning |
|--------|---------|
| `escrow_locked` | Crypto locked, waiting for vendor to accept (3 min window) |
| `accepted` | Vendor accepted, will send naira (30 min window) |
| `fiat_sent` | Vendor says naira was sent, check your bank |
| `completed` | You confirmed receipt, escrow released to vendor |
| `disputed` | Dispute opened, admin reviewing |
| `cancelled` | Order cancelled or expired |
| `refunded` | Escrow returned to you |

---

## Auth Errors (all endpoints)

- `401` — `"No agent token provided"` — missing or malformed Authorization header
- `401` — `"Invalid or expired agent token"` — token not found, expired, or revoked
- `403` — `"Missing required scope: <scope>"` — token does not have the needed permission

## Token Scopes

| Scope | Grants |
|-------|--------|
| `wallet:read` | balances, wallet info, history, bank accounts, P2P orders, rate vendor |
| `contacts:read` | list contacts |
| `contacts:write` | add/delete contacts |
| `payments:prepare` | prepare (preview) a payment |
| `payments:execute` | confirm payment, create P2P sell order, confirm fiat, open dispute |

All scopes are granted by default when connecting via `/api/agent/connect`.
