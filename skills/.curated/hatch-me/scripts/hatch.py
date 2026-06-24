#!/usr/bin/env python3
"""hatch.py — hatch yourself as a Codex baby from your date of birth.

Forked from `hatch-mom` (Apache 2.0): same Soul/Bones contract, but seeded
from a UTC-canonicalised date of birth instead of a session UUID. The moon
phase at the moment of birth is computed via `moon_phase.py` (Meeus AA2)
and embedded in the persisted Soul.

Layout intentionally mirrors ~/.codex/skills/hatch-pet/ and hatch-mom.

Usage:
    python3 hatch.py --dob 1995-08-14T03:20 --tz -07:00
    python3 hatch.py --dob 1995-08-14            # noon UTC
    python3 hatch.py --name Ada                  # reload existing baby
    python3 hatch.py --list
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from moon_phase import moon_phase as compute_moon_phase  # noqa: E402
from moon_phase import render_moon_ascii  # noqa: E402

SALT = "hatch-me-2026"

SPECIES = [
    ("duckling",   "🐤", "fluffy, follows you everywhere, peeps when confused"),
    ("chick",      "🐥", "just out of the shell, slightly damp, very brave"),
    ("sprout",     "🌱", "two leaves and a will to live"),
    ("hatchling",  "🥚", "still half-shelled; refuses to fully emerge"),
    ("mini-codex", "🤖", "tiny terminal native, speaks in monospace"),
    ("moonling",   "🌙", "born under a specific sky, knows it"),
    ("starlet",    "✨", "small and unreasonably hopeful"),
    ("tide",       "🌊", "moves with the moon, blames the moon"),
]

NAMES = [
    "Ada", "Babbage", "Cell", "Doppel", "Echo", "Fern", "Glia", "Hatch",
    "Iris", "Juno", "Kit", "Lumen", "Mote", "Nibble", "Orin", "Pip",
    "Quill", "Rune", "Sprout", "Tare", "Umbra", "Vex", "Wren", "Xilo",
    "Yarn", "Zephy", "Selene", "Hesper", "Aster", "Noctis",
]

STAT_KEYS = ["DEBUGGING", "PATIENCE", "CHAOS", "WISDOM", "SNARK"]

ZODIAC = [
    ((1, 20),  "Capricorn",   "♑"),
    ((2, 19),  "Aquarius",    "♒"),
    ((3, 21),  "Pisces",      "♓"),
    ((4, 20),  "Aries",       "♈"),
    ((5, 21),  "Taurus",      "♉"),
    ((6, 21),  "Gemini",      "♊"),
    ((7, 23),  "Cancer",      "♋"),
    ((8, 23),  "Leo",         "♌"),
    ((9, 23),  "Virgo",       "♍"),
    ((10, 23), "Libra",       "♎"),
    ((11, 22), "Scorpio",     "♏"),
    ((12, 22), "Sagittarius", "♐"),
    ((12, 31), "Capricorn",   "♑"),
]


def western_zodiac(dt: datetime) -> tuple[str, str]:
    m, d = dt.month, dt.day
    for (cm, cd), name, glyph in ZODIAC:
        if (m, d) < (cm, cd):
            return name, glyph
    return ZODIAC[-1][1], ZODIAC[-1][2]


def seeded_rng(seed_bytes: bytes):
    state = int.from_bytes(seed_bytes[:8], "big") or 1

    def next_u64() -> int:
        nonlocal state
        state = (state + 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
        z = state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
        return z ^ (z >> 31)

    return next_u64


def parse_dob(s: str, tz_offset: str | None) -> datetime:
    s = s.strip().replace(" ", "T")
    if "T" not in s:
        s = s + "T12:00:00"
    try:
        dt = datetime.fromisoformat(s)
    except ValueError as exc:
        raise SystemExit(f"unparseable --dob: {s!r} ({exc})")
    if dt.tzinfo is None:
        if tz_offset:
            sign = 1 if tz_offset[0] != "-" else -1
            hh, mm = tz_offset.lstrip("+-").split(":")
            off = timezone(timedelta(hours=sign * int(hh), minutes=sign * int(mm)))
            dt = dt.replace(tzinfo=off)
        else:
            dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def derive_soul(dob_utc: datetime) -> dict:
    dob_iso = dob_utc.isoformat().replace("+00:00", "Z")
    moon = compute_moon_phase(dob_utc)
    zodiac_name, zodiac_glyph = western_zodiac(dob_utc)

    digest = hashlib.blake2b(
        f"{SALT}|{dob_iso}|{moon['phase_name']}|{moon['illumination_pct']}".encode(),
        digest_size=32,
    ).digest()
    rng = seeded_rng(digest)

    name = NAMES[rng() % len(NAMES)]
    species_name, glyph, vibe = SPECIES[rng() % len(SPECIES)]
    shiny = (rng() % 100) == 0
    bones = {k: 1 + (rng() % 20) for k in STAT_KEYS}
    personality_seed = f"{rng():016x}"

    return {
        "schema_version": 1,
        "name": name + ("✨" if shiny else ""),
        "species": species_name,
        "glyph": glyph,
        "vibe": vibe,
        "shiny": shiny,
        "bones": bones,
        "personality_seed": personality_seed,
        "dob_utc": dob_iso,
        "moon": {
            "phase_name": moon["phase_name"],
            "phase_glyph": moon["phase_glyph"],
            "illumination_pct": moon["illumination_pct"],
            "waxing": moon["waxing"],
            "phase_angle_deg": moon["phase_angle_deg"],
            "lunation_day": moon["lunation_day"],
            "prev_new_moon_utc": moon["prev_new_moon_utc"],
            "algorithm": moon["algorithm"],
        },
        "zodiac": {"name": zodiac_name, "glyph": zodiac_glyph},
        "hatched_at": datetime.now(timezone.utc).isoformat(),
    }


def nursery_root() -> Path:
    home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    return home / "memories" / "babies"


def baby_dir(name: str) -> Path:
    safe = "".join(c for c in name if c.isalnum()).lower() or "anon"
    return nursery_root() / safe


def render_card(soul: dict) -> str:
    bones = soul["bones"]
    bar = lambda v: "█" * v + "░" * (20 - v)  # noqa: E731
    stat_lines = "\n".join(f"  {k:<10} {bar(v)} {v:>2}/20" for k, v in bones.items())
    shimmer = "  ✨ SHINY ✨\n" if soul["shiny"] else ""
    m = soul["moon"]
    z = soul["zodiac"]
    moon_art = render_moon_ascii(m["illumination_pct"], m.get("waxing", True), rows=9)
    moon_art_indented = "\n".join("    " + ln for ln in moon_art.splitlines())
    return (
        "\n"
        "  ╔══════════════════════════════════════════════╗\n"
        f"  ║   It's a {soul['species']}!{' ' * (35 - len(soul['species']))}║\n"
        "  ╚══════════════════════════════════════════════╝\n"
        f"\n   {soul['glyph']}  {soul['name']}\n"
        f"   {soul['vibe']}\n"
        f"{shimmer}"
        f"\n  sky on your birthday:\n\n"
        f"{moon_art_indented}\n\n"
        f"    {m['phase_glyph']}  {m['phase_name']:<18} {m['illumination_pct']:>5.1f}% illuminated\n"
        f"    {z['glyph']}  {z['name']}\n"
        "\n  bones:\n"
        f"{stat_lines}\n"
        f"\n  dob_utc:          {soul['dob_utc']}\n"
        f"  hatched_at:       {soul['hatched_at']}\n"
        f"  personality_seed: {soul['personality_seed']}\n"
    )


def load_baby(name: str) -> dict | None:
    path = baby_dir(name) / "baby.json"
    return json.loads(path.read_text()) if path.exists() else None


def save_baby(soul: dict) -> Path:
    d = baby_dir(soul["name"])
    d.mkdir(parents=True, exist_ok=True)
    path = d / "baby.json"
    path.write_text(json.dumps(soul, indent=2))
    return path


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Hatch yourself as a Codex baby.")
    p.add_argument("--dob", help="Date of birth: YYYY-MM-DD[THH:MM[:SS]] (UTC unless --tz).")
    p.add_argument("--tz", help="Offset like -07:00, applied when --dob has no tz info.")
    p.add_argument("--name", help="Load an existing baby by name instead of hatching.")
    p.add_argument("--list", action="store_true", help="List all hatched selves.")
    p.add_argument("--json", action="store_true", help="Emit soul JSON only (no birth card).")
    args = p.parse_args(argv)

    nursery = nursery_root()

    if args.list:
        if not nursery.exists():
            print("(no babies hatched yet)")
            return 0
        for baby in sorted(nursery.iterdir()):
            j = baby / "baby.json"
            if j.exists():
                s = json.loads(j.read_text())
                moon = s.get("moon", {}).get("phase_name", "?")
                print(f"  {s['glyph']}  {s['name']:<14} {s['species']:<12} "
                      f"dob={s.get('dob_utc','?')}  moon={moon}")
        return 0

    if args.name:
        soul = load_baby(args.name)
        if soul is None:
            print(f"no baby named {args.name!r} in {nursery}", file=sys.stderr)
            return 1
    else:
        if not args.dob:
            print("error: --dob required when not loading by --name", file=sys.stderr)
            return 2
        dob_utc = parse_dob(args.dob, args.tz)
        soul = derive_soul(dob_utc)
        save_baby(soul)

    if args.json:
        print(json.dumps(soul, indent=2))
    else:
        print(render_card(soul))
        if not args.name:
            print(f"  saved to: {baby_dir(soul['name']) / 'baby.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
