#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import readline from "node:readline";

function printHelp() {
	console.log(`Usage:
  bun report-token-usage.mjs [options]

Options:
  --date YYYY-MM-DD        Target date in the selected timezone (default: today)
  --timezone IANA_TZ       IANA timezone name (default: local timezone)
  --sessions-root PATH     Sessions root path (default: ~/.codex/sessions)
  --limit N                Max session rows shown in text output (default: 20)
  --json                   Print JSON only
  --help                   Show this help

Examples:
  bun report-token-usage.mjs --date 2026-03-05 --timezone Asia/Shanghai
  bun report-token-usage.mjs --date 2026-03-05 --json
`);
}

function parseArgs(argv) {
	const args = {
		date: null,
		timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
		sessionsRoot: path.join(os.homedir(), ".codex", "sessions"),
		limit: 20,
		json: false,
		help: false,
	};

	for (let i = 0; i < argv.length; i++) {
		const arg = argv[i];
		if (arg === "--help" || arg === "-h") {
			args.help = true;
			continue;
		}
		if (arg === "--json") {
			args.json = true;
			continue;
		}

		const [k, vInline] = arg.split("=", 2);
		const nextValue = vInline ?? argv[i + 1];

		if (k === "--date") {
			if (!nextValue) throw new Error("--date requires a value");
			args.date = nextValue;
			if (vInline === undefined) i++;
			continue;
		}
		if (k === "--timezone") {
			if (!nextValue) throw new Error("--timezone requires a value");
			args.timezone = nextValue;
			if (vInline === undefined) i++;
			continue;
		}
		if (k === "--sessions-root") {
			if (!nextValue) throw new Error("--sessions-root requires a value");
			args.sessionsRoot = nextValue;
			if (vInline === undefined) i++;
			continue;
		}
		if (k === "--limit") {
			if (!nextValue) throw new Error("--limit requires a value");
			const n = Number(nextValue);
			if (!Number.isFinite(n) || n <= 0) {
				throw new Error("--limit must be a positive number");
			}
			args.limit = Math.floor(n);
			if (vInline === undefined) i++;
			continue;
		}

		throw new Error(`Unknown argument: ${arg}`);
	}

	return args;
}

function isValidDate(date) {
	return /^\d{4}-\d{2}-\d{2}$/.test(date);
}

function getDateInTimezone(timezone, date = new Date()) {
	return new Intl.DateTimeFormat("en-CA", {
		timeZone: timezone,
		year: "numeric",
		month: "2-digit",
		day: "2-digit",
	}).format(date);
}

function getDateFormatter(timezone) {
	return new Intl.DateTimeFormat("en-CA", {
		timeZone: timezone,
		year: "numeric",
		month: "2-digit",
		day: "2-digit",
	});
}

function formatNumber(num) {
	return new Intl.NumberFormat("en-US").format(num);
}

async function collectRolloutFiles(rootDir) {
	const out = [];
	const stack = [rootDir];

	while (stack.length > 0) {
		const dir = stack.pop();
		let entries = [];
		try {
			entries = await fs.promises.readdir(dir, { withFileTypes: true });
		} catch {
			continue;
		}

		for (const entry of entries) {
			const fullPath = path.join(dir, entry.name);
			if (entry.isDirectory()) {
				stack.push(fullPath);
				continue;
			}
			if (
				entry.isFile() &&
				entry.name.startsWith("rollout-") &&
				entry.name.endsWith(".jsonl")
			) {
				out.push(fullPath);
			}
		}
	}

	return out;
}

async function parseRolloutFile(filePath) {
	let sessionId = null;
	let cwd = "(unknown)";
	const events = [];

	const rl = readline.createInterface({
		input: fs.createReadStream(filePath, { encoding: "utf8" }),
		crlfDelay: Infinity,
	});

	for await (const line of rl) {
		if (!line) continue;
		let obj;
		try {
			obj = JSON.parse(line);
		} catch {
			continue;
		}

		if (obj.type === "session_meta" && obj.payload) {
			sessionId = obj.payload.id || sessionId;
			cwd = obj.payload.cwd || cwd;
			continue;
		}

		if (
			obj.type === "event_msg" &&
			obj.payload?.type === "token_count" &&
			obj.payload?.info
		) {
			const total = Number(obj.payload.info?.total_token_usage?.total_tokens);
			const ts = obj.timestamp;
			const timeMs = ts ? Date.parse(ts) : Number.NaN;
			if (!Number.isFinite(total) || !Number.isFinite(timeMs)) continue;
			events.push({ ts, timeMs, total });
		}
	}

	if (events.length === 0) return null;

	return {
		sessionId,
		cwd,
		filePath,
		events,
	};
}

function chooseBestCwd(cwdCounts) {
	let best = "(unknown)";
	let bestCount = -1;
	for (const [cwd, count] of cwdCounts.entries()) {
		if (count > bestCount) {
			best = cwd;
			bestCount = count;
		}
	}
	return best;
}

function buildSessionAggregates(fileResults) {
	const bySession = new Map();

	for (const result of fileResults) {
		if (!result) continue;
		const key = result.sessionId ? `sid:${result.sessionId}` : `file:${result.filePath}`;
		let agg = bySession.get(key);
		if (!agg) {
			agg = {
				sessionKey: key,
				sessionId: result.sessionId,
				cwdCounts: new Map(),
				events: [],
				sourceFiles: new Set(),
			};
			bySession.set(key, agg);
		}

		if (result.cwd && result.cwd !== "(unknown)") {
			agg.cwdCounts.set(result.cwd, (agg.cwdCounts.get(result.cwd) || 0) + 1);
		}
		agg.events.push(...result.events);
		agg.sourceFiles.add(result.filePath);
	}

	return [...bySession.values()].map((agg) => ({
		sessionKey: agg.sessionKey,
		sessionId: agg.sessionId,
		cwd: chooseBestCwd(agg.cwdCounts),
		events: agg.events,
		sourceFiles: [...agg.sourceFiles],
	}));
}

function computeTokensForDay(events, targetDate, dateFormatter) {
	const deduped = [];
	const seen = new Set();
	for (const event of events) {
		const k = `${event.timeMs}|${event.total}`;
		if (seen.has(k)) continue;
		seen.add(k);
		deduped.push(event);
	}

	deduped.sort((a, b) => (a.timeMs - b.timeMs) || (a.total - b.total));

	let maxSeenTotal = null;
	let tokensForDay = 0;

	for (const event of deduped) {
		const delta =
			maxSeenTotal === null ? event.total : Math.max(0, event.total - maxSeenTotal);
		maxSeenTotal = maxSeenTotal === null ? event.total : Math.max(maxSeenTotal, event.total);

		if (dateFormatter.format(new Date(event.timeMs)) === targetDate) {
			tokensForDay += delta;
		}
	}

	return tokensForDay;
}

async function main() {
	const args = parseArgs(process.argv.slice(2));
	if (args.help) {
		printHelp();
		return;
	}

	if (!args.date) {
		args.date = getDateInTimezone(args.timezone);
	}

	if (!isValidDate(args.date)) {
		throw new Error(`Invalid --date: ${args.date} (expected YYYY-MM-DD)`);
	}

	if (!fs.existsSync(args.sessionsRoot)) {
		throw new Error(`Sessions root not found: ${args.sessionsRoot}`);
	}

	const dateFormatter = getDateFormatter(args.timezone);
	const files = await collectRolloutFiles(args.sessionsRoot);

	const parsedFiles = [];
	for (const filePath of files) {
		parsedFiles.push(await parseRolloutFile(filePath));
	}

	const sessionAggregates = buildSessionAggregates(parsedFiles);

	const sessions = [];
	const projects = new Map();
	let totalTokens = 0;

	for (const agg of sessionAggregates) {
		const tokens = computeTokensForDay(agg.events, args.date, dateFormatter);
		if (tokens <= 0) continue;

		const sessionRow = {
			sessionId: agg.sessionId,
			sessionKey: agg.sessionKey,
			cwd: agg.cwd,
			tokens,
			sourceFiles: agg.sourceFiles.length,
		};
		sessions.push(sessionRow);
		totalTokens += tokens;
		projects.set(sessionRow.cwd, (projects.get(sessionRow.cwd) || 0) + tokens);
	}

	sessions.sort((a, b) => b.tokens - a.tokens);
	const projectRows = [...projects.entries()]
		.map(([cwd, tokens]) => ({ cwd, tokens }))
		.sort((a, b) => b.tokens - a.tokens);

	const summary = {
		date: args.date,
		timezone: args.timezone,
		sessionsRoot: args.sessionsRoot,
		totalTokens,
		sessionsCount: sessions.length,
		projects: projectRows,
		sessions,
	};

	if (args.json) {
		console.log(JSON.stringify(summary, null, 2));
		return;
	}

	console.log(`Token Usage Summary`);
	console.log(`Date: ${summary.date}`);
	console.log(`Timezone: ${summary.timezone}`);
	console.log(`Sessions with usage: ${summary.sessionsCount}`);
	console.log(`Total tokens: ${formatNumber(summary.totalTokens)}`);

	if (projectRows.length > 0) {
		console.log(`\nBy project:`);
		for (const row of projectRows) {
			console.log(`- ${row.cwd}: ${formatNumber(row.tokens)}`);
		}
	}

	if (sessions.length > 0) {
		console.log(`\nTop sessions:`);
		for (const [idx, session] of sessions.slice(0, args.limit).entries()) {
			console.log(
				`${idx + 1}. ${session.sessionId ?? "(unknown session)"} | ${formatNumber(session.tokens)} | ${session.cwd}`,
			);
		}
	}
}

main().catch((error) => {
	console.error(`Error: ${error instanceof Error ? error.message : String(error)}`);
	process.exit(1);
});
