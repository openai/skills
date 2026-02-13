/**
 * X API wrapper — search, threads, profiles, single tweets.
 * Uses Bearer token from env: X_BEARER_TOKEN
 */

import { readFileSync } from "fs";

const BASE = "https://api.x.com/2";
const RATE_DELAY_MS = 350;
const RECENT_MAX_RESULTS = 100;
const ARCHIVE_MAX_RESULTS = 100;

type SearchMode = "recent" | "archive";

function getToken(): string {
  if (process.env.X_BEARER_TOKEN) return process.env.X_BEARER_TOKEN;

  try {
    const envFile = readFileSync(`${process.env.HOME}/.config/env/global.env`, "utf-8");
    const match = envFile.match(/X_BEARER_TOKEN=["']?([^"'\n]+)/);
    if (match) return match[1];
  } catch {
    // Fall through to error.
  }

  throw new Error("X_BEARER_TOKEN not found in env or ~/.config/env/global.env");
}

async function sleep(ms: number) {
  return new Promise((r) => setTimeout(r, ms));
}

export interface Tweet {
  id: string;
  text: string;
  author_id: string;
  username: string;
  name: string;
  created_at: string;
  conversation_id: string;
  metrics: {
    likes: number;
    retweets: number;
    replies: number;
    quotes: number;
    impressions: number;
    bookmarks: number;
  };
  urls: string[];
  mentions: string[];
  hashtags: string[];
  tweet_url: string;
}

interface RawResponse {
  data?: any[] | Record<string, unknown>;
  includes?: { users?: any[] };
  meta?: { next_token?: string; result_count?: number };
}

function toDataArray(data: RawResponse["data"]): any[] {
  if (!data) return [];
  return Array.isArray(data) ? data : [data];
}

function parseTweets(raw: RawResponse): Tweet[] {
  const tweetRows = toDataArray(raw.data);
  if (tweetRows.length === 0) return [];

  const users: Record<string, any> = {};
  for (const user of raw.includes?.users || []) {
    users[user.id] = user;
  }

  return tweetRows.map((tweet: any) => {
    const user = users[tweet.author_id] || {};
    const metrics = tweet.public_metrics || {};

    return {
      id: tweet.id,
      text: tweet.text,
      author_id: tweet.author_id,
      username: user.username || "?",
      name: user.name || "?",
      created_at: tweet.created_at,
      conversation_id: tweet.conversation_id,
      metrics: {
        likes: metrics.like_count || 0,
        retweets: metrics.retweet_count || 0,
        replies: metrics.reply_count || 0,
        quotes: metrics.quote_count || 0,
        impressions: metrics.impression_count || 0,
        bookmarks: metrics.bookmark_count || 0,
      },
      urls: (tweet.entities?.urls || []).map((u: any) => u.expanded_url).filter(Boolean),
      mentions: (tweet.entities?.mentions || []).map((m: any) => m.username).filter(Boolean),
      hashtags: (tweet.entities?.hashtags || []).map((h: any) => h.tag).filter(Boolean),
      tweet_url: `https://x.com/${user.username || "?"}/status/${tweet.id}`,
    };
  });
}

const FIELDS =
  "tweet.fields=created_at,public_metrics,author_id,conversation_id,entities&expansions=author_id&user.fields=username,name,public_metrics";

/**
 * Parse relative time shorthand or ISO timestamp into ISO 8601.
 */
export function parseSince(since: string, nowMs: number = Date.now()): string | null {
  const match = since.match(/^(\d+)(m|h|d)$/);
  if (match) {
    const num = parseInt(match[1], 10);
    const unit = match[2];
    const deltaMs =
      unit === "m" ? num * 60_000 :
      unit === "h" ? num * 3_600_000 :
      num * 86_400_000;
    return new Date(nowMs - deltaMs).toISOString();
  }

  if (since.includes("T") || since.includes("-")) {
    const parsed = new Date(since);
    if (Number.isNaN(parsed.getTime())) return null;
    return parsed.toISOString();
  }

  return null;
}

async function apiGet(url: string): Promise<RawResponse> {
  const token = getToken();
  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (res.status === 429) {
    const reset = res.headers.get("x-rate-limit-reset");
    const waitSec = reset
      ? Math.max(parseInt(reset, 10) - Math.floor(Date.now() / 1000), 1)
      : 60;
    throw new Error(`Rate limited. Resets in ${waitSec}s`);
  }

  if (!res.ok) {
    const body = await res.text();
    throw new Error(`X API ${res.status}: ${body.slice(0, 200)}`);
  }

  return (await res.json()) as RawResponse;
}

export async function search(
  query: string,
  opts: {
    maxResults?: number;
    pages?: number;
    sortOrder?: "relevancy" | "recency";
    since?: string;
    mode?: SearchMode;
  } = {}
): Promise<Tweet[]> {
  const mode = opts.mode || "recent";
  const endpoint = mode === "archive" ? "all" : "recent";
  const maxPerRequest = mode === "archive" ? ARCHIVE_MAX_RESULTS : RECENT_MAX_RESULTS;
  const maxResults = Math.max(Math.min(opts.maxResults || 100, maxPerRequest), 10);
  const pages = opts.pages || 1;
  const sort = opts.sortOrder || "relevancy";
  const encoded = encodeURIComponent(query);

  let timeFilter = "";
  if (opts.since) {
    const startTime = parseSince(opts.since);
    if (startTime) {
      timeFilter = `&start_time=${encodeURIComponent(startTime)}`;
    }
  }

  let allTweets: Tweet[] = [];
  let nextToken: string | undefined;

  for (let page = 0; page < pages; page++) {
    const pagination = nextToken ? `&pagination_token=${encodeURIComponent(nextToken)}` : "";
    const url = `${BASE}/tweets/search/${endpoint}?query=${encoded}&max_results=${maxResults}&${FIELDS}&sort_order=${sort}${timeFilter}${pagination}`;

    const raw = await apiGet(url);
    allTweets.push(...parseTweets(raw));

    nextToken = raw.meta?.next_token;
    if (!nextToken) break;
    if (page < pages - 1) await sleep(RATE_DELAY_MS);
  }

  return allTweets;
}

/**
 * Merge root + replies into deterministic thread output.
 */
export function mergeThreadTweets(root: Tweet | null, replies: Tweet[]): Tweet[] {
  const merged = root ? [root, ...replies] : [...replies];
  return dedupe(merged).sort(
    (a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
  );
}

export async function thread(
  conversationId: string,
  opts: { pages?: number; mode?: SearchMode } = {}
): Promise<Tweet[]> {
  const replies = await search(`conversation_id:${conversationId}`, {
    pages: opts.pages || 2,
    sortOrder: "recency",
    mode: opts.mode || "recent",
  });

  let root: Tweet | null = null;
  try {
    root = await getTweet(conversationId);
  } catch {
    // Root tweet may be deleted or unavailable.
  }

  return mergeThreadTweets(root, replies);
}

export async function profile(
  username: string,
  opts: { count?: number; includeReplies?: boolean } = {}
): Promise<{ user: any; tweets: Tweet[] }> {
  const userUrl = `${BASE}/users/by/username/${username}?user.fields=public_metrics,description,created_at`;
  const userData = await apiGet(userUrl);

  if (!userData.data || Array.isArray(userData.data)) {
    throw new Error(`User @${username} not found`);
  }

  const user = userData.data;
  await sleep(RATE_DELAY_MS);

  const replyFilter = opts.includeReplies ? "" : " -is:reply";
  const query = `from:${username} -is:retweet${replyFilter}`;
  const tweets = await search(query, {
    maxResults: Math.min(opts.count || 20, 100),
    sortOrder: "recency",
    mode: "recent",
  });

  return { user, tweets };
}

export async function getTweet(tweetId: string): Promise<Tweet | null> {
  const url = `${BASE}/tweets/${tweetId}?${FIELDS}`;
  const raw = await apiGet(url);
  const parsed = parseTweets(raw);
  return parsed[0] || null;
}

export function sortBy(
  tweets: Tweet[],
  metric: "likes" | "impressions" | "retweets" | "replies" = "likes"
): Tweet[] {
  return [...tweets].sort((a, b) => b.metrics[metric] - a.metrics[metric]);
}

export function filterEngagement(
  tweets: Tweet[],
  opts: { minLikes?: number; minImpressions?: number }
): Tweet[] {
  return tweets.filter((tweet) => {
    if (opts.minLikes && tweet.metrics.likes < opts.minLikes) return false;
    if (opts.minImpressions && tweet.metrics.impressions < opts.minImpressions) return false;
    return true;
  });
}

export function dedupe(tweets: Tweet[]): Tweet[] {
  const seen = new Set<string>();
  return tweets.filter((tweet) => {
    if (seen.has(tweet.id)) return false;
    seen.add(tweet.id);
    return true;
  });
}
