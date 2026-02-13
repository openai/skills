import type { Tweet } from "./api";
import { rankBySignal } from "./signal";
import type { ScoredTweet } from "./signal";
import type { ResearchPlan } from "./planner";

export interface BriefQueryRun {
  id: string;
  label: string;
  query: string;
  rawCount: number;
  cached: boolean;
}

export interface BriefSignalSummary {
  candidateCount: number;
  scoredCount: number;
  minScore: number;
  maxScore: number;
  medianScore: number;
}

export interface BriefReport {
  question: string;
  generatedAt: string;
  mode: "recent" | "archive";
  since?: string;
  uniqueTweetCount: number;
  rawTweetReads: number;
  plan: ResearchPlan;
  queryRuns: BriefQueryRun[];
  topVoices: Array<{
    username: string;
    postCount: number;
    likes: number;
    impressions: number;
    score: number;
  }>;
  topDomains: Array<{ domain: string; count: number }>;
  themes: Array<{ theme: string; count: number }>;
  polarity: {
    positiveExamples: ScoredTweet[];
    negativeExamples: ScoredTweet[];
  };
  topSignals: ScoredTweet[];
  signalSummary: BriefSignalSummary;
}

const THEME_RULES: Array<{ name: string; regex: RegExp }> = [
  { name: "Reliability", regex: /\b(bug|issue|broken|outage|fail|error|incident|regression)\b/i },
  { name: "Launches", regex: /\b(launch|release|shipped|announce|ga|beta|roadmap)\b/i },
  { name: "Performance", regex: /\b(fast|faster|latency|benchmark|throughput|perf)\b/i },
  { name: "Security", regex: /\b(security|vuln|vulnerability|exploit|hack|breach|risk)\b/i },
  { name: "Economics", regex: /\b(price|pricing|cost|revenue|fees|margin|business)\b/i },
];

const POSITIVE_REGEX = /\b(love|great|impressive|bullish|works|fast|better|win|excellent|solid)\b/i;
const NEGATIVE_REGEX = /\b(bug|broken|scam|slow|hate|concern|issue|bad|worse|regression|risk|downtime)\b/i;

function safeDomain(url: string): string | null {
  try {
    return new URL(url).hostname.toLowerCase();
  } catch {
    return null;
  }
}

function dedupeTweets(tweets: Tweet[]): Tweet[] {
  const seen = new Set<string>();
  const out: Tweet[] = [];
  for (const tweet of tweets) {
    if (seen.has(tweet.id)) continue;
    seen.add(tweet.id);
    out.push(tweet);
  }
  return out;
}

function signalSummaryFromRanked(scored: ScoredTweet[], candidates: number): BriefSignalSummary {
  if (scored.length === 0) {
    return {
      candidateCount: candidates,
      scoredCount: 0,
      minScore: 0,
      maxScore: 0,
      medianScore: 0,
    };
  }

  const sorted = [...scored].map((tweet) => tweet.signalScore).sort((a, b) => a - b);
  const mid = sorted[Math.floor(sorted.length / 2)] ?? 0;

  return {
    candidateCount: candidates,
    scoredCount: scored.length,
    minScore: sorted[0] ?? 0,
    maxScore: sorted[sorted.length - 1] ?? 0,
    medianScore: mid,
  };
}

export function createBriefReport(input: {
  question: string;
  mode: "recent" | "archive";
  since?: string;
  plan: ResearchPlan;
  queryRuns: BriefQueryRun[];
  tweets: Tweet[];
  minSignalScore?: number;
}): BriefReport {
  const uniqueTweets = dedupeTweets(input.tweets);
  const rankedBySignal = rankBySignal(uniqueTweets, {
    minScore: input.minSignalScore,
  });

  const voiceMap = new Map<string, { postCount: number; likes: number; impressions: number; score: number }>();
  for (const tweet of rankedBySignal) {
    const key = tweet.username.toLowerCase();
    const curr = voiceMap.get(key) || { postCount: 0, likes: 0, impressions: 0, score: 0 };
    curr.postCount += 1;
    curr.likes += tweet.metrics.likes;
    curr.impressions += tweet.metrics.impressions;
    curr.score += tweet.signalScore;
    voiceMap.set(key, curr);
  }

  const topVoices = [...voiceMap.entries()]
    .map(([username, stats]) => ({ username, ...stats }))
    .sort((a, b) => b.score - a.score)
    .slice(0, 8);

  const domainMap = new Map<string, number>();
  for (const tweet of uniqueTweets) {
    for (const url of tweet.urls) {
      const domain = safeDomain(url);
      if (!domain) continue;
      domainMap.set(domain, (domainMap.get(domain) || 0) + 1);
    }
  }

  const topDomains = [...domainMap.entries()]
    .map(([domain, count]) => ({ domain, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 8);

  const themeMap = new Map<string, number>();
  for (const tweet of uniqueTweets) {
    for (const rule of THEME_RULES) {
      if (rule.regex.test(tweet.text)) {
        themeMap.set(rule.name, (themeMap.get(rule.name) || 0) + 1);
      }
    }
  }

  const themes = [...themeMap.entries()]
    .map(([theme, count]) => ({ theme, count }))
    .sort((a, b) => b.count - a.count);

  const rankedText = rankedBySignal;
  const positiveExamples = rankedText.filter((t) => POSITIVE_REGEX.test(t.text)).slice(0, 3);
  const negativeExamples = rankedText.filter((t) => NEGATIVE_REGEX.test(t.text)).slice(0, 3);

  return {
    question: input.question,
    generatedAt: new Date().toISOString(),
    mode: input.mode,
    since: input.since,
    uniqueTweetCount: uniqueTweets.length,
    rawTweetReads: input.queryRuns.reduce((sum, run) => sum + run.rawCount, 0),
    plan: input.plan,
    queryRuns: input.queryRuns,
    topVoices,
    topDomains,
    themes,
    polarity: {
      positiveExamples,
      negativeExamples,
    },
    topSignals: rankedText.slice(0, 10),
    signalSummary: signalSummaryFromRanked(rankedBySignal, uniqueTweets.length),
  };
}

function formatTweetLine(tweet: ScoredTweet): string {
  const reasons = tweet.signalReasons.length > 0 ? ` · ${tweet.signalReasons.slice(0, 2).join(", ")}` : "";
  return `- @${tweet.username} (${tweet.metrics.likes}L/${tweet.metrics.impressions}I, score ${tweet.signalScore.toFixed(
    1
  )}${reasons}) [Tweet](${tweet.tweet_url})`;
}

function formatSignalSummary(summary: BriefSignalSummary): string {
  return `- Signal candidates: ${summary.candidateCount}\n- Scored candidates: ${summary.scoredCount}\n- Score range: ${summary.minScore.toFixed(1)} → ${summary.maxScore.toFixed(
    1
  )}\n- Median score: ${summary.medianScore.toFixed(1)}\n`;
}

export function formatBriefMarkdown(report: BriefReport): string {
  let out = `# X Brief: ${report.question}\n\n`;
  out += `- Generated: ${report.generatedAt}\n`;
  out += `- Mode: ${report.mode}`;
  if (report.since) out += ` (since ${report.since})`;
  out += "\n";
  out += `- Unique tweets: ${report.uniqueTweetCount}\n`;
  out += `- Raw tweet reads: ${report.rawTweetReads}\n`;
  out += `- Est. read cost: ~$${(report.rawTweetReads * 0.005).toFixed(2)}\n\n`;

  out += "## Signal Quality\n\n";
  out += `${formatSignalSummary(report.signalSummary)}\n`;

  out += "## Query Ledger\n\n";
  for (const run of report.queryRuns) {
    const cacheTag = run.cached ? "cached" : "live";
    out += `- ${run.label}: ${run.rawCount} tweets (${cacheTag})\n`;
    out += `  - \`${run.query}\`\n`;
  }
  out += "\n";

  out += "## Top Voices\n\n";
  if (report.topVoices.length === 0) {
    out += "- None\n\n";
  } else {
    for (const voice of report.topVoices) {
      out += `- @${voice.username}: ${voice.postCount} posts, ${voice.likes} likes, ${voice.impressions} impressions\n`;
    }
    out += "\n";
  }

  out += "## Top Domains\n\n";
  if (report.topDomains.length === 0) {
    out += "- None\n\n";
  } else {
    for (const domain of report.topDomains) {
      out += `- ${domain.domain}: ${domain.count}\n`;
    }
    out += "\n";
  }

  out += "## Theme Distribution\n\n";
  if (report.themes.length === 0) {
    out += "- No clear repeated themes detected\n\n";
  } else {
    for (const theme of report.themes) {
      out += `- ${theme.theme}: ${theme.count}\n`;
    }
    out += "\n";
  }

  out += "## Example Positive Takes\n\n";
  if (report.polarity.positiveExamples.length === 0) {
    out += "- None\n\n";
  } else {
    for (const tweet of report.polarity.positiveExamples) {
      out += `${formatTweetLine(tweet)}\n`;
    }
    out += "\n";
  }

  out += "## Example Critical Takes\n\n";
  if (report.polarity.negativeExamples.length === 0) {
    out += "- None\n\n";
  } else {
    for (const tweet of report.polarity.negativeExamples) {
      out += `${formatTweetLine(tweet)}\n`;
    }
    out += "\n";
  }

  out += "## Top Signal Posts\n\n";
  for (const tweet of report.topSignals) {
    out += `${formatTweetLine(tweet)}\n`;
  }

  return out;
}
