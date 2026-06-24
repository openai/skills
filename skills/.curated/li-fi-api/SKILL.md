---
name: li-fi-api
description: |
  REST API for cross-chain and same-chain token swaps, bridging, and DeFi operations.
  
  USE THIS SKILL WHEN USER WANTS TO:
  - Swap tokens between different blockchains (e.g., "swap USDC on Ethereum to ETH on Arbitrum")
  - Bridge tokens to another chain (e.g., "move my ETH from mainnet to Optimism")
  - Swap tokens on the same chain with best rates (e.g., "swap ETH to USDC on Polygon")
  - Find the best route or quote for a token swap across chains
  - Execute DeFi operations across chains (zap, bridge+swap+deposit, yield farming entry)
  - Build multi-chain payment flows (accept any token, settle in specific token)
  - Check supported chains, tokens, or bridges for cross-chain transfers
  - Track status of a cross-chain transaction
  - Build backend services (Python, Go, Rust, etc.) that need cross-chain swaps
  - Integrate cross-chain functionality via HTTP/REST (not JavaScript SDK)
---

# LI.FI REST API Integration

The LI.FI REST API provides direct HTTP access to cross-chain swap and bridge functionality. Use this API when building backend services, working with non-JavaScript languages, or needing fine-grained control over cross-chain operations.

## Base URL

```
https://li.quest/v1
```

## Authentication

API key is **optional** but recommended for higher rate limits.

```bash
# Without API key (lower rate limits)
curl "https://li.quest/v1/chains"

# With API key (higher rate limits)
curl "https://li.quest/v1/chains" \
  -H "x-lifi-api-key: YOUR_API_KEY"
```

**Important**: Never expose your API key in client-side code. Use it only in server-side applications.

## Rate Limits

| Tier | Limit |
|------|-------|
| Without API key | Per IP address |
| With API key | Per API key |

Request an API key from LI.FI for production use with higher limits.

## Quick Start

### 1. Get a Quote

```bash
curl "https://li.quest/v1/quote?\
fromChain=42161&\
toChain=10&\
fromToken=0xaf88d065e77c8cC2239327C5EDb3A432268e5831&\
toToken=0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1&\
fromAmount=10000000&\
fromAddress=0xYourAddress&\
slippage=0.005"
```

### 2. Execute the Transaction

Use the `transactionRequest` from the quote response to send the transaction via your wallet or web3 library.

### 3. Track Status

```bash
curl "https://li.quest/v1/status?\
txHash=0xYourTxHash&\
fromChain=42161&\
toChain=10&\
bridge=stargate"
```

## Core Endpoints

### GET /quote

Get a single-step quote with transaction data ready for execution.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `fromChain` | number | Yes | Source chain ID |
| `toChain` | number | Yes | Destination chain ID |
| `fromToken` | string | Yes | Source token address |
| `toToken` | string | Yes | Destination token address |
| `fromAmount` | string | Yes | Amount in smallest unit |
| `fromAddress` | string | Yes | Sender wallet address |
| `toAddress` | string | No | Recipient address |
| `slippage` | number | No | Slippage tolerance (0.005 = 0.5%) |
| `integrator` | string | No | Your integrator ID |
| `allowBridges` | string[] | No | Allowed bridges (or `all`, `none`, `default`) |
| `denyBridges` | string[] | No | Denied bridges |
| `preferBridges` | string[] | No | Preferred bridges |
| `allowExchanges` | string[] | No | Allowed exchanges (or `all`, `none`, `default`) |
| `denyExchanges` | string[] | No | Denied exchanges |
| `preferExchanges` | string[] | No | Preferred exchanges |
| `allowDestinationCall` | boolean | No | Allow contract calls on destination (default: true) |
| `order` | string | No | Route preference: `FASTEST` or `CHEAPEST` |
| `fee` | number | No | Integrator fee (0.02 = 2%, max <100%) |
| `referrer` | string | No | Referrer tracking information |
| `fromAmountForGas` | string | No | Amount to convert to gas on destination |
| `maxPriceImpact` | number | No | Max price impact threshold (0.1 = 10%, default: 10%) |
| `skipSimulation` | boolean | No | Skip TX simulation for faster response |
| `swapStepTimingStrategies` | string[] | No | Timing strategy for swap rates |
| `routeTimingStrategies` | string[] | No | Timing strategy for route selection |

**Example Request:**

```bash
curl "https://li.quest/v1/quote?\
fromChain=1&\
toChain=137&\
fromToken=0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48&\
toToken=0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174&\
fromAmount=1000000000&\
fromAddress=0x552008c0f6870c2f77e5cC1d2eb9bdff03e30Ea0&\
slippage=0.005"
```

The response includes `transactionRequest` with all data needed to execute the swap. See [references/REFERENCE.md](references/REFERENCE.md) for complete response schema.

### POST /advanced/routes

Get multiple route options for comparison. Returns routes without transaction data (use `/advanced/stepTransaction` to get TX data for a specific step).

**Request Body:**

```json
{
  "fromChainId": 42161,
  "toChainId": 10,
  "fromTokenAddress": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
  "toTokenAddress": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
  "fromAmount": "10000000",
  "fromAddress": "0xYourAddress",
  "options": {
    "integrator": "YourAppName",
    "slippage": 0.005,
    "order": "CHEAPEST",
    "bridges": {
      "allow": ["stargate", "hop", "across"]
    },
    "exchanges": {
      "allow": ["1inch", "uniswap"]
    },
    "allowSwitchChain": true,
    "maxPriceImpact": 0.1
  }
}
```

**Example Request:**

```bash
curl -X POST "https://li.quest/v1/advanced/routes" \
  -H "Content-Type: application/json" \
  -d '{
    "fromChainId": 42161,
    "toChainId": 10,
    "fromTokenAddress": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
    "toTokenAddress": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
    "fromAmount": "10000000",
    "options": {
      "slippage": 0.005,
      "integrator": "YourApp"
    }
  }'
```

Returns array of routes sorted by `order` preference. Each route contains `steps` but no `transactionRequest` - use `/advanced/stepTransaction` to get TX data.

### POST /advanced/stepTransaction

Populate a step (from `/advanced/routes`) with transaction data. Use this after selecting a route to get the actual transaction to execute.

**Request Body:** Send the full `Step` object from a route.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `skipSimulation` | boolean | No | Skip TX simulation for faster response |

**Example:**

```bash
curl -X POST "https://li.quest/v1/advanced/stepTransaction" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "step-id",
    "type": "cross",
    "tool": "stargate",
    "action": {...},
    "estimate": {...}
  }'
```

**Response:** Returns the Step object with `transactionRequest` populated.

### GET /status

Track transaction status across chains. Can query by sending TX hash, receiving TX hash, or transactionId.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `txHash` | string | Yes | Transaction hash (sending, receiving, or transactionId) |
| `fromChain` | number | No | Source chain ID (speeds up request) |
| `toChain` | number | No | Destination chain ID |
| `bridge` | string | No | Bridge tool name |

For same-chain swaps, set `fromChain` and `toChain` to the same value.

**Example Request:**

```bash
curl "https://li.quest/v1/status?txHash=0x123abc..."
```

**Response includes:** `transactionId`, `sending` (txHash, amount, chainId), `receiving` (txHash, amount, chainId), `status`, `substatus`, `lifiExplorerLink`.

**Status Values:** `NOT_FOUND`, `INVALID`, `PENDING`, `DONE`, `FAILED`

Poll until status is `DONE` or `FAILED`. See [references/REFERENCE.md](references/REFERENCE.md) for complete substatus values.

### GET /chains

Get all supported chains.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chainTypes` | string | No | Filter by chain types: `EVM`, `SVM` |

```bash
curl "https://li.quest/v1/chains"
curl "https://li.quest/v1/chains?chainTypes=EVM,SVM"
```

### GET /tokens

Get tokens for specified chains.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chains` | string | No | Comma-separated chain IDs or keys (e.g., `POL,DAI`) |
| `chainTypes` | string | No | Filter by chain types: `EVM`, `SVM` |
| `minPriceUSD` | number | No | Min token price filter (default: 0.0001 USD) |

```bash
curl "https://li.quest/v1/tokens?chains=1,137,42161"
```

### GET /token

Get information about a specific token.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chain` | string | Yes | Chain ID or key (e.g., `POL` or `137`) |
| `token` | string | Yes | Token address or symbol (e.g., `DAI`) |

```bash
curl "https://li.quest/v1/token?chain=POL&token=DAI"
```

### GET /tools

Get available bridges and exchanges. Use this to discover valid tool keys for filtering quotes.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chains` | string | No | Filter by chain IDs |

```bash
curl "https://li.quest/v1/tools"
curl "https://li.quest/v1/tools?chains=1,137"
```

Returns `bridges` and `exchanges` arrays with `key`, `name`, and `supportedChains`. Use these keys in `allowBridges`, `denyBridges`, `allowExchanges`, etc.

**Special values:** `all`, `none`, `default`, `[]`

### GET /connections

Get available token pair connections. At least one filter (chain, token, bridge, or exchange) is required.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `fromChain` | string | No | Source chain ID or key |
| `toChain` | string | No | Destination chain ID or key |
| `fromToken` | string | No | Source token address or symbol |
| `toToken` | string | No | Destination token address or symbol |
| `chainTypes` | string | No | Filter by chain types: `EVM,SVM` |
| `allowBridges` | string[] | No | Allowed bridges |
| `denyBridges` | string[] | No | Denied bridges |
| `preferBridges` | string[] | No | Preferred bridges |
| `allowExchanges` | string[] | No | Allowed exchanges |
| `denyExchanges` | string[] | No | Denied exchanges |
| `preferExchanges` | string[] | No | Preferred exchanges |
| `allowSwitchChain` | boolean | No | Include routes requiring chain switch (default: true) |
| `allowDestinationCall` | boolean | No | Include routes with destination calls (default: true) |

```bash
curl "https://li.quest/v1/connections?\
fromChain=POL&\
fromToken=DAI"
```

### POST /quote/contractCalls

Get a quote for bridging tokens and performing multiple contract calls on the destination chain. This enables 1-click DeFi workflows like bridge + swap + deposit.

**Request Body:**

```json
{
  "fromChain": 10,
  "fromToken": "0x4200000000000000000000000000000000000042",
  "fromAddress": "0x552008c0f6870c2f77e5cC1d2eb9bdff03e30Ea0",
  "toChain": 1,
  "toToken": "ETH",
  "toAmount": "100000000000001",
  "integrator": "YourAppName",
  "contractCalls": [
    {
      "fromAmount": "100000000000001",
      "fromTokenAddress": "0x0000000000000000000000000000000000000000",
      "toTokenAddress": "0xae7ab96520de3a18e5e111b5eaab095312d7fe84",
      "toContractAddress": "0xae7ab96520de3a18e5e111b5eaab095312d7fe84",
      "toContractCallData": "0x",
      "toContractGasLimit": "110000"
    },
    {
      "fromAmount": "100000000000000",
      "fromTokenAddress": "0xae7ab96520de3a18e5e111b5eaab095312d7fe84",
      "toTokenAddress": "0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0",
      "toContractAddress": "0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0",
      "toFallbackAddress": "0x552008c0f6870c2f77e5cC1d2eb9bdff03e30Ea0",
      "toContractCallData": "0xea598cb000000000000000000000000000000000000000000000000000005af3107a4000",
      "toContractGasLimit": "100000"
    }
  ]
}
```

## Integration Examples

### Python

```python
import requests

BASE_URL = "https://li.quest/v1"

def get_quote(from_chain, to_chain, from_token, to_token, amount, address):
    response = requests.get(f"{BASE_URL}/quote", params={
        "fromChain": from_chain,
        "toChain": to_chain,
        "fromToken": from_token,
        "toToken": to_token,
        "fromAmount": amount,
        "fromAddress": address,
        "slippage": 0.005
    })
    return response.json()

def get_status(tx_hash, from_chain, to_chain, bridge):
    response = requests.get(f"{BASE_URL}/status", params={
        "txHash": tx_hash,
        "fromChain": from_chain,
        "toChain": to_chain,
        "bridge": bridge
    })
    return response.json()

# Example usage
quote = get_quote(
    from_chain=42161,
    to_chain=10,
    from_token="0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
    to_token="0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
    amount="10000000",
    address="0xYourAddress"
)

print(f"Estimated output: {quote['estimate']['toAmount']}")
print(f"Gas cost: {quote['estimate']['gasCosts']}")
```

### Node.js (fetch)

```javascript
const BASE_URL = 'https://li.quest/v1';

async function getQuote(params) {
  const searchParams = new URLSearchParams(params);
  const response = await fetch(`${BASE_URL}/quote?${searchParams}`);
  return response.json();
}

async function getRoutes(body) {
  const response = await fetch(`${BASE_URL}/routes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return response.json();
}

async function pollStatus(txHash, fromChain, toChain, bridge) {
  const params = new URLSearchParams({ txHash, fromChain, toChain, bridge });
  
  while (true) {
    const response = await fetch(`${BASE_URL}/status?${params}`);
    const data = await response.json();
    
    if (data.status === 'DONE' || data.status === 'FAILED') {
      return data;
    }
    
    await new Promise(resolve => setTimeout(resolve, 5000));
  }
}

// Example usage
const quote = await getQuote({
  fromChain: 42161,
  toChain: 10,
  fromToken: '0xaf88d065e77c8cC2239327C5EDb3A432268e5831',
  toToken: '0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1',
  fromAmount: '10000000',
  fromAddress: '0xYourAddress',
  slippage: 0.005,
});
```

## Error Handling

| HTTP Status | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad request - check parameters |
| 429 | Rate limit exceeded - wait or use API key |
| 500 | Internal error - retry |

See [references/REFERENCE.md](references/REFERENCE.md) for complete error codes and response schemas.

## Best Practices

1. **Always specify slippage** - Default is conservative. Adjust based on token volatility.

2. **Poll status endpoint** - For cross-chain transfers, poll every 5-10 seconds until `DONE` or `FAILED`.

3. **Handle rate limits** - Implement exponential backoff for 429 responses.

4. **Cache chain/token data** - `/chains` and `/tokens` responses change infrequently.

5. **Use integrator parameter** - Always include `integrator` for analytics and potential monetization.

6. **Validate addresses** - Ensure token addresses match the specified chain.

7. **Handle gas estimation** - The API provides gas estimates, but actual costs may vary.

See [references/REFERENCE.md](references/REFERENCE.md) for complete endpoint documentation and response schemas.