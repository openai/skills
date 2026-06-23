#!/usr/bin/env node

'use strict';

const fs = require('node:fs');
const path = require('node:path');

const MAX_SLIPPAGE = 5000n;
const DEF_SLIPPAGE = 500n;
const EXCLUSIVITY = 0;
const REF_SHARE = 0;
const FRESHNESS = 30;
const TTL = 300n;
const U32_MAX = 4294967295n;
const MIN_NON_ZERO_EPOCH = 31n;
const MAX_APPROVAL = (1n << 256n) - 1n;
const DEF_WATCH_INTERVAL = 5;
const DEF_WATCH_TIMEOUT = 0;
const TERMINAL_ORDER_STATUSES = new Set(['filled', 'completed', 'cancelled', 'canceled', 'expired', 'failed', 'rejected']);
const NOTE_ORACLE = 'Oracle protection applies to all order types and every chunk.';
const NOTE_EPOCH = 'epoch is the delay between chunks, but it is not exact: one chunk can fill once anywhere inside each epoch window.';
const NOTE_SIGN = 'Sign typedData with any EIP-712 flow. eth_signTypedData_v4 is only an example.';
const WARN_LOW_SLIPPAGE = 'slippage below 5% can reduce fill probability. 5% is the default compromise; higher slippage still uses oracle pricing and offchain executors.';
const WARN_RECIPIENT = 'recipient differs from swapper and is dangerous to change';

const SCRIPT_DIR = __dirname;
const SKILL_DIR = path.resolve(SCRIPT_DIR, '..');
const REPO_ROOT = path.resolve(SKILL_DIR, '..');
const SKELETON = path.join(SKILL_DIR, 'assets', 'repermit.skeleton.json');
const MANIFEST_JSON = path.join(REPO_ROOT, 'manifest.json');

let runtimeConfig = null;
let skeletonCache = null;
let ZERO = '';
let SINK = '';
let CREATE_URL = '';
let QUERY_URL = '';
let REPERMIT = '';
let REACTOR = '';
let EXECUTOR = '';
let SUPPORTED_CHAIN_IDS = '';
let warnings = [];

class CliError extends Error {}

function die(message) {
  throw new CliError(message);
}

function lower(value) {
  return String(value).toLowerCase();
}

function trim(value) {
  return String(value ?? '').trim();
}

function warn(message) {
  warnings.push(message);
  process.stderr.write(`warning: ${message}\n`);
}

function note(message) {
  process.stderr.write(`info: ${message}\n`);
}

function firstDefined(...values) {
  for (const value of values) {
    if (value !== undefined && value !== null) {
      return value;
    }
  }
  return undefined;
}

function isPlainObject(value) {
  return !!value && typeof value === 'object' && !Array.isArray(value);
}

function objectOrEmpty(value) {
  return isPlainObject(value) ? value : {};
}

function decimalString(value, name = 'value') {
  const text = trim(value);
  if (!text) {
    die(`${name} is required`);
  }
  if (/^\d+$/.test(text)) {
    return BigInt(text).toString(10);
  }
  if (/^0[xX][0-9a-fA-F]+$/.test(text)) {
    return BigInt(text).toString(10);
  }
  die(`${name} must be decimal or 0x integer`);
}

function decimalOnly(value, name = 'value') {
  const text = trim(value);
  if (!/^\d+$/.test(text)) {
    die(`${name} must be decimal`);
  }
  return BigInt(text);
}

function compare(a, b) {
  const left = decimalOnly(a);
  const right = decimalOnly(b);
  if (left < right) {
    return -1;
  }
  if (left > right) {
    return 1;
  }
  return 0;
}

function eq(a, b) {
  return compare(a, b) === 0;
}

function gt(a, b) {
  return compare(a, b) === 1;
}

function add(a, b) {
  return (decimalOnly(a) + decimalOnly(b)).toString(10);
}

function subtract(a, b) {
  const left = decimalOnly(a);
  const right = decimalOnly(b);
  if (left < right) {
    die('internal subtraction underflow');
  }
  return (left - right).toString(10);
}

function multiply(a, b) {
  return (decimalOnly(a) * decimalOnly(b)).toString(10);
}

function divideAndRemainder(a, b) {
  const left = decimalOnly(a);
  const right = decimalOnly(b);
  if (right === 0n) {
    die('division by zero');
  }
  return {
    quotient: (left / right).toString(10),
    remainder: (left % right).toString(10),
  };
}

function ensureU32(value, name) {
  if (decimalOnly(value, name) > U32_MAX) {
    die(`${name} must fit in uint32`);
  }
}

function hexBody(value, name, { allowBare = false } = {}) {
  const text = trim(value);
  if (/^0x[0-9a-fA-F]*$/.test(text)) {
    return text.slice(2);
  }
  if (allowBare && /^[0-9a-fA-F]+$/.test(text)) {
    return text;
  }
  die(`${name} must be hex`);
}

function parseAddress(value, name, allowZero = false) {
  const text = `0x${hexBody(value, name)}`;
  if (text.length !== 42) {
    die(`${name} must be a 20-byte 0x address`);
  }
  if (!allowZero && ZERO && lower(text) === lower(ZERO)) {
    die(`${name} cannot be zero`);
  }
  return text;
}

function requireHex(value, name) {
  const raw = hexBody(value, name);
  if (raw.length % 2 !== 0) {
    die(`${name} must be hex`);
  }
  return `0x${raw}`;
}

function formatError(error) {
  if (!error) {
    return 'unknown error';
  }
  const parts = [];
  if (error.message) {
    parts.push(error.message);
  }
  if (error.cause && error.cause.message) {
    parts.push(error.cause.message);
  } else if (error.cause && error.cause.code) {
    parts.push(String(error.cause.code));
  }
  return parts.filter(Boolean).join(': ') || 'unknown error';
}

function normalizeSizedHex(value, name, size) {
  const raw = hexBody(value, name, { allowBare: true });
  if (raw.length !== size) {
    die(`${name} must be ${size} hex chars`);
  }
  return `0x${raw}`;
}

function padHex64(value, name = 'value') {
  const raw = lower(hexBody(value, name, { allowBare: true }));
  if (raw.length > 64) {
    die(`${name} must fit in uint256`);
  }
  return `0x${raw.padStart(64, '0')}`;
}

function parseOptions(args, spec, command) {
  const values = Object.fromEntries(Object.values(spec).map((key) => [key, '']));
  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];
    const key = spec[arg];
    if (!key) {
      die(`unknown ${command} arg: ${arg}`);
    }
    const value = args[index + 1];
    if (value === undefined) {
      die(`${command} arg requires a value: ${arg}`);
    }
    values[key] = value;
    index += 1;
  }
  return values;
}

function countPresent(...values) {
  return values.reduce((count, value) => count + (value ? 1 : 0), 0);
}

function approveCalldata(spender, amount) {
  const spenderHex = padHex64(parseAddress(spender, 'approve.spender'), 'approve.spender');
  const amountHex = padHex64(decimalOnly(amount, 'approve.amount').toString(16), 'approve.amount');
  return `0x095ea7b3${spenderHex.slice(2)}${amountHex.slice(2)}`;
}

function normalizeSigV(value, name = 'signature.v') {
  const raw = trim(value);
  if (!raw) {
    die(`${name} is required`);
  }

  let decimal;
  if (/^0[xX][0-9a-fA-F]+$/.test(raw)) {
    decimal = BigInt(raw);
  } else if (/^\d+$/.test(raw)) {
    decimal = BigInt(raw);
  } else if (/^[0-9a-fA-F]+$/.test(raw)) {
    decimal = BigInt(`0x${raw}`);
  } else {
    die(`${name} must be 0, 1, 27, 28, or equivalent hex`);
  }

  switch (decimal.toString(10)) {
    case '0':
    case '27':
      return '0x1b';
    case '1':
    case '28':
      return '0x1c';
    default:
      die(`${name} must be 0, 1, 27, 28, or equivalent hex`);
  }
}

function now() {
  return Math.floor(Date.now() / 1000).toString(10);
}

function iso() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');
}

function readSource(src, name) {
  const source = trim(src);
  if (!source) {
    die(`${name} is required`);
  }
  if (source === '-') {
    return fs.readFileSync(0, 'utf8');
  }
  try {
    return fs.readFileSync(source, 'utf8');
  } catch (error) {
    if (error && error.code === 'ENOENT') {
      die(`${name} not found: ${source}`);
    }
    throw error;
  }
}

function parseJson(text, name) {
  try {
    return JSON.parse(text);
  } catch {
    die(`${name} must be valid JSON`);
  }
}

function readJsonSource(src, name) {
  return parseJson(readSource(src, name), name);
}

function jsonOrText(text) {
  if (text === '') {
    return '';
  }
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

function writeOutput(value, outFile) {
  const text = typeof value === 'string' ? value : JSON.stringify(value, null, 2);
  if (outFile) {
    fs.writeFileSync(outFile, `${text}\n`);
    return;
  }
  process.stdout.write(`${text}\n`);
}

function loadRuntimeConfig() {
  if (runtimeConfig) {
    return runtimeConfig;
  }

  let manifest;
  try {
    manifest = parseJson(fs.readFileSync(MANIFEST_JSON, 'utf8'), 'manifest');
  } catch (error) {
    if (error instanceof CliError) {
      throw error;
    }
    if (error && error.code === 'ENOENT') {
      die(`skill manifest not found: ${MANIFEST_JSON}`);
    }
    throw error;
  }

  const runtime = manifest && typeof manifest === 'object' ? manifest.runtime : null;
  const contracts = runtime && typeof runtime === 'object' ? runtime.contracts : null;
  const chains = runtime && typeof runtime === 'object' ? runtime.chains : null;
  const url = runtime && typeof runtime.url === 'string' ? runtime.url : '';
  const zero = contracts && typeof contracts.zero === 'string' ? contracts.zero : '';
  const repermit = contracts && typeof contracts.repermit === 'string' ? contracts.repermit : '';
  const reactor = contracts && typeof contracts.reactor === 'string' ? contracts.reactor : '';
  const executor = contracts && typeof contracts.executor === 'string' ? contracts.executor : '';

  const invalidRuntime =
    !url ||
    !zero ||
    !repermit ||
    !reactor ||
    !executor ||
    !chains ||
    typeof chains !== 'object' ||
    Array.isArray(chains) ||
    Object.keys(chains).length === 0;

  if (invalidRuntime) {
    die(`invalid skill manifest runtime config: ${MANIFEST_JSON}`);
  }

  ZERO = parseAddress(zero, 'runtime.contracts.zero', true);
  REPERMIT = parseAddress(repermit, 'runtime.contracts.repermit');
  REACTOR = parseAddress(reactor, 'runtime.contracts.reactor');
  EXECUTOR = parseAddress(executor, 'runtime.contracts.executor');
  SINK = url;

  if (!/^https?:\/\//.test(SINK)) {
    die('runtime.url must be http(s)');
  }

  const supported = Object.keys(chains)
    .map((chainId) => {
      const parsed = Number(chainId);
      if (!Number.isInteger(parsed)) {
        die(`invalid skill manifest runtime config: ${MANIFEST_JSON}`);
      }
      return parsed;
    })
    .sort((left, right) => left - right)
    .map((value) => String(value));

  SUPPORTED_CHAIN_IDS = supported.join(', ');
  if (!SUPPORTED_CHAIN_IDS) {
    die(`skill manifest runtime has no supported chains: ${MANIFEST_JSON}`);
  }

  CREATE_URL = `${SINK}/orders/new`;
  QUERY_URL = `${SINK}/orders`;
  runtimeConfig = { chains };
  return runtimeConfig;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function hasSupportedChain(chainId) {
  const config = loadRuntimeConfig();
  const chain = config.chains[String(chainId)];
  return !!(chain && typeof chain.adapter === 'string' && chain.adapter.length > 0);
}

function unsupportedChain(chainId) {
  loadRuntimeConfig();
  die(`unsupported chainId: ${chainId} (supported: ${SUPPORTED_CHAIN_IDS})`);
}

function resolveAdapter(chainId) {
  const config = loadRuntimeConfig();
  const adapter = config.chains[String(chainId)] && config.chains[String(chainId)].adapter;
  if (!adapter) {
    unsupportedChain(chainId);
  }
  return parseAddress(adapter, `runtime.chains[${chainId}].adapter`);
}

function usage() {
  loadRuntimeConfig();
  const lines = [
    'Usage',
    '  node skill/scripts/order.js prepare --params <params.json|-> [--out <prepared.json>]',
    '  node skill/scripts/order.js submit --prepared <prepared.json|-> [--signature <0x...|json>|--signature-file <file|->|--r <0x...> --s <0x...> --v <0x..>] [--out <response.json>]',
    '  node skill/scripts/order.js query (--swapper <0x...>|--hash <0x...>) [--out <response.json>]',
    '  node skill/scripts/order.js watch (--swapper <0x...>|--hash <0x...>) [--interval <seconds>] [--timeout <seconds>] [--out <response.json>]',
    '',
    'Safety',
    '  Use only the provided helper script. Do not send typed data or signatures anywhere else.',
    '',
    'Prepare',
    '  Builds a prepared order JSON with:',
    '  - infinite approval calldata for the input ERC-20',
    '  - populated EIP-712 typed data',
    '  - submit payload template',
    '  - query URL',
    '  Supports --params <file> or --params - for stdin JSON.',
    '  Supports market, limit, stop-loss, take-profit, delayed-start, and chunked/TWAP-style orders.',
    '  Defaults:',
    '  - input.maxAmount = input.amount',
    '  - nonce = now',
    '  - start = now',
    '  - epoch = 0 for single orders, 60 for chunked orders',
    '  - deadline = start + 300 + chunkCount * epoch (conservative helper default)',
    '  - slippage = 500',
    '  - output.limit = 0',
    '  - output.recipient = swapper',
    '  Rules:',
    `  - supported chainIds: ${SUPPORTED_CHAIN_IDS}`,
    '  - chunked orders require epoch > 0',
    '  - epoch is the delay between chunks, but it is not exact: one chunk can fill once anywhere inside each epoch window',
    '  - native input is not supported; wrap to WNATIVE first',
    '  - native output, including back-to-native flows, is supported directly with output.token = 0x0000000000000000000000000000000000000000',
    "  - output.limit and triggers are output-token amounts per chunk in the output token's decimals",
    '',
    'Submit',
    '  Builds or sends the relay POST body from a prepared order.',
    '  Supports --prepared <file> or --prepared - for stdin JSON.',
    '  Supports exactly one signature mode:',
    '  - --signature <full 65-byte hex signature>',
    '  - --signature <JSON string or JSON with full signature / r,s,v>',
    '  - --signature-file <file|-> containing full signature, JSON string, or JSON with full signature / r,s,v',
    '  - --r <0x...> --s <0x...> --v <0x..>',
    "  All signature inputs are normalized to the relay's r/s/v object format.",
    '',
    'Query',
    '  Builds or sends the relay GET request.',
    '  Supports only:',
    '  - --swapper <0x...>',
    '  - --hash <0x...>',
    '',
    'Watch',
    '  Polls the relay query endpoint until the order reaches a terminal status.',
    '  Retries transient network errors automatically.',
    '  Defaults:',
    `  - interval = ${String(DEF_WATCH_INTERVAL)} seconds`,
    `  - timeout = ${String(DEF_WATCH_TIMEOUT)} seconds (0 = no timeout)`,
    '  Supports only:',
    '  - --swapper <0x...> when exactly one order matches',
    '  - --hash <0x...> (recommended)',
  ];
  process.stdout.write(`${lines.join('\n')}\n`);
}

function loadSkeleton() {
  if (!skeletonCache) {
    skeletonCache = parseJson(fs.readFileSync(SKELETON, 'utf8'), 'typed data skeleton');
  }
  return JSON.parse(JSON.stringify(skeletonCache));
}

function buildTypedData(
  chainId,
  swapper,
  nonce,
  start,
  deadline,
  epoch,
  slippage,
  inputToken,
  inputAmount,
  inputMaxAmount,
  outputToken,
  outputLimit,
  outputTriggerLower,
  outputTriggerUpper,
  outputRecipient,
) {
  const typedData = loadSkeleton();
  typedData.domain.chainId = Number(chainId);
  typedData.domain.verifyingContract = REPERMIT;
  typedData.message.permitted.token = inputToken;
  typedData.message.permitted.amount = inputMaxAmount;
  typedData.message.spender = REACTOR;
  typedData.message.nonce = nonce;
  typedData.message.deadline = deadline;
  typedData.message.witness.reactor = REACTOR;
  typedData.message.witness.executor = EXECUTOR;
  typedData.message.witness.exchange.adapter = resolveAdapter(chainId);
  typedData.message.witness.exchange.ref = ZERO;
  typedData.message.witness.exchange.share = REF_SHARE;
  typedData.message.witness.exchange.data = '0x';
  typedData.message.witness.swapper = swapper;
  typedData.message.witness.nonce = nonce;
  typedData.message.witness.start = start;
  typedData.message.witness.deadline = deadline;
  typedData.message.witness.chainid = Number(chainId);
  typedData.message.witness.exclusivity = EXCLUSIVITY;
  typedData.message.witness.epoch = Number(epoch);
  typedData.message.witness.slippage = Number(slippage);
  typedData.message.witness.freshness = FRESHNESS;
  typedData.message.witness.input.token = inputToken;
  typedData.message.witness.input.amount = inputAmount;
  typedData.message.witness.input.maxAmount = inputMaxAmount;
  typedData.message.witness.output.token = outputToken;
  typedData.message.witness.output.limit = outputLimit;
  typedData.message.witness.output.triggerLower = outputTriggerLower;
  typedData.message.witness.output.triggerUpper = outputTriggerUpper;
  typedData.message.witness.output.recipient = outputRecipient;
  return typedData;
}

function signatureFieldsFromObject(parsed) {
  if (typeof parsed.signature === 'string') {
    return { payload: parsed.signature };
  }
  if (typeof parsed.full === 'string') {
    return { payload: parsed.full };
  }
  const source = isPlainObject(parsed.signature) ? parsed.signature : parsed;
  const r = source.r ?? '';
  const s = source.s ?? '';
  const v = source.v ?? '';
  if (!r || !s || !v) {
    die('signature JSON must contain a full signature string or r, s, v');
  }
  return { r, s, v, kind: 'rsv' };
}

function normalizeSignature(payloadInput) {
  let payload = trim(payloadInput);
  let r = '';
  let s = '';
  let v = '';
  let full = '';
  let kind = '';

  if (!payload) {
    die('signature input is empty');
  }

  try {
    const parsed = JSON.parse(payload);
    if (typeof parsed === 'string') {
      payload = parsed;
    } else if (isPlainObject(parsed)) {
      ({ payload = payload, r = '', s = '', v = '', kind = '' } = signatureFieldsFromObject(parsed));
    } else {
      die('signature JSON must contain a full signature string or r, s, v');
    }
  } catch (error) {
    if (error instanceof CliError) {
      throw error;
    }
  }

  if (r || s || v) {
    r = normalizeSizedHex(r, 'signature.r', 64);
    s = normalizeSizedHex(s, 'signature.s', 64);
    v = normalizeSigV(v, 'signature.v');
    full = `${r}${s.slice(2)}${v.slice(2)}`;
  } else {
    let signature = trim(payload);
    if (!/^(?:0x)?[0-9a-fA-F]{130}$/.test(signature)) {
      die('signature must be full hex, a JSON string, or r/s/v JSON');
    }
    if (!signature.startsWith('0x')) {
      signature = `0x${signature}`;
    }
    full = signature;
    r = `0x${signature.slice(2, 66)}`;
    s = `0x${signature.slice(66, 130)}`;
    v = normalizeSigV(`0x${signature.slice(130, 132)}`, 'signature.v');
    if (!kind) {
      kind = 'full';
    }
  }

  return {
    kind,
    full,
    signature: { r, s, v },
  };
}

function prepare(args) {
  loadRuntimeConfig();

  warnings = [];

  const { paramsSource, outFile } = parseOptions(
    args,
    { '--params': 'paramsSource', '--out': 'outFile' },
    'prepare',
  );

  const params = readJsonSource(paramsSource, 'params');
  const input = objectOrEmpty(params.input);
  const output = objectOrEmpty(params.output);
  const nowTs = now();
  const chainId = decimalString(firstDefined(params.chainId, params.chainID), 'chainId');
  if (!hasSupportedChain(chainId)) {
    unsupportedChain(chainId);
  }

  const swapper = parseAddress(firstDefined(params.swapper, params.account, params.signer), 'swapper');
  const nonce = decimalString(firstDefined(params.nonce, nowTs), 'nonce');
  const start = decimalString(firstDefined(params.start, nowTs), 'start');
  const slippage = decimalString(firstDefined(params.slippage, DEF_SLIPPAGE.toString(10)), 'slippage');
  const inputToken = parseAddress(firstDefined(input.token, params.inputToken), 'input.token');
  const inputAmount = decimalString(firstDefined(input.amount, params.inputAmount), 'input.amount');
  let inputMaxAmount = decimalString(
    firstDefined(input.maxAmount, params.inputMaxAmount, inputAmount),
    'input.maxAmount',
  );
  const outputToken = parseAddress(firstDefined(output.token, params.outputToken), 'output.token', true);
  const outputLimit = decimalString(firstDefined(output.limit, params.outputLimit, '0'), 'output.limit');
  const outputTriggerLower = decimalString(
    firstDefined(output.triggerLower, params.outputTriggerLower, '0'),
    'output.triggerLower',
  );
  const outputTriggerUpper = decimalString(
    firstDefined(output.triggerUpper, params.outputTriggerUpper, '0'),
    'output.triggerUpper',
  );
  const recipient = parseAddress(firstDefined(output.recipient, params.recipient, swapper), 'output.recipient');

  let epoch;
  if (params.epoch !== undefined && params.epoch !== null) {
    epoch = decimalString(params.epoch, 'epoch');
  } else {
    epoch = eq(inputAmount, inputMaxAmount) ? '0' : '60';
  }

  ensureU32(epoch, 'epoch');
  ensureU32(slippage, 'slippage');

  if (eq(start, '0')) {
    die('start must be non-zero');
  }
  if (eq(inputAmount, '0')) {
    die('input.amount must be non-zero');
  }
  if (gt(inputAmount, inputMaxAmount)) {
    die('input.amount cannot exceed input.maxAmount');
  }
  if (lower(inputToken) === lower(outputToken)) {
    die('input.token and output.token must differ');
  }
  if (!eq(outputTriggerUpper, '0') && gt(outputTriggerLower, outputTriggerUpper)) {
    die('output.triggerLower cannot exceed output.triggerUpper');
  }
  if (gt(slippage, MAX_SLIPPAGE.toString(10))) {
    die(`slippage cannot exceed ${MAX_SLIPPAGE.toString(10)}`);
  }
  if (!eq(epoch, '0') && compare(epoch, MIN_NON_ZERO_EPOCH.toString()) === -1) {
    die(`non-zero epoch must be >= ${MIN_NON_ZERO_EPOCH.toString()} because helper freshness is ${String(FRESHNESS)}`);
  }
  if (!eq(epoch, '0') && compare(String(FRESHNESS), epoch) !== -1) {
    die('freshness must be < epoch when epoch != 0');
  }

  const requestedInputMaxAmount = inputMaxAmount;
  const chunking = divideAndRemainder(inputMaxAmount, inputAmount);
  const chunkCount = chunking.quotient;
  const remainder = chunking.remainder;

  if (!eq(remainder, '0')) {
    inputMaxAmount = subtract(inputMaxAmount, remainder);
    warn(
      `input.maxAmount is not divisible by input.amount; rounding down from ${requestedInputMaxAmount} to ${inputMaxAmount} to keep fixed chunk sizes`,
    );
  }

  if (!eq(inputAmount, inputMaxAmount) && eq(epoch, '0')) {
    die(`chunked orders require epoch >= ${MIN_NON_ZERO_EPOCH.toString()}`);
  }

  const kind = eq(inputAmount, inputMaxAmount) ? 'single' : 'chunked';
  let deadline;
  if (params.deadline !== undefined && params.deadline !== null) {
    deadline = decimalString(params.deadline, 'deadline');
  } else {
    deadline = add(start, TTL.toString(10));
    if (gt(epoch, '0')) {
      deadline = add(deadline, multiply(chunkCount, epoch));
    }
  }

  if (gt(start, nowTs)) {
    if (!gt(deadline, start)) {
      die('deadline must be after start');
    }
  } else if (!gt(deadline, nowTs)) {
    die('deadline must be after current time');
  }

  if (compare(slippage, DEF_SLIPPAGE.toString(10)) === -1) {
    warn(WARN_LOW_SLIPPAGE);
  }
  if (lower(recipient) !== lower(swapper)) {
    warn(WARN_RECIPIENT);
  }

  const approvalAmount = MAX_APPROVAL.toString(10);
  const approvalData = requireHex(approveCalldata(REPERMIT, approvalAmount), 'approval.tx.data');
  const typedData = buildTypedData(
    chainId,
    swapper,
    nonce,
    start,
    deadline,
    epoch,
    slippage,
    inputToken,
    inputAmount,
    inputMaxAmount,
    outputToken,
    outputLimit,
    outputTriggerLower,
    outputTriggerUpper,
    recipient,
  );

  const prepared = {
    meta: {
      preparedAt: iso(),
      kind,
      chunkCount,
      chunkInputAmount: inputAmount,
      start,
      deadline,
      epoch,
      epochScheduling: NOTE_EPOCH,
      limit: outputLimit,
      oracleProtection: NOTE_ORACLE,
    },
    warnings,
    approval: {
      token: inputToken,
      spender: REPERMIT,
      amount: approvalAmount,
      tx: {
        to: inputToken,
        data: approvalData,
        value: '0x0',
      },
    },
    typedData,
    signing: {
      signer: swapper,
      note: NOTE_SIGN,
    },
    submit: {
      url: CREATE_URL,
      body: {
        order: typedData.message,
        signature: {
          r: null,
          s: null,
          v: null,
        },
        status: 'pending',
      },
    },
    query: {
      url: QUERY_URL,
    },
  };

  writeOutput(prepared, outFile);
  return 0;
}

function selectOrderPayload(prepared) {
  if (prepared && prepared.submit && prepared.submit.body && prepared.submit.body.order) {
    return prepared.submit.body.order;
  }
  if (prepared && prepared.typedData && prepared.typedData.message) {
    return prepared.typedData.message;
  }
  if (prepared && prepared.domain && prepared.types && prepared.message) {
    return prepared.message;
  }
  die('missing order payload');
}

async function requestJson(url, options) {
  let response;
  try {
    response = await fetch(url, options);
  } catch (error) {
    die(`request failed: ${formatError(error)}`);
  }
  const text = await response.text();
  return {
    ok: response.ok,
    status: response.status,
    response: jsonOrText(text),
  };
}

function secondsOption(value, name, fallback) {
  const selected = trim(value) ? value : fallback;
  const parsed = decimalString(selected, name);
  ensureU32(parsed, name);
  return Number(parsed);
}

function buildQueryUrl(rawSwapper, rawHash) {
  let swapper = trim(rawSwapper);
  let hash = trim(rawHash);

  if (!swapper && !hash) {
    die('query needs --swapper or --hash');
  }

  let url = QUERY_URL;
  if (swapper) {
    swapper = parseAddress(swapper, 'swapper');
    url = `${url}?swapper=${encodeURIComponent(swapper)}`;
  }
  if (hash) {
    if (!/^0x[0-9a-fA-F]{64}$/.test(hash)) {
      die('hash must be 32-byte 0x hex');
    }
    url = url.includes('?') ? `${url}&hash=${encodeURIComponent(hash)}` : `${url}?hash=${encodeURIComponent(hash)}`;
  }

  return { swapper, hash, url };
}

function responseOrders(response) {
  return isPlainObject(response) && Array.isArray(response.orders) ? response.orders : [];
}

function responseOrderHash(response) {
  if (!isPlainObject(response)) {
    return '';
  }

  const direct = trim(response.orderHash);
  if (/^0x[0-9a-fA-F]{64}$/.test(direct)) {
    return direct;
  }

  const signedOrder = objectOrEmpty(response.signedOrder);
  const nested = trim(signedOrder.hash);
  if (/^0x[0-9a-fA-F]{64}$/.test(nested)) {
    return nested;
  }

  return '';
}

function submitOutput(result, request) {
  const orderHash = result.ok ? responseOrderHash(result.response) : '';
  const watch = orderHash
    ? {
        hash: orderHash,
        command: `node skill/scripts/order.js watch --hash ${orderHash}`,
        url: `${QUERY_URL}?hash=${encodeURIComponent(orderHash)}`,
      }
    : null;

  return {
    ok: result.ok,
    status: result.status,
    url: request.url,
    request,
    response: result.response,
    orderHash,
    watch,
  };
}

function watchSnapshot(response, { hash }) {
  const orders = responseOrders(response);
  if (!hash && orders.length > 1) {
    die('watch with --swapper requires exactly one matching order; use --hash to disambiguate');
  }

  const order = isPlainObject(orders[0]) ? orders[0] : null;
  const metadata = objectOrEmpty(order && order.metadata);
  const status = trim(firstDefined(metadata.status, order && order.status));
  const chunkStatuses = Array.isArray(metadata.chunks)
    ? metadata.chunks.map((chunk) => trim(chunk && chunk.status)).filter(Boolean)
    : [];

  return {
    count: orders.length,
    status,
    chunkStatuses,
  };
}

function watchOutput(result, url, watchMeta) {
  return {
    ok: result.ok,
    status: result.status,
    url,
    response: result.response,
    watch: watchMeta,
  };
}

function buildWatchMeta({
  polls,
  queryErrors,
  intervalSeconds,
  timeoutSeconds,
  startedAt,
  finalStatus,
  chunkStatuses,
  timedOut,
  lastError,
}) {
  return {
    command: 'watch',
    polls,
    queryErrors,
    intervalSeconds,
    timeoutSeconds,
    elapsedSeconds: Math.floor((Date.now() - startedAt) / 1000),
    finalStatus,
    chunkStatuses,
    timedOut,
    lastError,
  };
}

async function submit(args) {
  loadRuntimeConfig();

  const { preparedSource, signatureInput, signatureFile, r, s, v, outFile } = parseOptions(
    args,
    {
      '--prepared': 'preparedSource',
      '--signature': 'signatureInput',
      '--signature-file': 'signatureFile',
      '--r': 'r',
      '--s': 's',
      '--v': 'v',
      '--out': 'outFile',
    },
    'submit',
  );

  if (preparedSource === '-' && signatureFile === '-') {
    die('submit supports only one stdin source');
  }

  const prepared = readJsonSource(preparedSource, 'prepared');
  if (countPresent(signatureInput, signatureFile, r || s || v) !== 1) {
    die('submit needs exactly one of --signature, --signature-file, or --r/--s/--v');
  }

  let normalizedSignature;
  if (signatureFile) {
    normalizedSignature = normalizeSignature(readSource(signatureFile, 'signature-file'));
  } else if (signatureInput) {
    normalizedSignature = normalizeSignature(signatureInput);
  } else {
    if (!r || !s || !v) {
      die('--r --s --v must be used together');
    }
    normalizedSignature = normalizeSignature(JSON.stringify({ r, s, v }));
  }

  const request = {
    url: (prepared.submit && prepared.submit.url) || CREATE_URL,
    body: {
      order: selectOrderPayload(prepared),
      signature: normalizedSignature.signature,
      status: (prepared.submit && prepared.submit.body && prepared.submit.body.status) || 'pending',
    },
    signatureInput: normalizedSignature.kind,
  };

  const result = await requestJson(request.url, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(request.body),
  });

  writeOutput(submitOutput(result, request), outFile);

  return result.ok ? 0 : 1;
}

async function query(args) {
  loadRuntimeConfig();

  const { swapper: rawSwapper, hash: rawHash, outFile } = parseOptions(
    args,
    { '--swapper': 'swapper', '--hash': 'hash', '--out': 'outFile' },
    'query',
  );
  const { url } = buildQueryUrl(rawSwapper, rawHash);

  const result = await requestJson(url, { method: 'GET' });
  writeOutput(
    {
      ok: result.ok,
      status: result.status,
      url,
      response: result.response,
    },
    outFile,
  );

  return result.ok ? 0 : 1;
}

async function watchOrder(args) {
  loadRuntimeConfig();
  const watchCommand = 'watch';

  const { swapper: rawSwapper, hash: rawHash, interval, timeout, outFile } = parseOptions(
    args,
    {
      '--swapper': 'swapper',
      '--hash': 'hash',
      '--interval': 'interval',
      '--timeout': 'timeout',
      '--out': 'outFile',
    },
    watchCommand,
  );

  const intervalSeconds = secondsOption(interval, 'interval', String(DEF_WATCH_INTERVAL));
  const timeoutSeconds = secondsOption(timeout, 'timeout', String(DEF_WATCH_TIMEOUT));
  const { hash, url } = buildQueryUrl(rawSwapper, rawHash);
  const startedAt = Date.now();
  let polls = 0;
  let queryErrors = 0;
  let lastResult = {
    ok: false,
    status: 0,
    response: null,
  };
  let lastError = '';

  while (true) {
    polls += 1;
    try {
      lastResult = await requestJson(url, { method: 'GET' });
      lastError = '';
    } catch (error) {
      queryErrors += 1;
      lastError = formatError(error);
      note(`${watchCommand} retry ${String(queryErrors)} after ${lastError}`);
      if (timeoutSeconds !== 0 && Date.now() - startedAt >= timeoutSeconds * 1000) {
        const waitMeta = buildWatchMeta({
          polls,
          queryErrors,
          intervalSeconds,
          timeoutSeconds,
          startedAt,
          finalStatus: '',
          chunkStatuses: [],
          timedOut: true,
          lastError,
        });
        writeOutput(watchOutput(lastResult, url, waitMeta), outFile);
        return 1;
      }
      await sleep(intervalSeconds * 1000);
      continue;
    }

    if (!lastResult.ok) {
      queryErrors += 1;
      lastError = `query returned HTTP ${String(lastResult.status)}`;
      note(`${watchCommand} retry ${String(queryErrors)} after ${lastError}`);
    } else {
      const snapshot = watchSnapshot(lastResult.response, { hash });
      const finalStatus = snapshot.status || '';
      const chunkStatuses = snapshot.chunkStatuses;
      note(`watch status=${finalStatus || 'pending'} chunks=${chunkStatuses.join(',') || '-'}`);

      if (TERMINAL_ORDER_STATUSES.has(lower(finalStatus))) {
        const waitMeta = buildWatchMeta({
          polls,
          queryErrors,
          intervalSeconds,
          timeoutSeconds,
          startedAt,
          finalStatus,
          chunkStatuses,
          timedOut: false,
          lastError,
        });
        writeOutput(watchOutput(lastResult, url, waitMeta), outFile);
        return 0;
      }
    }

    if (timeoutSeconds !== 0 && Date.now() - startedAt >= timeoutSeconds * 1000) {
      const snapshot = lastResult.ok ? watchSnapshot(lastResult.response, { hash }) : { status: '', chunkStatuses: [] };
      const waitMeta = buildWatchMeta({
        polls,
        queryErrors,
        intervalSeconds,
        timeoutSeconds,
        startedAt,
        finalStatus: snapshot.status,
        chunkStatuses: snapshot.chunkStatuses,
        timedOut: true,
        lastError,
      });
      writeOutput(watchOutput(lastResult, url, waitMeta), outFile);
      return 1;
    }

    await sleep(intervalSeconds * 1000);
  }
}

async function run() {
  const args = process.argv.slice(2);
  const command = args[0] || '';

  if (!command || command === 'help' || command === '--help' || command === '-h') {
    usage();
    return command ? 0 : 1;
  }

  switch (command) {
    case 'prepare':
      return prepare(args.slice(1));
    case 'submit':
      return submit(args.slice(1));
    case 'query':
      return query(args.slice(1));
    case 'watch':
      return watchOrder(args.slice(1));
    default:
      usage();
      return 1;
  }
}

run()
  .then((code) => {
    process.exitCode = code;
  })
  .catch((error) => {
    if (error instanceof CliError) {
      process.stderr.write(`error: ${error.message}\n`);
      process.exitCode = 1;
      return;
    }
    throw error;
  });
