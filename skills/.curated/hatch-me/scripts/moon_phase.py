#!/usr/bin/env python3
"""moon_phase.py — accurate lunar phase from a UTC date(time), with cross-verification.

Local Meeus math, optionally cross-checked against NASA JPL Horizons:

  ┌──────────────────────────────────────────────────────────────────────────┐
  │ source                          verifier                                 │
  │   meeus  Local Meeus AA2  ─────▶ jpl  NASA JPL Horizons HTTP API         │
  │   offline, deterministic, <1 ms  no key, ~500 ms, ground truth           │
  └──────────────────────────────────────────────────────────────────────────┘

Meeus implements:
  Ch. 7   — Gregorian calendar → Julian Date
  Ch. 47  — Mean elements of the Moon (D, M, M')
  Ch. 48  — Illuminated fraction and phase angle of the Moon (eq. 48.4)
  Ch. 49  — Phases of the Moon: JDE of nearest new moon (Table 49.A
            + 14 additional planetary corrections, p. 351-352)

JPL Horizons returns quantities 10 (Illu%) and 24 (S-T-O = phase angle)
for body 301 (Moon) from Earth geocenter 500@399. Endpoint:
https://ssd.jpl.nasa.gov/api/horizons.api (no key, public).

Inputs are interpreted as UTC. Pass --tz ±HH:MM for civil time.

Usage:
    python3 moon_phase.py --date 1995-08-14T10:20:00
    python3 moon_phase.py --date 1995-08-14T10:20:00 --source jpl
    python3 moon_phase.py --date 1995-08-14T10:20:00 --verify
    python3 moon_phase.py --self-test
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

# --------------------------------------------------------------------------- #
# Ch. 7 — Julian Date                                                         #
# --------------------------------------------------------------------------- #


def jd_from_datetime(dt: datetime) -> float:
    """Return Julian Date (UT) for a Gregorian datetime in UTC."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    dt = dt.astimezone(timezone.utc)
    y, m = dt.year, dt.month
    d = dt.day + (dt.hour + dt.minute / 60 + dt.second / 3600) / 24
    if m <= 2:
        y -= 1
        m += 12
    a = y // 100
    b = 2 - a + a // 4  # Gregorian only; modern dates assumed.
    return math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + d + b - 1524.5


def jd_to_datetime(jd: float) -> datetime:
    """Inverse of jd_from_datetime, UTC."""
    jd += 0.5
    z = int(math.floor(jd))
    f = jd - z
    if z < 2299161:
        a = z
    else:
        alpha = int((z - 1867216.25) / 36524.25)
        a = z + 1 + alpha - alpha // 4
    b = a + 1524
    c = int((b - 122.1) / 365.25)
    d = int(365.25 * c)
    e = int((b - d) / 30.6001)
    day_frac = b - d - int(30.6001 * e) + f
    day = int(day_frac)
    month = e - 1 if e < 14 else e - 13
    year = c - 4716 if month > 2 else c - 4715
    secs = (day_frac - day) * 86400
    return datetime(year, month, day, tzinfo=timezone.utc) + timedelta(seconds=secs)


# --------------------------------------------------------------------------- #
# Ch. 49 — JDE of new moon for integer k                                      #
# --------------------------------------------------------------------------- #


def _newmoon_jde(k: int) -> float:
    """JDE of the new moon whose ordinal (since 2000 Jan 6) is k. Meeus 49.1."""
    T = k / 1236.85
    jde = (
        2451550.09766
        + 29.530588861 * k
        + 0.00015437 * T**2
        - 0.000000150 * T**3
        + 0.00000000073 * T**4
    )
    E = 1 - 0.002516 * T - 0.0000074 * T**2

    M = math.radians(
        2.5534 + 29.10535670 * k - 0.0000014 * T**2 - 0.00000011 * T**3
    )
    Mp = math.radians(
        201.5643
        + 385.81693528 * k
        + 0.0107582 * T**2
        + 0.00001238 * T**3
        - 0.000000058 * T**4
    )
    F = math.radians(
        160.7108
        + 390.67050284 * k
        - 0.0016118 * T**2
        - 0.00000227 * T**3
        + 0.00000000011 * T**4
    )
    Om = math.radians(
        124.7746 - 1.56375588 * k + 0.0020672 * T**2 + 0.00000215 * T**3
    )

    # Table 49.A — periodic corrections for NEW MOON.
    c = (
        -0.40720 * math.sin(Mp)
        + 0.17241 * E * math.sin(M)
        + 0.01608 * math.sin(2 * Mp)
        + 0.01039 * math.sin(2 * F)
        + 0.00739 * E * math.sin(Mp - M)
        - 0.00514 * E * math.sin(Mp + M)
        + 0.00208 * E * E * math.sin(2 * M)
        - 0.00111 * math.sin(Mp - 2 * F)
        - 0.00057 * math.sin(Mp + 2 * F)
        + 0.00056 * E * math.sin(2 * Mp + M)
        - 0.00042 * math.sin(3 * Mp)
        + 0.00042 * E * math.sin(M + 2 * F)
        + 0.00038 * E * math.sin(M - 2 * F)
        - 0.00024 * E * math.sin(2 * Mp - M)
        - 0.00017 * math.sin(Om)
        - 0.00007 * math.sin(Mp + 2 * M)
        + 0.00004 * math.sin(2 * Mp - 2 * F)
        + 0.00004 * math.sin(3 * M)
        + 0.00003 * math.sin(Mp + M - 2 * F)
        + 0.00003 * math.sin(2 * Mp + 2 * F)
        - 0.00003 * math.sin(Mp + M + 2 * F)
        + 0.00003 * math.sin(Mp - M + 2 * F)
        - 0.00002 * math.sin(Mp - M - 2 * F)
        - 0.00002 * math.sin(3 * Mp + M)
        + 0.00002 * math.sin(4 * Mp)
    )
    jde += c

    # Additional 14 planetary corrections (Meeus pp. 351–352).
    A = [
        (299.77, 0.107408, -0.009173, 0.000325),
        (251.88, 0.016321, 0.0, 0.000165),
        (251.83, 26.651886, 0.0, 0.000164),
        (349.42, 36.412478, 0.0, 0.000126),
        (84.66, 18.206239, 0.0, 0.000110),
        (141.74, 53.303771, 0.0, 0.000062),
        (207.14, 2.453732, 0.0, 0.000060),
        (154.84, 7.306860, 0.0, 0.000056),
        (34.52, 27.261239, 0.0, 0.000047),
        (207.19, 0.121824, 0.0, 0.000042),
        (291.34, 1.844379, 0.0, 0.000040),
        (161.72, 24.198154, 0.0, 0.000037),
        (239.56, 25.513099, 0.0, 0.000035),
        (331.55, 3.592518, 0.0, 0.000023),
    ]
    for base, k_coeff, t2_coeff, amp in A:
        ang = math.radians(base + k_coeff * k + t2_coeff * T**2)
        jde += amp * math.sin(ang)

    return jde


# --------------------------------------------------------------------------- #
# Ch. 47/48 — Phase angle and illuminated fraction                            #
# --------------------------------------------------------------------------- #


def _phase_geometry(jd: float) -> tuple[float, float]:
    """Return (phase_angle_deg in [0,180], mean_elongation_deg in [0,360)).

    Phase angle i (Sun-Moon-Earth at the Moon) from Meeus 48.4. Mean elongation
    D from Meeus 47.2 — used to distinguish waxing (0<=D<180) from waning.
    """
    T = (jd - 2451545.0) / 36525.0
    D = (
        297.8501921
        + 445267.1114034 * T
        - 0.0018819 * T**2
        + T**3 / 545868
        - T**4 / 113065000
    )
    M = (
        357.5291092
        + 35999.0502909 * T
        - 0.0001536 * T**2
        + T**3 / 24490000
    )
    Mp = (
        134.9633964
        + 477198.8675055 * T
        + 0.0087414 * T**2
        + T**3 / 69699
        - T**4 / 14712000
    )
    D_r, M_r, Mp_r = math.radians(D), math.radians(M), math.radians(Mp)
    i_raw = (
        180.0
        - D
        - 6.289 * math.sin(Mp_r)
        + 2.100 * math.sin(M_r)
        - 1.274 * math.sin(2 * D_r - Mp_r)
        - 0.658 * math.sin(2 * D_r)
        - 0.214 * math.sin(2 * Mp_r)
        - 0.110 * math.sin(D_r)
    )
    i = i_raw % 360
    if i > 180:
        i = 360 - i
    return i, D % 360


# --------------------------------------------------------------------------- #
# Public API                                                                  #
# --------------------------------------------------------------------------- #

# Phase naming: narrow-quarter convention (matches USNO / TimeAndDate / most almanacs).
# A cardinal phase (new, first quarter, full, last quarter) is named only within
# ±1 day of its true event; everything else is crescent or gibbous, signed by
# whether the moon is waxing (mean elongation D in [0, 180)) or waning.
NEW_FULL_ILLUM_THRESHOLD = 1.0    # within ±1% illumination of new/full
QUARTER_ILLUM_THRESHOLD = 3.0     # within ±3% of 50% illumination (≈ ±1 day)


def _name_phase(illum_pct: float, waxing: bool) -> tuple[str, str]:
    if illum_pct < NEW_FULL_ILLUM_THRESHOLD:
        return "New Moon", "🌑"
    if illum_pct > 100 - NEW_FULL_ILLUM_THRESHOLD:
        return "Full Moon", "🌕"
    if abs(illum_pct - 50) < QUARTER_ILLUM_THRESHOLD:
        return ("First Quarter", "🌓") if waxing else ("Last Quarter", "🌗")
    if waxing:
        return ("Waxing Crescent", "🌒") if illum_pct < 50 else ("Waxing Gibbous", "🌔")
    return ("Waning Gibbous", "🌖") if illum_pct > 50 else ("Waning Crescent", "🌘")


def _bracket_new_moons(jd: float) -> tuple[float, float, int]:
    """Return (prev_new_jde, next_new_jde, k_prev) bracketing jd."""
    year_approx = 2000 + (jd - 2451545.0) / 365.25
    k = math.floor((year_approx - 2000) * 12.3685)
    # Walk down until prev <= jd.
    jde = _newmoon_jde(k)
    while jde > jd:
        k -= 1
        jde = _newmoon_jde(k)
    # Walk up while next still <= jd.
    while True:
        jde_next = _newmoon_jde(k + 1)
        if jde_next > jd:
            return jde, jde_next, k
        k += 1
        jde = jde_next


def moon_phase(dt_utc: datetime) -> dict:
    """Full moon-phase report for a UTC datetime."""
    jd = jd_from_datetime(dt_utc)
    prev_new, next_new, k_prev = _bracket_new_moons(jd)
    cycle = next_new - prev_new
    frac = (jd - prev_new) / cycle
    lunation_day = jd - prev_new

    i, D = _phase_geometry(jd)
    illum_pct = (1 + math.cos(math.radians(i))) / 2 * 100
    waxing = D < 180.0
    name, glyph = _name_phase(illum_pct, waxing)

    return {
        "input_utc": dt_utc.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "julian_date": round(jd, 6),
        "phase_name": name,
        "phase_glyph": glyph,
        "waxing": waxing,
        "illumination_pct": round(illum_pct, 2),
        "phase_angle_deg": round(i, 3),
        "mean_elongation_deg": round(D, 3),
        "lunation_day": round(lunation_day, 3),
        "lunation_fraction": round(frac, 5),
        "synodic_period_days": round(cycle, 5),
        "prev_new_moon_utc": jd_to_datetime(prev_new).isoformat().replace("+00:00", "Z"),
        "next_new_moon_utc": jd_to_datetime(next_new).isoformat().replace("+00:00", "Z"),
        "source": "meeus",
        "algorithm": "Meeus AA2 Ch. 47/48/49 + Table 49.A + 14 planetary corrections",
    }


# --------------------------------------------------------------------------- #
# JPL Horizons — ground-truth verifier                                        #
# --------------------------------------------------------------------------- #

JPL_HORIZONS_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"


def moon_phase_jpl(dt_utc: datetime, timeout: float = 15.0) -> dict:
    """Query JPL Horizons for illuminated fraction + phase angle at dt_utc.

    Uses quantities 10 (Illu%) and 24 (S-T-O = phase angle in degrees) for
    body 301 (Moon) from Earth geocenter 500@399. Waxing/waning is not
    returned by Horizons in this query, so we derive it from local Meeus
    mean elongation D — this is a sub-degree-precise property that all
    sources agree on, so reusing Meeus for D alone is safe.
    """
    t1 = dt_utc.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M")
    t2 = (dt_utc.astimezone(timezone.utc) + timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M")
    params = {
        "format": "text",
        "COMMAND": "'301'",
        "OBJ_DATA": "'NO'",
        "MAKE_EPHEM": "'YES'",
        "EPHEM_TYPE": "'OBSERVER'",
        "CENTER": "'500@399'",
        "START_TIME": f"'{t1}'",
        "STOP_TIME": f"'{t2}'",
        "STEP_SIZE": "'1m'",
        "QUANTITIES": "'10,24'",
    }
    url = JPL_HORIZONS_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "hatch-me/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read().decode("utf-8", errors="replace")
    except Exception as exc:
        raise RuntimeError(f"JPL Horizons request failed: {exc}") from exc

    try:
        soe = body.index("$$SOE")
        eoe = body.index("$$EOE", soe)
    except ValueError:
        raise RuntimeError("JPL Horizons response missing $$SOE/$$EOE block")
    data_line = next((ln for ln in body[soe:eoe].splitlines()[1:] if ln.strip()), None)
    if not data_line:
        raise RuntimeError("JPL Horizons returned an empty data block")
    parts = data_line.split()
    try:
        illum, sto = float(parts[-2]), float(parts[-1])
    except (IndexError, ValueError) as exc:
        raise RuntimeError(f"unparseable JPL data row {data_line!r}: {exc}") from exc

    _, D = _phase_geometry(jd_from_datetime(dt_utc))
    waxing = D < 180.0
    name, glyph = _name_phase(illum, waxing)
    return {
        "source": "jpl-horizons",
        "input_utc": dt_utc.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "phase_name": name,
        "phase_glyph": glyph,
        "waxing": waxing,
        "illumination_pct": round(illum, 4),
        "phase_angle_deg": round(sto, 4),
        "endpoint": JPL_HORIZONS_URL,
        "quantities": "10 (Illu%), 24 (S-T-O phase angle)",
        "body": "301 (Moon)",
        "center": "500@399 (Earth geocenter)",
    }


# --------------------------------------------------------------------------- #
# Cross-verification                                                          #
# --------------------------------------------------------------------------- #

SOURCE_FNS = {
    "meeus": moon_phase,
    "jpl":   moon_phase_jpl,
}

# Tolerances against JPL ground truth.
TOLERANCE_ILLUM_PCT = 1.0    # Meeus typically <0.5%, LLMs frequently fail this.
TOLERANCE_ANGLE_DEG = 0.5


def verify(dt_utc: datetime) -> dict:
    """Run local Meeus and compute deltas against JPL Horizons (ground truth).

    Returns a structured report; pretty-printing is the CLI's job.
    """
    results: dict[str, dict] = {}
    errors: dict[str, str] = {}

    try:
        results["jpl"] = moon_phase_jpl(dt_utc)
    except Exception as exc:
        errors["jpl"] = str(exc)

    try:
        results["meeus"] = moon_phase(dt_utc)
    except Exception as exc:
        errors["meeus"] = str(exc)

    truth = results.get("jpl")
    diffs: dict[str, dict] = {}
    if truth is not None:
        for src, r in results.items():
            if src == "jpl":
                continue
            illum = r.get("illumination_pct")
            angle = r.get("phase_angle_deg")
            d_illum = None if illum is None else round(illum - truth["illumination_pct"], 4)
            d_angle = None if angle is None else round(angle - truth["phase_angle_deg"], 4)
            within = (
                d_illum is not None
                and abs(d_illum) <= TOLERANCE_ILLUM_PCT
                and (d_angle is None or abs(d_angle) <= TOLERANCE_ANGLE_DEG)
            )
            diffs[src] = {
                "illum_delta_pct": d_illum,
                "phase_angle_delta_deg": d_angle,
                "phase_name_matches": r.get("phase_name") == truth["phase_name"],
                "within_tolerance": within,
            }

    return {
        "input_utc": dt_utc.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "ground_truth": "jpl-horizons" if truth else None,
        "tolerances": {
            "illum_pct": TOLERANCE_ILLUM_PCT,
            "phase_angle_deg": TOLERANCE_ANGLE_DEG,
        },
        "results": results,
        "diffs_vs_jpl": diffs,
        "errors": errors,
    }


def render_verify_table(report: dict) -> str:
    """Compact human-readable verification table."""
    truth = report["results"].get("jpl")
    lines = [f"  moon phase at {report['input_utc']}",
             "  " + "─" * 78]
    header = f"  {'source':<14} {'phase':<18} {'illum%':>8} {'phase°':>8}   Δ vs JPL"
    lines.append(header)
    lines.append("  " + "─" * 78)
    if truth:
        lines.append(
            f"  {'jpl-horizons':<14} {truth['phase_name']:<18} "
            f"{truth['illumination_pct']:>8.4f} {truth['phase_angle_deg']:>8.4f}   "
            f"── (ground truth)"
        )
    for src, r in report["results"].items():
        if src == "jpl":
            continue
        d = report["diffs_vs_jpl"].get(src, {})
        illum = r.get("illumination_pct")
        angle = r.get("phase_angle_deg")
        illum_s = "—" if illum is None else f"{illum:>8.4f}"
        angle_s = "—" if angle is None else f"{angle:>8.4f}"
        delta_bits = []
        if d.get("illum_delta_pct") is not None:
            delta_bits.append(f"{d['illum_delta_pct']:+.4f}%")
        if d.get("phase_angle_delta_deg") is not None:
            delta_bits.append(f"{d['phase_angle_delta_deg']:+.4f}°")
        marker = " ✓" if d.get("within_tolerance") else (" ✗" if d else "")
        lines.append(
            f"  {src:<14} {(r.get('phase_name') or '—'):<18} "
            f"{illum_s} {angle_s}   {' / '.join(delta_bits) or '—'}{marker}"
        )
    if report["errors"]:
        lines.append("  " + "─" * 78)
        for src, msg in report["errors"].items():
            lines.append(f"  {src:<14} ERROR: {msg}")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# CLI                                                                         #
# --------------------------------------------------------------------------- #


def _parse_dt(s: str, tz_offset: str | None) -> datetime:
    """Parse YYYY-MM-DD or YYYY-MM-DD[T ]HH:MM[:SS][±HH:MM]. Default 12:00 UTC."""
    s = s.strip().replace(" ", "T")
    if "T" not in s:
        s = s + "T12:00:00"
    try:
        dt = datetime.fromisoformat(s)
    except ValueError as exc:
        raise SystemExit(f"unparseable date: {s!r} ({exc})")
    if dt.tzinfo is None:
        if tz_offset:
            sign = 1 if tz_offset[0] != "-" else -1
            hh, mm = tz_offset.lstrip("+-").split(":")
            off = timezone(timedelta(hours=sign * int(hh), minutes=sign * int(mm)))
            dt = dt.replace(tzinfo=off)
        else:
            dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _self_test() -> int:
    """Verify against four reference events (USNO/JPL)."""
    cases = [
        # (label, iso UTC, expected phase, expected illum %, tolerance)
        ("2000 Jan 6 18:14 UT new moon",  "2000-01-06T18:14:00Z", "New Moon",      0.0, 1.0),
        ("2024 Apr 8 18:18 UT new moon",  "2024-04-08T18:18:00Z", "New Moon",      0.0, 1.0),
        ("2024 Apr 23 23:49 UT full moon","2024-04-23T23:49:00Z", "Full Moon",   100.0, 1.0),
        ("1969 Jul 20 20:17 UT Apollo 11","1969-07-20T20:17:00Z", "Waxing Crescent", 33.0, 8.0),
    ]
    ok = True
    for label, iso, want_phase, want_illum, tol in cases:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        r = moon_phase(dt)
        phase_ok = r["phase_name"] == want_phase
        illum_ok = abs(r["illumination_pct"] - want_illum) <= tol
        flag = "OK " if phase_ok and illum_ok else "FAIL"
        if not (phase_ok and illum_ok):
            ok = False
        print(f"[{flag}] {label}")
        print(f"       got phase={r['phase_name']!r} illum={r['illumination_pct']}%  "
              f"want={want_phase!r} ~{want_illum}% (±{tol})")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Moon phase: local Meeus math, verified against NASA JPL Horizons.")
    ap.add_argument("--date", help="YYYY-MM-DD[THH:MM[:SS]]; UTC unless --tz given.")
    ap.add_argument("--tz", help="Offset like -07:00 applied when --date has no tz.")
    ap.add_argument(
        "--source",
        choices=list(SOURCE_FNS.keys()),
        default="meeus",
        help="Compute via this source only. Default: meeus (local, deterministic, offline).",
    )
    ap.add_argument(
        "--verify",
        action="store_true",
        help="Run meeus + JPL Horizons and print a comparison table. JPL is ground truth.",
    )
    ap.add_argument("--self-test", action="store_true", help="Run reference checks.")
    ap.add_argument("--pretty", action="store_true", help="Indent JSON output.")
    args = ap.parse_args()

    if args.self_test:
        return _self_test()
    if not args.date:
        ap.error("--date is required (or use --self-test)")

    dt = _parse_dt(args.date, args.tz)

    if args.verify:
        report = verify(dt)
        if args.pretty:
            print(json.dumps(report, indent=2))
        else:
            print(render_verify_table(report))
        # Exit 1 if any non-error source is outside tolerance.
        for d in report["diffs_vs_jpl"].values():
            if not d.get("within_tolerance"):
                return 1
        return 0 if report["results"].get("jpl") else 2

    result = SOURCE_FNS[args.source](dt)
    print(json.dumps(result, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    sys.exit(main())
