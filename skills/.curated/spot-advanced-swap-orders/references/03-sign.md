# Sign And Submit

1. Sign `prepared.typedData` with any EIP-712-capable wallet or library. The signer must equal `swapper`. `eth_signTypedData_v4` is only one example.
2. Submit with `--prepared <prepared.json|->` and exactly one signature mode: `--signature <0x...|json>`, `--signature-file <sig.txt|sig.json|->`, or `--r <0x...> --s <0x...> --v <0x...>`.
3. The helper accepts a full 65-byte signature, a JSON string, or JSON/object `r/s/v`.
4. Cancel trustlessly onchain by calling `RePermit.cancel([digest])` as the swapper for the signed RePermit digest.
