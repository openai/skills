# Params

Use this file for field semantics, defaults, units, and validation.

1. Required: `chainId`, `swapper`, `input.token`, `input.amount`, `output.token`.
2. Optional: `input.maxAmount`, `nonce`, `start`, `deadline`, `epoch`, `slippage`, `output.limit`, `output.triggerLower`, `output.triggerUpper`, `output.recipient`.
3. `input.amount` is the fixed per-chunk size. `input.maxAmount` is the total requested size. If omitted, it defaults to `input.amount`. If it is not divisible by `input.amount`, the helper rounds it down to a whole number of chunks.
4. `output.limit`, `output.triggerLower`, and `output.triggerUpper` are output-token amounts per chunk, encoded in the output token's decimals.
5. Future `start` delays the first fill. `epoch` is the delay between chunks, but it is not exact: each chunk can fill anywhere inside its epoch window, only once. Large `epoch` is not a delayed order by itself.
6. Chunked orders should use `epoch > 0`; with `epoch = 0`, only the first chunk can fill.
7. Defaults:
   - `input.maxAmount = input.amount`
   - `nonce = now`
   - `start = now`
   - `epoch = 0` for single orders, `60` for chunked orders
   - `deadline = start + 300 + chunkCount * epoch`
   - `slippage = 500`
   - `output.limit = 0`
   - `output.recipient = swapper`
8. Higher slippage is still protected by oracle pricing and offchain executors.
9. `output.recipient` is dangerous to change away from `swapper`.
10. Native input is not supported. Wrap to WNATIVE first. Native output, including "back to native" orders, is supported directly with `output.token = 0x0000000000000000000000000000000000000000`.
11. Example:

```json
{
  "chainId": 42161,
  "swapper": "0x1111111111111111111111111111111111111111",
  "input": {
    "token": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
    "amount": "1000000"
  },
  "output": {
    "token": "0x82af49447d8a07e3bd95bd0d56f35241523fbab1",
    "limit": "0"
  },
  "epoch": 3600
}
```
