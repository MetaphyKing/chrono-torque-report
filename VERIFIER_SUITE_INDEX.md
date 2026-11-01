# CHRONO-TORQUE (`v2.0.1`) Verifier Suite Index & Peer-Review Line Map

> **Second-Seat Integrity Invariant:** [`GROK_PEER_REVIEW_VERDICT.md`](GROK_PEER_REVIEW_VERDICT.md) is preserved byte-for-byte as written by the independent reviewer in commit `3dc2770`. This companion index maps the line ranges of `GROK_PEER_REVIEW_VERDICT.md` and the full 3-script `20/20` verifier suite in `public-verifier/`.

## 1. Line-Range Map of `GROK_PEER_REVIEW_VERDICT.md` (`commit 3dc2770`)
- **Lines `1–62` (`## Round 2 reopen — current verdict: 6/6 SIGN-OFF`):** The **active, current verdict** certifying all 6 Round-1 close conditions on `public-verifier/verify_chrono_torque_public_cartridge.py`, including:
  - Condition 1 (`line 19`): Closed-form Eq. (1) yields $I_k = [3.96, 12.06, 28.88, 92.74, 115.66, 2189.20]$, $I_6/I_1 = 552.83\times$ (CBCE terminal-pinion model ratio), and $\Omega_{\text{CBCE}} = 248.9182$.
  - Condition 2 (`line 20`): $p_{\text{in,RM}} = 1.2261 \times 10^{-6} \to 35 p_{\text{in}}^3 = 6.452 \times 10^{-17}$.
  - Condition 3 (`line 21` & `lines 40–49`): Canonical `55.18 B/cell [60.8 µs model]` and PAPR `38.00 B/cell [41.2 µs model, 80.84× byte-layout ratio]`, plus explicit uncompiled Python/NumPy wall-clock timers (`measured_zdc_wall_latency_us = 1070.11 µs`, `measured_fp32_wall_latency_us = 181.64 µs`).
  - Condition 4 (`line 22`): Gunther USL $S(32) = 4.3447\times \to 47,228.5\text{ tok/s}$.
  - Condition 5 (`line 23`): `papr_guarded=True -> Z_ref=0.0`; `papr_guarded=False -> Z_ref=9,765,625.0`.
  - Condition 6 (`line 24`): `9` inversion swaps + `1` cull = `10` ops, and `7×7 = 49` ticks vs. $\le \binom{8}{2} = 28$ swaps.
  - Scope Note (`lines 59–62`): Certifies numerical and structural closures of the cartridge; `60.8 µs` / `41.2 µs` are the cache-line model latencies and `3,259.80 -> 264.97 ms` (`12.303×`) is the modelled 6-stage ecosystem latency budget.
- **Lines `65–144` (`## Prior Round 2 (retained, superseded)`):** Retained historical log from Round 2 (`4/6` met prior to the Pass-3 reopen).
- **Lines `147–220` (`## Round 1 verdict (retained)` — including `## Method`, `## Gate log`, `## Number audit`, `## What holds`, `## Verifier scope`, and `## Recommendation`):** Retained historical log from Round 1 (`429.91×` prior to Theorem 1.2/2.1 alignment).

## 2. Full `v2.0.1` Public Verifier Suite (`6 + 6 + 8 = 20/20` Gates)
1. **`public-verifier/verify_chrono_torque_public_cartridge.py` (`6/6` Gates):** Primary cartridge verifier reviewed in `GROK_PEER_REVIEW_VERDICT.md`.
2. **`public-verifier/independent_second_method_verifier.py` (`6/6` Gates):** Zero-shared-code cross-verifier using Python `fractions.Fraction` and 50-digit `decimal.Decimal` arithmetic.
3. **`public-verifier/verify_tpd_qms_chrono_unification.py` (`8/8` Gates):** 20,000-point 16-decade wavenumber sweep for Theorem 3.1 ($\min(v_g/c_0) = 0.963773 \ge 0.96$, $|\Delta\alpha/\alpha_0| < 10^{-17}$).

## 3. Sibling Repository Cross-Reference (`CHORD-SIEVES v2.4`)
- Exoplanet NASA TESS 2-minute SPOC lightcurve and Contact-Map Diophantine Non-Transit Sector Veto metrics (`845` v2.4 snapshot / `1,263` live candidate records across `386` / `525` TIC star systems, `2,170 / 4,957` on-time ephemeris windows, `0 WRONG` across `2,592` covered windows, `4/4` verifier gates) live in `C:\dev\chord-sieves-report\GROK_PEER_REVIEW_VERDICT.md` (Grok Round 2 `SIGN-OFF`, `7/7` close conditions met).
