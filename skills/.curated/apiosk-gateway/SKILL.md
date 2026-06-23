---
name: apiosk-gateway
description: Use Apiosk pay-per-call APIs through an x402 payment flow (HTTP 402 + USDC on Base) without API keys. Trigger this skill when Codex needs to call Apiosk endpoints, handle or explain Payment Required responses, estimate micropayment cost per request, choose an endpoint from the Apiosk catalog, or integrate Apiosk gateway calls in scripts/apps.
---

# Apiosk Skill - Pay-per-call API Gateway

Access APIs by paying per request with USDC micropayments on Base blockchain.
Use `https://gateway.apiosk.com` as the base URL.

## Core Function

Apply the x402 protocol flow:
1. Call an Apiosk endpoint.
2. If the gateway returns `402 Payment Required`, read payment details.
3. Submit the USDC payment on Base.
4. Retry or continue the request with payment proof as required by the gateway.
5. Receive the proxied upstream API response.

Treat `402` as a normal step in the request lifecycle, not as a terminal error.

## Available APIs

- Weather: Current conditions and forecasts
- Crypto prices: Real-time token and coin prices
- News headlines: Latest news by topic or region
- Company data: Business information lookup
- Geocoding: Address to coordinates conversion
- Code execution: Run code in a sandboxed environment
- PDF generation: Convert HTML/Markdown to PDF
- Screenshots: Capture website screenshots
- File conversion: Convert between file formats
- Image processing: Resize, crop, and optimize images

## Usage Examples

```bash
# Weather for Amsterdam
curl "https://gateway.apiosk.com/weather?city=Amsterdam"

# Bitcoin price
curl "https://gateway.apiosk.com/crypto/price?symbol=BTC"

# Company lookup
curl "https://gateway.apiosk.com/company?domain=apple.com"
```

## Payment Details

- Cost: typically `$0.001` to `$0.01` per API call (depends on endpoint).
- Currency: USDC on Base.
- Settlement: instant and on-chain.
- Billing model: no subscription, pay per request.

## Integration Details

- Gateway URL: `https://gateway.apiosk.com`
- Protocol: x402 (`HTTP 402` + crypto payment)
- Chain: Base (Ethereum L2)
- Token: `$APIOSK` can be used for optional discounts

## Provider Notes

Use these details when users ask about publishing APIs on Apiosk:
- Revenue share: usually `90-95%` to API providers.
- Settlement: instant USDC.
- Payments: no separate payment processor setup.
- Distribution: globally accessible through one gateway.

## Links

- Website: `https://apiosk.com`
- Documentation: `https://docs.apiosk.com`
- GitHub: `https://github.com/apiosk`
- Token note: `$APIOSK` on Base (contract example provided by user: `0xb98251...`)
