#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import {
  clusterApiUrl,
  Connection,
  Keypair,
  LAMPORTS_PER_SOL,
  PublicKey,
  sendAndConfirmTransaction,
  SystemProgram,
  Transaction,
} from "@solana/web3.js";
import {
  createAssociatedTokenAccountInstruction,
  createTransferInstruction,
  getAccount,
  getAssociatedTokenAddress,
  getMint,
} from "@solana/spl-token";
import bs58 from "bs58";

const DEFAULT_RPC = clusterApiUrl("devnet");

function parseArgs(argv) {
  const positional = [];
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const current = argv[i];
    if (!current.startsWith("--")) {
      positional.push(current);
      continue;
    }

    const key = current.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      args[key] = true;
      continue;
    }

    args[key] = next;
    i++;
  }
  args._ = positional;
  return args;
}

function arg(args, ...names) {
  for (const name of names) {
    if (args[name] !== undefined) {
      return args[name];
    }
  }
  return undefined;
}

function isFlagTruthy(value) {
  if (typeof value === "boolean") return value;
  if (typeof value === "string") {
    return ["1", "true", "yes", "on"].includes(value.toLowerCase());
  }
  return false;
}

function printResult(payload) {
  console.log(JSON.stringify(payload, null, 2));
}

function resolveRpcUrl(args) {
  return (
    arg(args, "rpc-url", "rpcUrl", "rpc_url") ||
    process.env.SOLANA_RPC_URL ||
    process.env.RPC_URL ||
    DEFAULT_RPC
  );
}

function isLikelyFile(value) {
  if (!value) return false;
  return fs.existsSync(value);
}

function normalizeSource(rawSource) {
  if (!rawSource) return undefined;
  const trimmed = String(rawSource).trim();
  if (!trimmed) return undefined;
  if (isLikelyFile(trimmed)) {
    return fs.readFileSync(trimmed, "utf8").trim();
  }
  return trimmed;
}

function loadSecretKeyBytes(rawInput) {
  const text = normalizeSource(rawInput);
  if (!text) {
    throw new Error("No private key source provided");
  }

  if (text.startsWith("[")) {
    const parsed = JSON.parse(text);
    if (!Array.isArray(parsed) || parsed.length !== 64) {
      throw new Error("Invalid JSON secret key array; expected length 64");
    }
    return new Uint8Array(parsed);
  }

  const decoded = bs58.decode(text);
  if (decoded.length !== 64) {
    throw new Error(
      `Invalid secret key length ${decoded.length}. Expected base58 secret key with 64 bytes.`,
    );
  }
  return decoded;
}

function loadKeypair(args) {
  const source =
    arg(args, "wallet", "private-key", "private_key", "seed", "secret", "secret-key", "secret_key") ||
    process.env.SOLANA_PRIVATE_KEY ||
    process.env.PRIVATE_KEY;
  return Keypair.fromSecretKey(loadSecretKeyBytes(source));
}

function getPublicKey(text, fallbackLabel) {
  try {
    return new PublicKey(text);
  } catch (error) {
    throw new Error(`Invalid ${fallbackLabel}: ${String(error.message || error)}`);
  }
}

function requireAmount(value, label = "amount") {
  const parsed = Number(value);
  if (!Number.isFinite(parsed) || parsed <= 0) {
    throw new Error(`${label} must be a positive number`);
  }
  return parsed;
}

function clusterFromRpc(rpcUrl) {
  if (!rpcUrl) return "custom";
  const lowercase = rpcUrl.toLowerCase();
  if (lowercase.includes("mainnet") || lowercase.includes("mainnet-beta")) return "mainnet";
  if (lowercase.includes("testnet")) return "testnet";
  if (lowercase.includes("devnet")) return "devnet";
  return "custom";
}

async function getWalletBalance(connection, walletAddress, tokenMint) {
  const publicKey = getPublicKey(walletAddress, "wallet");
  if (!tokenMint) {
    const lamports = await connection.getBalance(publicKey);
    return lamports / LAMPORTS_PER_SOL;
  }

  const mint = getPublicKey(tokenMint, "token mint");
  const tokenAccounts = await connection.getTokenAccountsByOwner(publicKey, {
    mint,
  });
  if (tokenAccounts.value.length === 0) return 0;

  const parsedAccount = await connection.getParsedAccountInfo(
    tokenAccounts.value[0].pubkey,
  );
  const tokenData = parsedAccount.value?.data;
  const parsedAmount = tokenData?.parsed?.info?.tokenAmount?.uiAmount;
  return Number(parsedAmount || 0);
}

async function transferNative(connection, from, to, amount) {
  const instruction = SystemProgram.transfer({
    fromPubkey: from.publicKey,
    toPubkey: to,
    lamports: amount * LAMPORTS_PER_SOL,
  });
  const tx = new Transaction().add(instruction);
  return await sendAndConfirmTransaction(connection, tx, [from]);
}

async function transferSpl(connection, from, to, amount, mintAddress) {
  const mint = getPublicKey(mintAddress, "token mint");
  const fromAta = await getAssociatedTokenAddress(mint, from.publicKey);
  const toAta = await getAssociatedTokenAddress(mint, to);

  const tx = new Transaction();
  try {
    await getAccount(connection, toAta);
  } catch (error) {
    tx.add(
      createAssociatedTokenAccountInstruction(from.publicKey, toAta, to, mint),
    );
  }

  const mintInfo = await getMint(connection, mint);
  const mintDecimals = mintInfo.decimals;
  const converted = BigInt(Math.round(amount * Math.pow(10, mintDecimals)));
  if (converted <= 0) {
    throw new Error("Token amount rounds to zero for this mint precision");
  }

  tx.add(
    createTransferInstruction(
      fromAta,
      toAta,
      from.publicKey,
      converted,
    ),
  );

  return await sendAndConfirmTransaction(connection, tx, [from]);
}

function saveWalletSecret(filePath, keypair, format) {
  const normalized = path.resolve(filePath);
  let payload;
  if (format === "json-array") {
    payload = JSON.stringify(Array.from(keypair.secretKey));
  } else {
    payload = bs58.encode(keypair.secretKey);
  }

  fs.writeFileSync(normalized, `${payload}\n`, "utf8");
  return normalized;
}

async function cmdCreateWallet(args) {
  const keypair = Keypair.generate();
  const output = {
    command: "create-wallet",
    publicKey: keypair.publicKey.toBase58(),
    secretKeyBase58: bs58.encode(keypair.secretKey),
    secretLength: keypair.secretKey.length,
  };

  const savePath = arg(args, "save");
  if (savePath) {
    const format = arg(args, "save-format", "format") || "base58";
    const normalizedFormat = String(format).toLowerCase();
    output.savedTo = saveWalletSecret(savePath, keypair, normalizedFormat);
    output.saveFormat = normalizedFormat;
  }

  printResult(output);
}

async function cmdImportWallet(args) {
  const keypair = loadKeypair(args);
  const output = {
    command: "import-wallet",
    publicKey: keypair.publicKey.toBase58(),
    secretLength: keypair.secretKey.length,
  };
  const savePath = arg(args, "save");
  if (savePath) {
    const format = arg(args, "save-format", "format") || "base58";
    const normalizedFormat = String(format).toLowerCase();
    output.savedTo = saveWalletSecret(savePath, keypair, normalizedFormat);
    output.saveFormat = normalizedFormat;
  }
  printResult(output);
}

async function cmdAddress(args) {
  const keypair = loadKeypair(args);
  printResult({
    command: "address",
    publicKey: keypair.publicKey.toBase58(),
  });
}

async function cmdBalance(args) {
  const wallet = arg(args, "wallet") || arg(args, "public-key", "public_key");
  const targetPublicKey = wallet || loadKeypair(args).publicKey.toBase58();
  const tokenMint = arg(args, "token-mint", "token_mint", "mint");
  const rpcUrl = resolveRpcUrl(args);
  const connection = new Connection(rpcUrl, "confirmed");

  const amount = await getWalletBalance(
    connection,
    targetPublicKey,
    tokenMint,
  );

  printResult({
    command: "balance",
    wallet: targetPublicKey,
    token: tokenMint || "SOL",
    amount,
    rpcUrl,
  });
}

async function cmdTransfer(args) {
  const keypair = loadKeypair(args);
  const rpcUrl = resolveRpcUrl(args);
  const connection = new Connection(rpcUrl, "confirmed");

  const to = getPublicKey(arg(args, "to"), "recipient");
  const amount = requireAmount(arg(args, "amount"), "amount");
  const token = arg(args, "token-mint", "token_mint", "mint");

  const signature = token
    ? await transferSpl(connection, keypair, to, amount, token)
    : await transferNative(connection, keypair, to, amount);

  printResult({
    command: "transfer",
    from: keypair.publicKey.toBase58(),
    to: to.toBase58(),
    token: token || "SOL",
    amount,
    signature,
    rpcUrl,
  });
}

async function cmdRequestFaucet(args) {
  const keypair = loadKeypair(args);
  const rpcUrl = resolveRpcUrl(args);
  const cluster = clusterFromRpc(rpcUrl);
  const amount = requireAmount(arg(args, "amount") || 5, "amount");
  if (cluster === "mainnet" && !isFlagTruthy(arg(args, "allow-mainnet-faucet", "allow_mainnet_faucet"))) {
    throw new Error(
      "Refusing to request faucet from mainnet. Use --allow-mainnet-faucet only if your RPC explicitly supports it.",
    );
  }

  const connection = new Connection(rpcUrl, "confirmed");
  const signature = await connection.requestAirdrop(
    keypair.publicKey,
    amount * LAMPORTS_PER_SOL,
  );
  const latest = await connection.getLatestBlockhash();
  await connection.confirmTransaction({ signature, ...latest }, "confirmed");

  printResult({
    command: "request-faucet",
    publicKey: keypair.publicKey.toBase58(),
    amount,
    rpcUrl,
    signature,
  });
}

function usage() {
  return `Usage:
  node solana-wallet.mjs <command> [options]

Commands:
  create-wallet          Create a new keypair
  import-wallet          Validate and print an existing wallet public key
  address                Print wallet address
  balance                Get SOL or SPL token balance
  transfer               Send SOL or SPL token
  request-faucet         Request airdrop on devnet/testnet (or explicit mainnet override)

Common flags:
  --rpc-url <url>             RPC endpoint (defaults to devnet)
  --wallet <key-or-path>      Base58 key, JSON key array, or path to key file

Examples:
  node solana-wallet.mjs create-wallet --save ./wallet.txt
  node solana-wallet.mjs balance --wallet ./wallet.txt
  node solana-wallet.mjs transfer --wallet ./wallet.txt --to 8x... --amount 1.5
  node solana-wallet.mjs transfer --wallet ./wallet.txt --to 8x... --amount 100 --token-mint EPj...`;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const command = args._.shift();

  if (!command) {
    throw new Error(usage());
  }

  const handlers = {
    "create-wallet": cmdCreateWallet,
    "import-wallet": cmdImportWallet,
    address: cmdAddress,
    balance: cmdBalance,
    transfer: cmdTransfer,
    "request-faucet": cmdRequestFaucet,
  };

  const handler = handlers[command];
  if (!handler) {
    throw new Error(`Unknown command ${command}\n\n${usage()}`);
  }

  await handler(args);
}

main().catch((error) => {
  printResult({
    status: "error",
    message: error?.message || String(error),
  });
  process.exitCode = 1;
});
