# Order Patterns

1. Market swap: `input.amount = input.maxAmount`, `output.limit = 0`.
2. Limit order: `input.amount = input.maxAmount`, `output.limit > 0`.
3. Stop-loss or take-profit: set `output.triggerLower` for stop-loss and/or `output.triggerUpper` for take-profit.
4. Delayed order: set future `start`.
5. Chunked or TWAP-style: set `input.amount < input.maxAmount`.
6. Time-spaced chunked order: set `epoch > 0`. For example, `epoch = 60` means one chunk can fill once anywhere inside each 60-second epoch window.
7. `N chunks`: use one TWAP order instead of manually submitting `N` separate orders. Use `input.maxAmount` as the requested total amount, set `input.amount = floor(total / N)`, and accept any rounded-down remainder as dust.
8. If timing is omitted for a chunked or TWAP order, `epoch` defaults to `60`. Single orders default to `0`.
9. Native output or back to native exposure: set `output.token = 0x0000000000000000000000000000000000000000`.
10. Best execution and oracle protection apply regardless of `output.limit`.
