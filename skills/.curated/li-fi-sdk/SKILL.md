---
name: li-fi-sdk
description: |
  TypeScript/JavaScript SDK for cross-chain and same-chain token swaps, bridging, and DeFi operations.
  
  USE THIS SKILL TO:
  - Swap tokens between different blockchains (e.g., "swap USDC on Ethereum to ETH on Arbitrum")
  - Bridge tokens to another chain (e.g., "transfer my ETH from mainnet to Base")
  - Swap tokens on the same chain with best DEX rates (e.g., "swap ETH to DAI on Polygon")
  - Get quotes or compare routes for token swaps across any chains
  - Execute 1-click DeFi workflows (zap into LP, bridge+swap+deposit, cross-chain yield entry)
  - Build a dApp, wallet, or frontend that supports multi-chain token operations
  - Create payment flows that accept any token and convert to a specific token
  - Build React, Next.js, Vue, or Node.js apps with cross-chain swap functionality
  - Handle cross-chain transaction lifecycle (status tracking, retries, refunds)
  - Find available bridges, DEXs, chains, or tokens for cross-chain operations
---

# LI.FI SDK Integration

The LI.FI SDK (`@lifi/sdk`) is a TypeScript/JavaScript toolkit for cross-chain and on-chain swaps and bridging. It provides complete functionality from obtaining routes/quotes to executing transactions across 30+ blockchain networks.

## Installation

```bash
# Using yarn
yarn add @lifi/sdk

# Using npm
npm install @lifi/sdk

# Using pnpm
pnpm add @lifi/sdk

# Using bun
bun add @lifi/sdk
```

## Quick Start

### 1. Configure the SDK

```typescript
import { createConfig } from '@lifi/sdk';

createConfig({
  integrator: 'YourAppName', // Required: identifies your application
});
```

### 2. Request a Quote

```typescript
import { getQuote } from '@lifi/sdk';

const quote = await getQuote({
  fromChain: 42161,      // Arbitrum
  toChain: 10,           // Optimism
  fromToken: '0xaf88d065e77c8cC2239327C5EDb3A432268e5831', // USDC on Arbitrum
  toToken: '0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1',   // DAI on Optimism
  fromAmount: '10000000', // 10 USDC (6 decimals)
  fromAddress: '0xYourWalletAddress',
});
```

### 3. Execute the Transfer

```typescript
import { executeRoute, convertQuoteToRoute } from '@lifi/sdk';

const route = convertQuoteToRoute(quote);

const executedRoute = await executeRoute(route, {
  updateRouteHook(updatedRoute) {
    console.log('Route updated:', updatedRoute);
  },
});
```

## Core Concepts

### Routes vs Quotes

- **`getQuote()`**: Returns single best option with transaction data ready. Use for simple transfers.
- **`getRoutes()`**: Returns multiple options for comparison. Use when presenting choices to users.

See [references/REFERENCE.md](references/REFERENCE.md) for chain IDs, token addresses, and parameter tables.

## SDK Configuration

### Basic Configuration

```typescript
import { createConfig } from '@lifi/sdk';

createConfig({
  integrator: 'YourAppName',
  apiKey: 'your-api-key', // Optional: for higher rate limits
});
```

### Advanced Configuration

```typescript
import { createConfig, ChainType } from '@lifi/sdk';

createConfig({
  integrator: 'YourAppName',
  apiKey: 'your-api-key',
  rpcUrls: {
    1: ['https://your-ethereum-rpc.com'],
    137: ['https://your-polygon-rpc.com'],
  },
  chains: {
    allow: [1, 10, 137, 42161], // Only allow specific chains
  },
  preloadChains: true, // Preload chain data for faster initial requests
});
```

## Requesting Routes and Quotes

### Get Multiple Routes

```typescript
import { getRoutes, RoutesRequest } from '@lifi/sdk';

const routesRequest: RoutesRequest = {
  fromChainId: 42161,
  toChainId: 10,
  fromTokenAddress: '0xaf88d065e77c8cC2239327C5EDb3A432268e5831',
  toTokenAddress: '0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1',
  fromAmount: '10000000',
  fromAddress: '0xYourAddress', // Optional for routes
  options: {
    slippage: 0.005,  // 0.5% slippage
    order: 'CHEAPEST', // or 'FASTEST'
  },
};

const result = await getRoutes(routesRequest);
const routes = result.routes;
```

### Get Single Best Quote

```typescript
import { getQuote, QuoteRequest } from '@lifi/sdk';

const quoteRequest: QuoteRequest = {
  fromChain: 42161,
  toChain: 10,
  fromToken: '0xaf88d065e77c8cC2239327C5EDb3A432268e5831',
  toToken: '0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1',
  fromAmount: '10000000',
  fromAddress: '0xYourAddress', // Required for quotes
  slippage: 0.005,
};

const quote = await getQuote(quoteRequest);
```

### Route Options

```typescript
const options = {
  slippage: 0.005,           // 0.5% slippage tolerance
  order: 'CHEAPEST',         // 'CHEAPEST' or 'FASTEST'
  maxPriceImpact: 0.3,       // Hide routes with >30% price impact
  allowSwitchChain: true,    // Allow 2-step routes
  integrator: 'YourApp',
  fee: 0.03,                 // 3% integrator fee (requires verification)
  
  // Bridge/exchange preferences
  bridges: {
    allow: ['stargate', 'hop'],    // Only use these bridges
    deny: ['multichain'],          // Never use these bridges
    prefer: ['stargate'],          // Prefer if available
  },
  exchanges: {
    allow: ['1inch', 'uniswap'],
    deny: ['sushiswap'],
  },
};
```

## Executing Transactions

### Basic Execution

```typescript
import { executeRoute } from '@lifi/sdk';

const executedRoute = await executeRoute(route, {
  updateRouteHook(updatedRoute) {
    // Called on every route state change
    console.log('Status:', updatedRoute.steps[0]?.execution?.status);
  },
});
```

### Execution with All Hooks

```typescript
import { executeRoute } from '@lifi/sdk';

const executedRoute = await executeRoute(route, {
  // Track route updates
  updateRouteHook(updatedRoute) {
    const step = updatedRoute.steps[0];
    const process = step?.execution?.process;
    const latestProcess = process?.[process.length - 1];
    
    console.log('Status:', latestProcess?.status);
    console.log('TX Hash:', latestProcess?.txHash);
  },
  
  // Handle exchange rate changes (important!)
  acceptExchangeRateUpdateHook(toToken, oldAmount, newAmount) {
    const oldValue = parseFloat(oldAmount);
    const newValue = parseFloat(newAmount);
    const percentChange = ((newValue - oldValue) / oldValue) * 100;
    
    // Accept if change is less than 2%
    if (Math.abs(percentChange) < 2) {
      return Promise.resolve(true);
    }
    // Prompt user for larger changes
    return promptUserToAccept(percentChange);
  },
  
  // Handle chain switching (for 2-step routes)
  async switchChainHook(chainId) {
    await walletClient.switchChain({ id: chainId });
    return walletClient;
  },
  
  // Modify transaction before sending (advanced)
  async updateTransactionRequestHook(txRequest) {
    return {
      ...txRequest,
      gas: txRequest.gas ? BigInt(txRequest.gas) * 120n / 100n : undefined,
    };
  },
});
```

### Execute a Quote

```typescript
import { getQuote, convertQuoteToRoute, executeRoute } from '@lifi/sdk';

// Get quote
const quote = await getQuote(quoteRequest);

// Convert to route for execution
const route = convertQuoteToRoute(quote);

// Execute
const result = await executeRoute(route);
```

## Managing Execution Lifecycle

### Resume Interrupted Execution

```typescript
import { resumeRoute } from '@lifi/sdk';

// Resume from the last saved route state
const resumedRoute = await resumeRoute(savedRoute, {
  updateRouteHook(route) {
    console.log('Resumed execution:', route);
  },
});
```

### Background Execution

```typescript
import { executeRoute, updateRouteExecution } from '@lifi/sdk';

// Start execution
const routePromise = executeRoute(route, {
  updateRouteHook(route) {
    saveRouteState(route); // Persist state
  },
});

// Move to background (e.g., user navigates away)
updateRouteExecution(route, { executeInBackground: true });

// Later: resume in foreground
const resumedRoute = await resumeRoute(savedRoute, {
  executeInBackground: false,
});
```

### Stop Execution

```typescript
import { stopRouteExecution } from '@lifi/sdk';

// Stop execution (already-sent transactions will complete on-chain)
const stoppedRoute = stopRouteExecution(route);
```

### Get Active Routes

```typescript
import { getActiveRoutes, getActiveRoute } from '@lifi/sdk';

// Get all active routes
const activeRoutes = getActiveRoutes();

// Get specific active route
const activeRoute = getActiveRoute(routeId);
```

## Chain and Token Discovery

### Get Available Chains

```typescript
import { getChains, ChainType } from '@lifi/sdk';

// Get all chains
const allChains = await getChains();

// Get only EVM chains
const evmChains = await getChains({ chainTypes: [ChainType.EVM] });
```

### Get Available Tokens

```typescript
import { getTokens, getToken } from '@lifi/sdk';

// Get all tokens for a chain
const tokens = await getTokens({ chains: [1, 137] });

// Get specific token
const usdc = await getToken(1, '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48');
```

### Get Available Tools (Bridges/DEXs)

```typescript
import { getTools } from '@lifi/sdk';

const tools = await getTools();
console.log('Bridges:', tools.bridges);
console.log('Exchanges:', tools.exchanges);
```

### Get Connections

```typescript
import { getConnections } from '@lifi/sdk';

// Find all possible routes from ETH on Ethereum
const connections = await getConnections({
  fromChain: 1,
  fromToken: '0x0000000000000000000000000000000000000000', // Native ETH
});
```

## Multi-VM Provider Setup

### EVM Provider (Viem)

```typescript
import { createConfig, EVM } from '@lifi/sdk';
import { createWalletClient, http } from 'viem';
import { mainnet } from 'viem/chains';

const walletClient = createWalletClient({
  chain: mainnet,
  transport: http(),
});

createConfig({
  integrator: 'YourApp',
  providers: [
    EVM({ getWalletClient: () => Promise.resolve(walletClient) }),
  ],
});
```

### Solana Provider

```typescript
import { createConfig, Solana } from '@lifi/sdk';

createConfig({
  integrator: 'YourApp',
  providers: [
    Solana({ getWalletAdapter: () => Promise.resolve(walletAdapter) }),
  ],
});
```

## Contract Calls (Composer)

Execute contract calls on the destination chain after bridging:

```typescript
import { getContractCallsQuote } from '@lifi/sdk';

const contractCallQuote = await getContractCallsQuote({
  fromAddress: '0xYourAddress',
  fromChain: 10,      // Optimism
  fromToken: '0x0000000000000000000000000000000000000000',
  toAmount: '8500000000000',
  toChain: 8453,      // Base
  toToken: '0x0000000000000000000000000000000000000000',
  contractCalls: [{
    fromAmount: '8500000000000',
    fromTokenAddress: '0x0000000000000000000000000000000000000000',
    toContractAddress: '0xTargetContract',
    toContractCallData: '0x...', // Encoded function call
    toContractGasLimit: '210000',
  }],
});
```

## Error Handling

```typescript
import { executeRoute } from '@lifi/sdk';

try {
  const result = await executeRoute(route, {
    acceptExchangeRateUpdateHook: () => Promise.resolve(true),
  });
} catch (error) {
  if (error.message.includes('Exchange rate has changed')) {
    // Handle rate change rejection
  } else if (error.message.includes('insufficient funds')) {
    // Handle balance issues
  } else if (error.message.includes('user rejected')) {
    // Handle user cancellation
  } else {
    // Handle other errors
    console.error('Execution failed:', error);
  }
}
```

## Best Practices

1. **Always implement `acceptExchangeRateUpdateHook`** - Exchange rates can change during execution. Without this hook, execution fails on rate changes.

2. **Persist route state** - Use `updateRouteHook` to save route state for recovery after page refreshes or app restarts.

3. **Handle chain switching** - For cross-chain routes, implement `switchChainHook` to handle wallet chain switches.

4. **Use appropriate slippage** - Default 0.5% (0.005) works for most cases. Increase for volatile tokens or low-liquidity pairs.

5. **Set integrator name** - Always configure `integrator` for analytics and potential monetization.

6. **Check token allowances** - The SDK handles allowances automatically, but you may want to show approval UI to users.

7. **Monitor gas prices** - Use `updateTransactionRequestHook` to adjust gas if needed.

See [references/REFERENCE.md](references/REFERENCE.md) for detailed parameter tables and TypeScript interfaces.
