/**
 * x-search — CLI for X/Twitter research.
 */

import { existsSync, mkdirSync, writeFileSync } from "fs";
import { dirname, join } from "path";
import { fileURLToPath } from "url";
import * as api from "./lib/api";
import * as cache from "./lib/cache";
import * as fmt from "./lib/format";
import * as planner from "./lib/planner";
import * as brief from "./lib/brief";
import * as briefHistory from "./lib/brief-history";
import { type ScoredTweet, rankBySignal, SIGNAL_DEFAULT_MIN_SCORE } from "./lib/signal";
import { runWatchlistCommand } from "./lib/watchlist";

const THIS_DIR = dirname(fileURLToPath(import.meta.url));
const SKILL_DIR = join(THIS_DIR, "..");
const DRAFTS_DIR =
  process.env.X_TWITTER_SKILLS_DRAFTS_DIR || join(SKILL_DIR, "data", "drafts");
const BRIEF_HISTORY_DIR = join(SKILL_DIR, "data", "brief-history");
const SORT_OPTIONS = ["likes", "impressions", "retweets", "recent", "signal"] as const;
type SortOption = (typeof SORT_OPTIONS)[number];
const SEARCH_PAGE_LIMIT = { min: 1, max: 5 } as const;
const DEFAULT_SEARCH_LIMIT = 15;
const DEFAULT_PLAN_QUERIES = 5;
const DEFAULT_BRIEF_PAGES = 1;
const DEFAULT_CACHE_MIN = 15;

const args = process.argv.slice(2);
const command = args[0];

function ensureDir(path: string) {
  if (!existsSync(path)) mkdirSync(path, { recursive: true });
}

function clamp(n: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, n));
}

function slugify(text: string): string {
  return text
    .replace(/[^a-zA-Z0-9]+/g, "-")
    .replace(/^-|-$/g, "")
    .slice(0, 50)
    .toLowerCase();
}

function getFlag(name: string): boolean {
  const idx = args.indexOf(`--${name}`);
  if (idx >= 0) {
    args.splice(idx, 1);
    return true;
  }
  return false;
}

function getOpt(name: string): string | undefined {
  const idx = args.indexOf(`--${name}`);
  if (idx >= 0) {
    if (idx + 1 >= args.length) {
      console.error(`Missing value for --${name}.`);
      process.exit(1);
    }
    if (args[idx + 1]?.startsWith("--")) {
      console.error(`Missing value for --${name}.`);
      process.exit(1);
    }

    const val = args[idx + 1];
    args.splice(idx, 2);
    return val;
  }
  return undefined;
}

function parseIntOption(name: string): number | undefined {
  const raw = getOpt(name);
  if (raw === undefined) return undefined;
  if (!/^\d+$/.test(raw)) {
    console.error(`Invalid --${name} value "${raw}". Expected a positive integer.`);
    process.exit(1);
  }
  const parsed = parseInt(raw, 10);
  if (parsed <= 0) {
    console.error(`Invalid --${name} value "${raw}". Expected a positive integer.`);
    process.exit(1);
  }
  return parsed;
}

function parseIntOptionOrDefault(name: string, fallback: number): number {
  return parseIntOption(name) ?? fallback;
}

function parseFloatOption(name: string, opts: { positive?: boolean } = {}): number | undefined {
  const raw = getOpt(name);
  if (raw === undefined) return undefined;
  const parsed = Number(raw);
  if (!Number.isFinite(parsed)) {
    console.error(`Invalid --${name} value "${raw}". Expected a number.`);
    process.exit(1);
  }

  if (opts.positive && parsed <= 0) {
    console.error(`Invalid --${name} value "${raw}". Expected a positive number.`);
    process.exit(1);
  }

  return parsed;
}

function parseSinceOption(name: string): string | undefined {
  const raw = getOpt(name);
  if (raw === undefined) return undefined;
  const normalized = api.parseSince(raw);
  if (!normalized) {
    console.error(`Invalid --${name} value "${raw}". Use a value like 30m, 2h, 7d, or ISO-8601.`);
    process.exit(1);
  }
  return normalized;
}

function parseSortOption(): SortOption {
  const sort = getOpt("sort") || "likes";
  if (!SORT_OPTIONS.includes(sort as SortOption)) {
    console.error(`Invalid --sort value "${sort}". Use one of: likes, impressions, retweets, recent, signal.`);
    process.exit(1);
  }
  return sort as SortOption;
}

function parseFloatOptionStrict(name: string, opts: { positive?: boolean } = {}): number | undefined {
  const raw = getOpt(name);
  if (raw === undefined) return undefined;
  const parsed = Number.parseFloat(raw);
  if (!Number.isFinite(parsed)) {
    console.error(`Invalid --${name} value "${raw}". Expected a number.`);
    process.exit(1);
  }
  if (opts.positive && parsed < 0) {
    console.error(`Invalid --${name} value "${raw}". Expected a non-negative number.`);
    process.exit(1);
  }
  return parsed;
}

function readSubjectArg(): string {
  return args
    .slice(1)
    .filter((a) => !a.startsWith("--"))
    .join(" ")
    .trim();
}

async function cmdSearch() {
  const quick = getFlag("quick");
  const quality = getFlag("quality");
  const fromUser = getOpt("from");
  const archive = getFlag("archive");

  const sortOpt = parseSortOption();
  const minLikes = parseIntOption("min-likes") || 0;
  const minImpressions = parseIntOption("min-impressions") || 0;
  const minScore =
    parseFloatOptionStrict("min-score", { positive: true }) ?? SIGNAL_DEFAULT_MIN_SCORE;
  let pages = clamp(parseIntOptionOrDefault("pages", 1), SEARCH_PAGE_LIMIT.min, SEARCH_PAGE_LIMIT.max);
  let limit = clamp(parseIntOptionOrDefault("limit", DEFAULT_SEARCH_LIMIT), 1, 200);
  const since = parseSinceOption("since");
  const noReplies = getFlag("no-replies");
  const noRetweets = getFlag("no-retweets");
  const save = getFlag("save");
  const asJson = getFlag("json");
  const asMarkdown = getFlag("markdown");

  if (quick) {
    pages = 1;
    limit = Math.min(limit, 10);
  }

  let query = readSubjectArg();
  if (!query) {
    console.error("Usage: x-search.ts search <query> [options]");
    process.exit(1);
  }

  if (fromUser && !query.toLowerCase().includes("from:")) {
    query += ` from:${fromUser.replace(/^@/, "")}`;
  }

  if (!query.includes("is:retweet") && !noRetweets) {
    query += " -is:retweet";
  }
  if (quick && !query.includes("is:reply")) {
    query += " -is:reply";
  } else if (noReplies && !query.includes("is:reply")) {
    query += " -is:reply";
  }

  const mode: "recent" | "archive" = archive ? "archive" : "recent";
  const cacheTtlMs = quick ? 3_600_000 : 900_000;
  const scoreParam = sortOpt === "signal" ? `&minScore=${minScore.toFixed(3)}` : "";
  const cacheParams = `mode=${mode}&sort=${sortOpt}&pages=${pages}&since=${since || "none"}${scoreParam}`;

  const cached = cache.get(query, cacheParams, cacheTtlMs);
  let tweets: api.Tweet[];
  let scoredTweets: ScoredTweet[] | null = null;

  if (cached) {
    tweets = cached;
    console.error(`(cached — ${tweets.length} tweets)`);
  } else {
    tweets = await api.search(query, {
      pages,
      sortOrder: sortOpt === "recent" ? "recency" : "relevancy",
      since: since || undefined,
      mode,
    });
    cache.set(query, cacheParams, tweets);
  }

  const rawTweetCount = tweets.length;

  if (minLikes > 0 || minImpressions > 0) {
    tweets = api.filterEngagement(tweets, {
      minLikes: minLikes || undefined,
      minImpressions: minImpressions || undefined,
    });
  }

  if (quality) {
    tweets = api.filterEngagement(tweets, { minLikes: 10 });
  }

  if (sortOpt === "signal") {
    scoredTweets = rankBySignal(tweets, {
      minScore,
    });
    tweets = scoredTweets;
  } else if (sortOpt !== "recent") {
    tweets = api.sortBy(tweets, sortOpt as "likes" | "impressions" | "retweets");
  }

  tweets = api.dedupe(tweets);
  const display = scoredTweets ? scoredTweets : (tweets as api.Tweet[]);

  if (asJson) {
    console.log(JSON.stringify(display.slice(0, limit), null, 2));
  } else if (asMarkdown) {
    console.log(fmt.formatResearchMarkdown(query, display, { queries: [query], showSignal: sortOpt === "signal" }));
  } else {
    console.log(
      fmt.formatResultsTelegram(display, { query, limit, showSignal: sortOpt === "signal" })
    );
  }

  if (save) {
    ensureDir(DRAFTS_DIR);
    const date = new Date().toISOString().split("T")[0];
    const path = join(DRAFTS_DIR, `x-twitter-skills-${slugify(query)}-${date}.md`);
    writeFileSync(
      path,
      fmt.formatResearchMarkdown(query, display, {
        queries: [query],
        showSignal: sortOpt === "signal",
      })
    );
    console.error(`\nSaved to ${path}`);
  }

  const cost = (rawTweetCount * 0.005).toFixed(2);
  const modeLabel = archive ? "archive" : "recent";
  if (quick) {
    console.error(`\n⚡ quick mode · ${modeLabel} search · ${rawTweetCount} tweets read (~$${cost})`);
  } else {
    console.error(`\n📊 ${modeLabel} search · ${rawTweetCount} tweets read · est. cost ~$${cost}`);
  }

  const finalCount = display.length;
  const filtered = rawTweetCount !== finalCount ? ` -> ${finalCount} after filters` : "";
  const sinceLabel = since ? ` | since ${since}` : "";
  const scoreLabel = sortOpt === "signal" ? ` | min-score ${minScore}` : "";
  console.error(
    `${rawTweetCount} tweets${filtered} | sorted by ${sortOpt} | ${pages} page(s)${scoreLabel}${sinceLabel}`
  );
}

function cmdPlan() {
  const asJson = getFlag("json");
  const maxQueries = clamp(
    parseIntOption("max-queries") || DEFAULT_PLAN_QUERIES,
    2,
    10
  );

  const question = readSubjectArg();
  if (!question) {
    console.error("Usage: x-search.ts plan <research-question> [--max-queries N] [--json]");
    process.exit(1);
  }

  const plan = planner.buildResearchPlan(question, { maxQueries });

  if (asJson) {
    console.log(JSON.stringify(plan, null, 2));
  } else {
    console.log(planner.formatPlanMarkdown(plan));
  }
}

async function cmdBrief() {
  const asJson = getFlag("json");
  const save = getFlag("save");
  const compareLast = getFlag("compare-last");
  const archive = getFlag("archive");
  const dryRun = getFlag("dry-run");
  const since = parseSinceOption("since") || "7d";
  const pages = clamp(parseIntOption("pages") || DEFAULT_BRIEF_PAGES, 1, 5);
  const maxQueries = clamp(
    parseIntOption("max-queries") || DEFAULT_PLAN_QUERIES,
    2,
    10
  );
  const cacheTtlMs = clamp(parseIntOption("cache-min") || DEFAULT_CACHE_MIN, 1, 720) * 60_000;
  const maxCost = parseFloatOption("max-cost", { positive: true });
  const minScore = parseFloatOptionStrict("min-score", { positive: true }) ?? SIGNAL_DEFAULT_MIN_SCORE;

  const question = readSubjectArg();
  if (!question) {
    console.error("Usage: x-search.ts brief <research-question> [options]");
    process.exit(1);
  }

  const mode: "recent" | "archive" = archive ? "archive" : "recent";
  const plan = planner.buildResearchPlan(question, { maxQueries });
  const estimatedWorstCaseCost = briefHistory.estimateWorstCaseCost(plan.queries.length, pages);
  if (maxCost !== undefined && Number.isFinite(maxCost) && maxCost > 0 && estimatedWorstCaseCost > maxCost) {
    console.error(
      `Refusing run: estimated worst-case read cost ~$${estimatedWorstCaseCost.toFixed(2)} exceeds --max-cost ${maxCost.toFixed(2)}`
    );
    console.error("Reduce --pages/--max-queries or use a higher --max-cost.");
    process.exit(1);
  }

  if (dryRun) {
    if (asJson) {
      console.log(
        JSON.stringify(
          {
            question,
            mode,
            since,
            pages,
            maxQueries,
            estimatedWorstCaseCost,
            plan,
          },
          null,
          2
        )
      );
    } else {
      console.log(planner.formatPlanMarkdown(plan));
      console.log(`Estimated worst-case reads: ${plan.queries.length * pages * 100}`);
      console.log(`Estimated worst-case cost: ~$${estimatedWorstCaseCost.toFixed(2)}`);
    }
    return;
  }

  const allTweets: api.Tweet[] = [];
  const queryRuns: brief.BriefQueryRun[] = [];

  for (const q of plan.queries) {
    const params = `brief=1&mode=${mode}&pages=${pages}&since=${since}`;
    let tweets = cache.get(q.query, params, cacheTtlMs);
    const cached = !!tweets;

    if (!tweets) {
      tweets = await api.search(q.query, {
        pages,
        sortOrder: "relevancy",
        since,
        mode,
      });
      cache.set(q.query, params, tweets);
    }

    queryRuns.push({
      id: q.id,
      label: q.label,
      query: q.query,
      rawCount: tweets.length,
      cached,
    });

    allTweets.push(...tweets);
  }

  const report = brief.createBriefReport({
    question,
    mode,
    since,
    plan,
    queryRuns,
    tweets: allTweets,
    minSignalScore: minScore,
  });

  const slug = slugify(question);
  const snapshotPath = join(BRIEF_HISTORY_DIR, `${slug}.json`);
  const previousSnapshot = compareLast ? briefHistory.readSnapshot(snapshotPath) : null;
  const currentSnapshot = briefHistory.createSnapshot(report);
  ensureDir(BRIEF_HISTORY_DIR);
  briefHistory.writeSnapshot(snapshotPath, currentSnapshot);
  const delta = previousSnapshot
    ? briefHistory.compareSnapshots(previousSnapshot, currentSnapshot)
    : null;
  const markdownBody = `${brief.formatBriefMarkdown(report)}${
    delta ? `\n\n${briefHistory.formatDeltaMarkdown(delta)}` : ""
  }`;

  if (asJson) {
    const jsonOut: Record<string, unknown> = {
      ...report,
      estimatedWorstCaseCost,
    };
    if (delta) jsonOut.delta = delta;
    console.log(JSON.stringify(jsonOut, null, 2));
  } else {
    console.log(markdownBody);
    if (compareLast && !previousSnapshot) {
      console.error("(No prior brief snapshot found for this question. Baseline saved for next run.)");
    }
  }

  if (save) {
    ensureDir(DRAFTS_DIR);
    const date = new Date().toISOString().split("T")[0];
    const path = join(DRAFTS_DIR, `x-brief-${slug}-${date}.md`);
    const body = asJson
      ? JSON.stringify(
          {
            ...report,
            estimatedWorstCaseCost,
            ...(delta ? { delta } : {}),
          },
          null,
          2
        )
      : markdownBody;
    writeFileSync(path, body);
    console.error(`\nSaved to ${path}`);
  }
}

async function cmdThread() {
  const tweetId = args[1];
  if (!tweetId) {
    console.error("Usage: x-search.ts thread <tweet_id>");
    process.exit(1);
  }

  const pages = clamp(parseIntOptionOrDefault("pages", 2), SEARCH_PAGE_LIMIT.min, SEARCH_PAGE_LIMIT.max);
  const archive = getFlag("archive");
  const tweets = await api.thread(tweetId, {
    pages,
    mode: archive ? "archive" : "recent",
  });

  if (tweets.length === 0) {
    console.log("No tweets found in thread.");
    return;
  }

  console.log(`🧵 Thread (${tweets.length} tweets)\n`);
  for (const tweet of tweets) {
    console.log(fmt.formatTweetTelegram(tweet, undefined, { full: true }));
    console.log();
  }
}

async function cmdProfile() {
  const username = args[1]?.replace(/^@/, "");
  if (!username) {
    console.error("Usage: x-search.ts profile <username>");
    process.exit(1);
  }

  const count = clamp(parseIntOptionOrDefault("count", 20), 1, 100);
  const includeReplies = getFlag("replies");
  const asJson = getFlag("json");

  const { user, tweets } = await api.profile(username, {
    count,
    includeReplies,
  });

  if (asJson) {
    console.log(JSON.stringify({ user, tweets }, null, 2));
  } else {
    console.log(fmt.formatProfileTelegram(user, tweets));
  }
}

async function cmdTweet() {
  const tweetId = args[1];
  if (!tweetId) {
    console.error("Usage: x-search.ts tweet <tweet_id>");
    process.exit(1);
  }

  const tweet = await api.getTweet(tweetId);
  if (!tweet) {
    console.log("Tweet not found.");
    return;
  }

  if (getFlag("json")) {
    console.log(JSON.stringify(tweet, null, 2));
  } else {
    console.log(fmt.formatTweetTelegram(tweet, undefined, { full: true }));
  }
}

function cmdCache() {
  const sub = args[1];
  if (sub === "clear") {
    console.log(`Cleared ${cache.clear()} cached entries.`);
  } else {
    console.log(`Pruned ${cache.prune()} expired entries.`);
  }
}

function usage() {
  console.log(`x-search — X/Twitter research CLI

Commands:
  search <query> [options]      Search tweets
  plan <question> [options]     Build multi-query research strategy
  brief <question> [options]    Run multi-query briefing workflow
  thread <tweet_id>             Fetch full conversation thread
  profile <username>            Recent tweets from a user
  tweet <tweet_id>              Fetch a single tweet
  watchlist                     Show watchlist
  watchlist add <user> [note]   Add user to watchlist
  watchlist remove <user>       Remove user from watchlist
  watchlist check               Check recent from all watchlist accounts
  cache clear                   Clear search cache

  Search options:
  --sort likes|impressions|retweets|recent|signal   (default: likes)
  --since 1h|3h|12h|1d|7d|<ISO>
  --archive                    Use full-archive endpoint
  --min-likes N                Filter minimum likes
  --min-impressions N          Filter minimum impressions
  --min-score N                Only show signal posts with score >= N (only for --sort signal)
  --pages N                    Pages to fetch, 1-5 (default: 1)
  --limit N                    Results to display (default: 15)
  --quick                      Quick mode: 1 page, max 10 results
  --from <username>            Shorthand for from:username
  --quality                    Filter low-engagement tweets (>=10 likes)
  --no-replies                 Exclude replies
  --save                       Save markdown report to drafts dir
  --json                       Raw JSON output
  --markdown                   Markdown output

Plan options:
  --max-queries N              Planned query count (2-10, default 5)
  --json                       Output JSON plan

Brief options:
  --since <window>             Time window (default 7d)
  --archive                    Use full-archive endpoint
  --pages N                    Pages per planned query (1-5, default 1)
  --max-queries N              Planned query count (2-10, default 5)
  --max-cost USD               Abort if worst-case read cost exceeds budget
  --min-score N                Min signal score threshold for brief ranking
  --cache-min N                Cache TTL minutes (default 15)
  --compare-last               Compare against previous snapshot for same question
  --dry-run                    Print plan + estimated cost only, skip API calls
  --save                       Save brief to drafts dir
  --json                       Output machine-readable JSON`);
}

async function main() {
  switch (command) {
    case "search":
      await cmdSearch();
      break;
    case "plan":
      cmdPlan();
      break;
    case "brief":
      await cmdBrief();
      break;
    case "thread":
      await cmdThread();
      break;
    case "profile":
      await cmdProfile();
      break;
    case "tweet":
      await cmdTweet();
      break;
    case "watchlist":
      await runWatchlistCommand(args, {
        watchlistPath: join(SKILL_DIR, "data", "watchlist.json"),
        profile: api.profile,
        formatTweet: fmt.formatTweetTelegram,
      });
      break;
    case "cache":
      cmdCache();
      break;
    default:
      usage();
  }
}

main().catch((e) => {
  console.error(`Error: ${e.message}`);
  process.exit(1);
});
