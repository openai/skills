import type { Tweet } from "./api";

export const SIGNAL_DEFAULT_MIN_SCORE = 0;

export interface ScoredTweet extends Tweet {
  signalScore: number;
  signalReasons: string[];
  signalBreakdown: {
    engagement: number;
    recency: number;
    actionability: number;
    quality: number;
  };
}

const ONE_HOUR_MS = 60 * 60 * 1000;
const MAX_REASON_COUNT = 4;
const CLAIM_KEYWORDS =
  /\b(announcement|release|launched|launch|ship|shipping|regression|bug|outage|issue|incident|pricing|risk|rollback|security|downtime|benchmark|evidence|postmortem|patch|update)\b/i;
const VERIFIED_PHRASE_KEYWORDS = /\b(according|based on|confirmed|results|we found|verified|proof|source|docs|release note)\b/i;
const TRUSTED_DOMAINS = new Set([
  "github.com",
  "arxiv.org",
  "docs.google.com",
  "openai.com",
  "x.com",
  "status.x.com",
]);

function dedupeById(tweets: Tweet[]): Tweet[] {
  const seen = new Set<string>();
  const out: Tweet[] = [];
  for (const tweet of tweets) {
    if (seen.has(tweet.id)) continue;
    seen.add(tweet.id);
    out.push(tweet);
  }
  return out;
}

function safeDateMs(createdAt: string): number {
  const ts = Date.parse(createdAt);
  return Number.isFinite(ts) ? ts : 0;
}

function toHost(tweet: Tweet): string | null {
  if (tweet.urls.length === 0) return null;
  try {
    return new URL(tweet.urls[0]).hostname.toLowerCase();
  } catch {
    return null;
  }
}

function recencyFactor(createdAt: string, nowMs: number): number {
  const createdMs = safeDateMs(createdAt);
  if (!createdMs) return 0.1;

  const ageHours = Math.max((nowMs - createdMs) / ONE_HOUR_MS, 1);
  return 80 / (1 + ageHours / 12);
}

function engagementSignal(tweet: Tweet): number {
  const impressionsBoost = Math.log1p(tweet.metrics.impressions);
  return (
    tweet.metrics.likes * 2 +
    tweet.metrics.retweets * 3.5 +
    tweet.metrics.replies * 1.25 +
    tweet.metrics.quotes * 1.8 +
    tweet.metrics.bookmarks * 1.4 +
    impressionsBoost * 1.75
  );
}

function diversityPenalty(count: number): number {
  if (count <= 1) return 1;
  return 1 / (1 + Math.sqrt(count - 1) * 0.38);
}

function qualitySignals(
  tweet: Tweet,
  hostCounts: Map<string, number>,
  voiceCounts: Map<string, number>
): { score: number; reasons: string[] } {
  const reasons: string[] = [];
  let score = engagementSignal(tweet);

  const host = toHost(tweet);
  const voice = tweet.username.toLowerCase();
  const lower = tweet.text.toLowerCase();

  const linkBonus = tweet.urls.length > 0 ? 1.22 : 0.93;
  if (tweet.urls.length > 0) reasons.push("has links");
  if (tweet.urls.length > 1) reasons.push("multiple links");

  if (host && TRUSTED_DOMAINS.has(host)) {
    reasons.push("trusted source domain");
    score *= 1.08;
  }

  const domainCount = host ? (hostCounts.get(host) || 0) : 0;
  const voiceCount = voiceCounts.get(voice) || 0;
  const domainPenalty = diversityPenalty(domainCount);
  const voicePenalty = diversityPenalty(voiceCount);
  if (domainPenalty < 1) reasons.push("domain saturation");
  if (voicePenalty < 1) reasons.push("voice saturation");

  const hasConcreteClaim = CLAIM_KEYWORDS.test(lower);
  const hasVerifiableLanguage = VERIFIED_PHRASE_KEYWORDS.test(lower);
  if (hasConcreteClaim) reasons.push("actionable claim");
  if (hasVerifiableLanguage) reasons.push("verifiable phrasing");

  const hasRiskSignal =
    /\b(scandal|breach|hack|fraud|vuln|vulnerability|regression|downgrade)\b/i.test(lower);
  if (hasRiskSignal) reasons.push("risk signal");

  const riskScore = hasRiskSignal ? 1.08 : 1;
  const claimScore = hasConcreteClaim ? 1.16 : 1;
  const verifiableScore = hasVerifiableLanguage ? 1.08 : 1;
  const actionability = hasConcreteClaim || hasVerifiableLanguage || tweet.urls.length > 0 ? 24 : 10;

  score += actionability;
  score *= claimScore * verifiableScore * riskScore * linkBonus;
  score = score * 0.75 + engagementSignal(tweet) * 0.4;
  score *= voicePenalty * domainPenalty;

  return { score, reasons };
}

function actionabilityScore(tweet: Tweet): number {
  const hasHashtags = Math.min(tweet.hashtags.length, 6) * 1.5;
  const hasMentions = Math.min(tweet.mentions.length, 4) * 1.1;
  const hasUrls = tweet.urls.length > 0 ? 14 : 0;
  const hasClaimTerms = CLAIM_KEYWORDS.test(tweet.text.toLowerCase()) ? 12 : 0;
  const hasVerified = VERIFIED_PHRASE_KEYWORDS.test(tweet.text.toLowerCase()) ? 12 : 0;
  return Math.max(0, hasHashtags + hasMentions + hasUrls + hasClaimTerms + hasVerified);
}

function addReasonsByWeight(score: number, reasons: string[]): string[] {
  const out = [...new Set(reasons)];
  if (score > 180) out.push("outstanding signal");
  if (score > 90 && !out.includes("high-confidence signal")) out.push("high-confidence signal");
  if (out.length === 0) out.push("contextual signal");
  return out.slice(0, MAX_REASON_COUNT);
}

export function rankBySignal(
  tweets: Tweet[],
  opts: { nowMs?: number; minScore?: number } = {}
): ScoredTweet[] {
  const nowMs = opts.nowMs ?? Date.now();
  const minScore = opts.minScore ?? SIGNAL_DEFAULT_MIN_SCORE;

  const unique = dedupeById(tweets);
  const hostCounts = new Map<string, number>();
  const voiceCounts = new Map<string, number>();

  for (const tweet of unique) {
    const host = toHost(tweet);
    if (host) hostCounts.set(host, (hostCounts.get(host) || 0) + 1);
    voiceCounts.set(tweet.username.toLowerCase(), (voiceCounts.get(tweet.username.toLowerCase()) || 0) + 1);
  }

  return unique
    .map((tweet) => {
      const engagement = engagementSignal(tweet);
      const recency = recencyFactor(tweet.created_at, nowMs);
      const actionability = actionabilityScore(tweet);
      const quality = qualitySignals(tweet, hostCounts, voiceCounts);
      const baseScore = quality.score + recency + actionability;
      const reasons = addReasonsByWeight(baseScore, [...quality.reasons]);

      return {
        ...tweet,
        signalScore: baseScore,
        signalReasons: reasons,
        signalBreakdown: {
          engagement,
          recency,
          actionability,
          quality: quality.score,
        },
      } satisfies ScoredTweet;
    })
    .filter((tweet) => tweet.signalScore >= minScore)
    .sort((a, b) =>
      b.signalScore - a.signalScore ||
      b.signalBreakdown.recency - a.signalBreakdown.recency ||
      b.signalBreakdown.engagement - a.signalBreakdown.engagement ||
      b.metrics.likes - a.metrics.likes
    );
}
