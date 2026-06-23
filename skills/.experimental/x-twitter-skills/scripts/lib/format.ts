/**
 * Format tweets for terminal and markdown output.
 */

import type { Tweet } from "./api";

interface ScoredTweetLike {
  signalScore?: number;
  signalReasons?: string[];
}

function isScoredTweet(tweet: Tweet | ScoredTweetLike): tweet is ScoredTweetLike & Tweet {
  return (
    typeof tweet.signalScore === "number" &&
    Number.isFinite(tweet.signalScore) &&
    Array.isArray(tweet.signalReasons)
  );
}

function signalLine(tweet: Tweet | ScoredTweetLike): string {
  if (!isScoredTweet(tweet)) return "";
  const score = tweet.signalScore.toFixed(1);
  const reasons = tweet.signalReasons?.slice(0, 3).join(", ");
  return `· score ${score} ${reasons ? `(${reasons})` : ""}`.trim();
}

function compactNumber(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`;
  return String(n);
}

function timeAgo(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(diff / 60_000);
  if (mins < 60) return `${mins}m`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h`;
  const days = Math.floor(hours / 24);
  return `${days}d`;
}

function safeHostname(url: string): string {
  try {
    return new URL(url).hostname;
  } catch {
    return "link";
  }
}

export function formatTweetTelegram(
  t: Tweet | ScoredTweetLike,
  index?: number,
  opts: { full?: boolean; showSignal?: boolean } = {}
): string {
  const prefix = index !== undefined ? `${index + 1}. ` : "";
  const engagement = `${compactNumber(t.metrics.likes)}❤️ ${compactNumber(t.metrics.impressions)}👁`;
  const time = timeAgo(t.created_at);
  const text = opts.full || t.text.length <= 200 ? t.text : `${t.text.slice(0, 197)}...`;
  const cleanText = text.replace(/https:\/\/t\.co\/\S+/g, "").trim();
  const signal = opts.showSignal ? ` ${signalLine(t)}` : "";

  let out = `${prefix}@${t.username} (${engagement} · ${time}${signal})\n${cleanText}`;
  if (t.urls.length > 0) {
    out += `\n🔗 ${t.urls[0]}`;
  }
  out += `\n${t.tweet_url}`;
  return out;
}

export function formatResultsTelegram(
  tweets: Array<Tweet | ScoredTweetLike>,
  opts: { query?: string; limit?: number; showSignal?: boolean } = {}
): string {
  const limit = opts.limit || 15;
  const shown = tweets.slice(0, limit);

  let out = "";
  if (opts.query) {
    out += `🔍 "${opts.query}" — ${tweets.length} results\n\n`;
  }

  out += shown
    .map((tweet, i) => formatTweetTelegram(tweet, i, { showSignal: opts.showSignal }))
    .join("\n\n");
  if (tweets.length > limit) {
    out += `\n\n... +${tweets.length - limit} more`;
  }

  return out;
}

export function formatTweetMarkdown(
  t: Tweet | ScoredTweetLike,
  opts: { showSignal?: boolean } = {}
): string {
  const engagement = `${t.metrics.likes}L ${t.metrics.impressions}I`;
  const cleanText = t.text.replace(/https:\/\/t\.co\/\S+/g, "").trim();
  const quoted = cleanText.replace(/\n/g, "\n  > ");
  const signal = opts.showSignal ? ` ${signalLine(t)}` : "";

  let out = `- **@${t.username}** (${engagement} ${signal}) [Tweet](${t.tweet_url})\n  > ${quoted}`;
  if (t.urls.length > 0) {
    out += `\n  Links: ${t.urls.map((u) => `[${safeHostname(u)}](${u})`).join(", ")}`;
  }

  return out;
}

export function formatResearchMarkdown(
  query: string,
  tweets: Array<Tweet | ScoredTweetLike>,
  opts: {
    themes?: { title: string; tweetIds: string[] }[];
    apiCalls?: number;
    queries?: string[];
    showSignal?: boolean;
  } = {}
): string {
  const date = new Date().toISOString().split("T")[0];
  const topSortLabel = opts.showSignal ? "signal" : "engagement";

  let out = `# X/Twitter Skills Research: ${query}\n\n`;
  out += `**Date:** ${date}\n`;
  out += `**Tweets found:** ${tweets.length}\n\n`;

  if (opts.themes && opts.themes.length > 0) {
    for (const theme of opts.themes) {
      out += `## ${theme.title}\n\n`;
      const themeTweets = theme.tweetIds
        .map((id) => tweets.find((tweet) => tweet.id === id))
        .filter(Boolean) as Array<Tweet | ScoredTweetLike>;
      out += themeTweets
        .map((tweet) => formatTweetMarkdown(tweet, { showSignal: opts.showSignal }))
        .join("\n\n");
      out += "\n\n";
    }
  } else {
    out += `## Top Results (by ${topSortLabel})\n\n`;
    out += tweets
      .slice(0, 30)
      .map((tweet) => formatTweetMarkdown(tweet, { showSignal: opts.showSignal }))
      .join("\n\n");
    out += "\n\n";
  }

  out += "---\n\n## Research Metadata\n";
  out += `- **Query:** ${query}\n`;
  out += `- **Date:** ${date}\n`;
  if (opts.apiCalls) out += `- **API calls:** ${opts.apiCalls}\n`;
  out += `- **Tweets scanned:** ${tweets.length}\n`;
  out += `- **Est. cost:** ~$${(tweets.length * 0.005).toFixed(2)}\n`;
  if (opts.queries) {
    out += "- **Search queries:**\n";
    for (const q of opts.queries) {
      out += `  - \`${q}\`\n`;
    }
  }

  return out;
}

export function formatProfileTelegram(user: any, tweets: Tweet[]): string {
  const m = user.public_metrics || {};
  let out = `👤 @${user.username} — ${user.name}\n`;
  out += `${compactNumber(m.followers_count || 0)} followers · ${compactNumber(m.tweet_count || 0)} tweets\n`;
  if (user.description) {
    out += `${user.description.slice(0, 150)}\n`;
  }
  out += "\nRecent:\n\n";
  out += tweets.slice(0, 10).map((tweet, i) => formatTweetTelegram(tweet, i)).join("\n\n");

  return out;
}
