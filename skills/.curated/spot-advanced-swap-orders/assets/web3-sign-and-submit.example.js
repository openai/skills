// Example only. This flow uses eth_signTypedData_v4 via an injected provider,
// but any framework that signs the same prepared.typedData payload is valid.

import Web3 from "web3";

const DEPOSIT_DATA = "0xd0e30db0";
const ERC20_ABI = [
  {
    constant: true,
    inputs: [
      { name: "owner", type: "address" },
      { name: "spender", type: "address" },
    ],
    name: "allowance",
    outputs: [{ name: "", type: "uint256" }],
    type: "function",
  },
];

export async function approveSignAndSubmitOrder({
  prepared,
  account,
  provider = window.ethereum,
  wrappedNative,
  nativeInputAmount,
  sendApproval = true,
}) {
  const web3 = new Web3(provider);
  const normalizedAccount = account.toLowerCase();
  const expectedSigner = prepared.signing.signer.toLowerCase();

  // The EIP-712 signer must be the same address that created the order.
  if (normalizedAccount !== expectedSigner) {
    throw new Error(
      `signer mismatch: expected ${prepared.signing.signer}, got ${account}`
    );
  }

  // Native input is not supported by the order itself.
  // If the input starts as the chain's native asset, wrap it to WNATIVE first.
  if (
    nativeInputAmount != null &&
    nativeInputAmount !== "0" &&
    nativeInputAmount !== "0x0"
  ) {
    if (!wrappedNative) {
      throw new Error("wrappedNative is required when nativeInputAmount is set");
    }

    await web3.eth.sendTransaction({
      from: account,
      to: wrappedNative,
      data: DEPOSIT_DATA,
      value: nativeInputAmount,
    });
  }

  if (prepared.approval && sendApproval) {
    // The skill helper is RPC-agnostic, so the caller should use its own
    // provider access to avoid resending the same infinite approval.
    const token = new web3.eth.Contract(ERC20_ABI, prepared.approval.tx.to);
    const allowance = BigInt(
      await token.methods
        .allowance(account, prepared.approval.spender)
        .call()
    );

    if (allowance < BigInt(prepared.approval.amount)) {
      await web3.eth.sendTransaction({
        from: account,
        to: prepared.approval.tx.to,
        data: prepared.approval.tx.data,
        value: prepared.approval.tx.value,
      });
    }
  }

  // This example uses eth_signTypedData_v4, but any equivalent EIP-712 signer works.
  const signature = await provider.request({
    method: "eth_signTypedData_v4",
    params: [account, JSON.stringify(prepared.typedData)],
  });

  // Submit the order payload plus the returned signature to the relay endpoint.
  const response = await fetch(prepared.submit.url, {
    method: "POST",
    headers: {
      "content-type": "application/json",
    },
    body: JSON.stringify({
      ...prepared.submit.body,
      signature,
    }),
  });

  const text = await response.text();
  let body;

  try {
    body = JSON.parse(text);
  } catch {
    body = text;
  }

  return {
    ok: response.ok,
    status: response.status,
    signature,
    body,
  };
}
