# Quickstart

1. Required fields: `chainId`, `swapper`, `input.token`, `input.amount`, `output.token`.
2. Choose the intended order shape before preparing: market, limit, stop-loss, take-profit, delayed-start, or chunked/TWAP.
3. Prepare the order with the helper.
4. If approval is needed, send `prepared.approval.tx` to approve `RePermit`.
5. The skill helper does not read allowance onchain. The calling agent or app should use its own RPC or provider access to compare the current ERC-20 allowance against `prepared.approval.amount`, send that infinite approval only when allowance is lower, and then leave the infinite approval in place with no reset.
6. Sign `prepared.typedData` as the `swapper`.
7. Submit the signed order.
8. Query the order by `swapper` or `hash`.
9. Watch until terminal state. Default polling is every 5 seconds, timeout `0` means no timeout, and transient network errors are retried automatically.
10. When measuring a fill onchain, sum both transfers to the swapper: the main fill and the surplus refund. Measuring only the main fill undercounts actual output by up to the slippage tolerance.
