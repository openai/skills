import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";
import { join } from "path";
import type { Tweet } from "./api";

interface Watchlist {
  accounts: { username: string; note?: string; addedAt: string }[];
}

function ensureDir(path: string) {
  if (!existsSync(path)) mkdirSync(path, { recursive: true });
}

function loadWatchlist(path: string): Watchlist {
  if (!existsSync(path)) return { accounts: [] };
  return JSON.parse(readFileSync(path, "utf-8"));
}

function saveWatchlist(path: string, wl: Watchlist) {
  ensureDir(join(path, ".."));
  writeFileSync(path, JSON.stringify(wl, null, 2));
}

export async function runWatchlistCommand(
  args: string[],
  opts: {
    watchlistPath: string;
    profile: (username: string, options: { count?: number; includeReplies?: boolean }) => Promise<{ user: any; tweets: Tweet[] }>;
    formatTweet: (tweet: Tweet, index?: number, options?: { full?: boolean }) => string;
  }
): Promise<void> {
  const sub = args[1];
  const wl = loadWatchlist(opts.watchlistPath);

  if (sub === "add") {
    const username = args[2]?.replace(/^@/, "");
    const note = args.slice(3).join(" ") || undefined;
    if (!username) {
      console.error("Usage: x-search.ts watchlist add <username> [note]");
      process.exit(1);
    }
    if (wl.accounts.find((a) => a.username.toLowerCase() === username.toLowerCase())) {
      console.log(`@${username} already on watchlist.`);
      return;
    }

    wl.accounts.push({ username, note, addedAt: new Date().toISOString() });
    saveWatchlist(opts.watchlistPath, wl);
    console.log(`Added @${username} to watchlist.${note ? ` (${note})` : ""}`);
    return;
  }

  if (sub === "remove" || sub === "rm") {
    const username = args[2]?.replace(/^@/, "");
    if (!username) {
      console.error("Usage: x-search.ts watchlist remove <username>");
      process.exit(1);
    }

    const before = wl.accounts.length;
    wl.accounts = wl.accounts.filter((a) => a.username.toLowerCase() !== username.toLowerCase());
    saveWatchlist(opts.watchlistPath, wl);
    console.log(
      wl.accounts.length < before
        ? `Removed @${username} from watchlist.`
        : `@${username} not found on watchlist.`
    );
    return;
  }

  if (sub === "check") {
    if (wl.accounts.length === 0) {
      console.log("Watchlist is empty. Add accounts with: watchlist add <username>");
      return;
    }

    console.log(`Checking ${wl.accounts.length} watchlist accounts...\n`);
    for (const acct of wl.accounts) {
      try {
        const { tweets } = await opts.profile(acct.username, { count: 5 });
        const label = acct.note ? ` (${acct.note})` : "";
        console.log(`\n--- @${acct.username}${label} ---`);
        if (tweets.length === 0) {
          console.log("  No recent tweets.");
        } else {
          for (const tweet of tweets.slice(0, 3)) {
            console.log(opts.formatTweet(tweet));
            console.log();
          }
        }
      } catch (e: any) {
        console.error(`  Error checking @${acct.username}: ${e.message}`);
      }
    }
    return;
  }

  if (wl.accounts.length === 0) {
    console.log("Watchlist is empty. Add accounts with: watchlist add <username>");
    return;
  }

  console.log(`📋 Watchlist (${wl.accounts.length} accounts)\n`);
  for (const acct of wl.accounts) {
    const note = acct.note ? ` — ${acct.note}` : "";
    console.log(`  @${acct.username}${note} (added ${acct.addedAt.split("T")[0]})`);
  }
}
