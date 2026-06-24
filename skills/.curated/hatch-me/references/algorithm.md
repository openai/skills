# algorithm: moon-phase math + cross-verification

`scripts/moon_phase.py` ships one local implementation and one network
verifier. The default is the local Meeus math; JPL Horizons is the single
source of truth used when `--verify` is passed.

## Sources

```
                                   ┌─────────────────────────────────┐
                                   │ default source (used for hatch) │
                          ┌────────┤   meeus   pure-Python AA2       │
                          │        │   offline, deterministic, <1 ms │
                          │        └─────────────────────────────────┘
DOB / any UTC instant ────┤
                          │        ┌─────────────────────────────────┐
                          │        │ ground truth (verifier)         │
                          └───────▶│   jpl     NASA JPL Horizons     │
                                   │   https://ssd.jpl.nasa.gov/api  │
                                   │   /horizons.api                 │
                                   │   body 301, center 500@399,     │
                                   │   QUANTITIES=10,24 (Illu%, S-T-O)│
                                   │   ~500 ms, no key, public       │
                                   └────────────┬────────────────────┘
                                                ▼
                                       --verify compares meeus to jpl
                                       |Δ illum%| ≤ 1.0
                                       |Δ phase°| ≤ 0.5
                                       phase name must match
```

## Local pipeline (Meeus)

All formulas from Jean Meeus, *Astronomical Algorithms*, Willmann-Bell, 1998
(2nd ed.). Implemented in pure Python in `scripts/moon_phase.py`, no deps.

## Pipeline

```
                              ┌──────────────────────────────────────┐
                              │ Meeus Ch. 7 — calendar → Julian Date │
                              │   civil UTC datetime → JD            │
                              └────────────────┬─────────────────────┘
                                               ▼
        ┌──────────────────────────────────────┴──────────────────────────────────────┐
        ▼                                                                             ▼
┌──────────────────────────────────────────┐                  ┌──────────────────────────────────────────┐
│ Meeus Ch. 47 — mean elements             │                  │ Meeus Ch. 49 — JDE of new moon           │
│   D  mean elongation                     │                  │   k integer ordinal since 2000-01-06     │
│   M  Sun mean anomaly                    │                  │   JDE = 2451550.09766 + 29.530588861·k   │
│   M' Moon mean anomaly                   │                  │         + polynomial in T = k/1236.85    │
└──────────────────────────────────────────┘                  │   + Table 49.A periodic corrections      │
        ▼                                                     │   + 14 planetary corrections (pp.351-352)│
┌──────────────────────────────────────────┐                  └────────────────┬─────────────────────────┘
│ Meeus Ch. 48 eq. 48.4 — phase angle i    │                                   ▼
│ i = 180° − D − 6.289°sinM' + 2.100°sinM  │                  ┌──────────────────────────────────────────┐
│     − 1.274°sin(2D−M') − 0.658°sin(2D)   │                  │ bracket JD between new moons k, k+1      │
│     − 0.214°sin(2M')   − 0.110°sinD       │                  │   prev_new ≤ JD < next_new               │
│ illum = (1 + cos i) / 2                  │                  │   cycle = next_new − prev_new (~29.53 d) │
└────────────┬─────────────────────────────┘                  │   lunation_day = JD − prev_new           │
             ▼                                                └────────────────┬─────────────────────────┘
   illumination_pct, phase_angle_deg                                            ▼
                                                                   lunation_day, prev/next_new_moon_utc
             │                                                                 │
             └──────────────────────────────┬──────────────────────────────────┘
                                            ▼
                              ┌─────────────────────────────────┐
                              │ name from (illum, waxing)       │
                              │   waxing iff D mod 360 < 180    │
                              │   New / Full ≤ 1% of cardinal   │
                              │   Quarter ≤ 3% of 50%           │
                              │   else Crescent / Gibbous       │
                              └─────────────────────────────────┘
```

## Precision

Per Meeus, the published constants give:

- new-moon JDE: ±2 minutes for dates in 1900–2100
- phase angle i: <0.5° (so illumination error <1% near the quarters,
  even smaller near new/full)
- mean elongation D: drifts by <0.001° / century from the J2000 fit

The implementation is verified two ways:

1. `moon_phase.py --self-test` against four hardcoded reference events
   (USNO/JPL ephemeris times):

   | Event | Reference time (UT) | Expected |
   |---|---|---|
   | New Moon (k = 0 baseline) | 2000-01-06 18:14 | New Moon, 0% |
   | Total Solar Eclipse | 2024-04-08 18:18 | New Moon, 0% |
   | Pink Full Moon | 2024-04-23 23:49 | Full Moon, 100% |
   | Apollo 11 LM touchdown | 1969-07-20 20:17 | Waxing Crescent, ~33% |

2. `moon_phase.py --date <any> --verify` calls NASA JPL Horizons live
   for the same date and prints the delta. JPL is the authority Meeus's
   polynomial tables were fit to; round-trip agreement is the strongest
   correctness signal we can get for arbitrary dates.

   Spot check at 1995-08-14 10:20 UTC: meeus 83.89% / 47.33°, JPL 83.85%
   / 47.40°, Δ +0.04% / −0.07° — well within the ±1.0% / ±0.5° tolerance.

## Why narrow-quarter naming

Two conventions exist:

- **Equal-eighth buckets** — each of the 8 named phases owns 1/8 of the
  synodic cycle. Simple, but a moon at 6 days post-new (33% illuminated)
  gets labeled "First Quarter" even though the actual quarter event is
  another day away.
- **Narrow-quarter (USNO / TimeAndDate / most almanacs)** — the four
  cardinal names apply only within ±1 day of the actual event;
  crescent/gibbous fill the rest. This matches what users see in moon
  phase apps and on the front of paper calendars.

`scripts/moon_phase.py` uses the narrow-quarter convention. The
illumination percentage is reported separately and is independent of
the naming choice.

## What this code does **not** include

- Topocentric parallax (geocentric only — irrelevant for phase naming)
- Lunar libration
- Lunar position in equatorial / ecliptic coordinates (Meeus Ch. 47 has
  it; we only need D, M, M' for phase, not the full position)
- First / last quarter and full-moon JDEs (we bracket new moons only;
  the quarter and full timings can be inferred from D crossing 90/180/270°
  but we don't expose them — phase naming uses illumination, not events)

Add any of these if downstream tools start asking for them.
