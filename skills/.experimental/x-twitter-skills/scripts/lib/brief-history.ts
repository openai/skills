import { existsSync, readFileSync, writeFileSync } from "fs";
import type { BriefReport } from "./brief";

export interface BriefSnapshot {
  question: string;
  generatedAt: string;
  uniqueTweetCount: number;
  rawTweetReads: number;
  topVoices: string[];
  themes: Record<string, number>;
}

export interface BriefDelta {
  prevGeneratedAt: string;
  currGeneratedAt: string;
  uniqueTweetDelta: number;
  tweetReadDelta: number;
  newVoices: string[];
  droppedVoices: string[];
  themeChanges: Array<{
    theme: string;
    previous: number;
    current: number;
    delta: number;
  }>;
}

export function estimateWorstCaseCost(
  queryCount: number,
  pages: number,
  opts: { tweetsPerPage?: number; readCostUsd?: number } = {}
): number {
  const tweetsPerPage = opts.tweetsPerPage ?? 100;
  const readCostUsd = opts.readCostUsd ?? 0.005;
  return queryCount * pages * tweetsPerPage * readCostUsd;
}

export function createSnapshot(report: BriefReport): BriefSnapshot {
  const themes: Record<string, number> = {};
  for (const theme of report.themes) {
    themes[theme.theme] = theme.count;
  }

  return {
    question: report.question,
    generatedAt: report.generatedAt,
    uniqueTweetCount: report.uniqueTweetCount,
    rawTweetReads: report.rawTweetReads,
    topVoices: report.topVoices.map((v) => v.username.toLowerCase()),
    themes,
  };
}

export function readSnapshot(path: string): BriefSnapshot | null {
  if (!existsSync(path)) return null;
  try {
    return JSON.parse(readFileSync(path, "utf-8")) as BriefSnapshot;
  } catch {
    return null;
  }
}

export function writeSnapshot(path: string, snapshot: BriefSnapshot): void {
  writeFileSync(path, JSON.stringify(snapshot, null, 2));
}

export function compareSnapshots(previous: BriefSnapshot, current: BriefSnapshot): BriefDelta {
  const prevVoices = new Set(previous.topVoices.map((v) => v.toLowerCase()));
  const currVoices = new Set(current.topVoices.map((v) => v.toLowerCase()));

  const newVoices = [...currVoices].filter((v) => !prevVoices.has(v)).sort();
  const droppedVoices = [...prevVoices].filter((v) => !currVoices.has(v)).sort();

  const themeNames = new Set<string>([
    ...Object.keys(previous.themes),
    ...Object.keys(current.themes),
  ]);

  const themeChanges = [...themeNames]
    .map((theme) => {
      const prev = previous.themes[theme] || 0;
      const curr = current.themes[theme] || 0;
      return {
        theme,
        previous: prev,
        current: curr,
        delta: curr - prev,
      };
    })
    .filter((row) => row.delta !== 0)
    .sort((a, b) => Math.abs(b.delta) - Math.abs(a.delta));

  return {
    prevGeneratedAt: previous.generatedAt,
    currGeneratedAt: current.generatedAt,
    uniqueTweetDelta: current.uniqueTweetCount - previous.uniqueTweetCount,
    tweetReadDelta: current.rawTweetReads - previous.rawTweetReads,
    newVoices,
    droppedVoices,
    themeChanges,
  };
}

export function formatDeltaMarkdown(delta: BriefDelta): string {
  let out = "## Delta vs Previous Brief\n\n";
  out += `- Previous run: ${delta.prevGeneratedAt}\n`;
  out += `- Current run: ${delta.currGeneratedAt}\n`;
  out += `- Unique tweet delta: ${delta.uniqueTweetDelta >= 0 ? "+" : ""}${delta.uniqueTweetDelta}\n`;
  out += `- Raw read delta: ${delta.tweetReadDelta >= 0 ? "+" : ""}${delta.tweetReadDelta}\n\n`;

  out += "### Voice Changes\n\n";
  out += `- New voices: ${delta.newVoices.length ? delta.newVoices.map((v) => `@${v}`).join(", ") : "none"}\n`;
  out += `- Dropped voices: ${delta.droppedVoices.length ? delta.droppedVoices.map((v) => `@${v}`).join(", ") : "none"}\n\n`;

  out += "### Theme Changes\n\n";
  if (delta.themeChanges.length === 0) {
    out += "- No meaningful theme shifts\n";
  } else {
    for (const row of delta.themeChanges) {
      const sign = row.delta >= 0 ? "+" : "";
      out += `- ${row.theme}: ${row.previous} -> ${row.current} (${sign}${row.delta})\n`;
    }
  }

  return out;
}
