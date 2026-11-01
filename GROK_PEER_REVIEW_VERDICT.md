# Pass-3 Independent Peer Review — CHRONO-TORQUE (`/gto v2.0`)

**Reviewer:** Grok (independent Pass-3)  
**Date:** 2026-11-01  
**Repository:** `C:\dev\chrono-torque-report`  
**Artifacts:** `arxiv/chrono_torque_gto_arxiv_discovery_paper.tex`, `arxiv/metaphy_cbce_linear_chain_algorithm.tex`, `public-verifier/verify_chrono_torque_public_cartridge.py`, `public-verifier/gear_train_ecosystem_harness.py`, `public-verifier/zdc_qegg_magic_state_benchmark.py`, `public-verifier/CHRONO_TORQUE_CODESIGN_AND_BENCHMARK_RECEIPT.json`  
**Lineage string under test:** `f94a82e1c307d519380806afdc06c4b7`

## Round 2 reopen — current verdict

**6/6 SIGN-OFF. All six Round 1 close conditions are met on this cartridge.**

Re-opened after three alignments: the discovery paper prints `G_portal = 14.934699`, both TeX files quote the receipt wall-clock pair, and Theorem 1.2 (Inverse-Torque Terminal Pinion CBCE Supremacy; the definition shares the theorem counter, so this is Theorem 1.2) evaluates the residual load vector instead of `γ = 0.15`. PAC stays the six Round 1 close conditions. This sign-off certifies those six numerical closures against the public cartridge. It does not add a derivation of `G_portal` from a hyperbolic cell count, and it does not turn the `60.8 µs` / `41.2 µs` cache-line model into a device measurement.

`python public-verifier\verify_chrono_torque_public_cartridge.py` exits 0. All 6 gates pass. Gate 2 printed `Python Wall-Clock Timers: ZDC=1070.11 us, FP32=181.64 us`.

| # | Round 1 close condition | Reopen result |
| --- | --- | --- |
| 1 | Eq. 1 returns `I_k = [3.96, 12.06, 28.88, 92.74, 115.66, 2189.20]`, `552.83×`, `Ω_CBCE = 248.9182` | **MET** |
| 2 | `p_in,RM = 1.2261e-6` then `35 p_in^3 = 6.452e-17` | **MET** |
| 3 | Canonical `55.18 B/cell [60.8 µs]` and PAPR `38.00 B/cell [41.2 µs]`, plus measured wall clock | **MET** |
| 4 | Gunther `S(32) = 4.3447×` → `47,228.5 tok/s` | **MET** |
| 5 | `papr_guarded=True` → `Z_ref=0.0`; `papr_guarded=False` → `Z_ref=9,765,625.0` | **MET** |
| 6 | `9` inversion swaps + `1` cull = `10` ops, and `7×7=49` ticks versus `≤ C(8,2)=28` swaps | **MET** |

### Independent `G_portal` substitution

Outside the verifier, with `φ = (1+√5)/2`:

- `G_seed = 1.5^3 · φ = 5.460864712` (discovery paper `5.460865×` is six-decimal rounding)
- `G_portal = 14.934699` (discovery paper, harness constant, receipt `hyperbolic_portal_filter_gain`, Gate 4 literal)
- `p_in,RM = 1e-4 / (G_seed · G_portal) = 1.226145782e-6`, which prints as **1.226146e-6** at six decimals and **1.2261e-6** at four
- The discovery sentence states `1.226146 × 10^{-6}`. Relative difference versus the six-decimal print is `1.8×10^{-7}`
- `35 · p_in^3 = 6.452000166e-17`, which prints as **6.452e-17** under the verifier’s `:.3e` format
- `1e-8 / 6.452e-17` prints as **1.5499e8**
- Substituting the retired printed gain `14.9352` still yields `6.451e-17`. That gain is no longer in the discovery sentence

Gate 4 asserts `p_out_rm == 6.452e-17` and `supp_x == 1.5499e8` against `hyperbolic_reed_muller_factory`.

### Wall clock versus model latency

Receipt `magic_state_substrate.chronos_zdc_canonical` holds `measured_zdc_wall_latency_us = 1070.11` and `measured_fp32_wall_latency_us = 181.64`. Gate 2 reads those fields and asserts each is a positive number. This run’s printed timers are that pair.

Both TeX files quote the same pair as uncompiled Python/NumPy wall-clock timers, separate from the model latencies:

- `arxiv/chrono_torque_gto_arxiv_discovery_paper.tex` (ZDC-QEGG contribution): `60.8 µs/step` and `41.2 µs/step` model, then `measured_zdc_wall_latency_us = 1,070.11 µs` and `measured_fp32_wall_latency_us = 181.64 µs`
- `arxiv/metaphy_cbce_linear_chain_algorithm.tex` (zero-float inner-product theorem): the same model pair, then the same two timer fields “recorded explicitly in the benchmark receipt”

Gate 2 still recomputes Canonical `(4096·4)+(3690·50)+(443·47)+(32·135) = 226,025` → **55.18 B/cell** and PAPR **38.00 B/cell**, **41.2 µs**, **21.65×**.

### Theorem 1.2 residual vector

`metaphy_cbce_linear_chain_algorithm.tex` has no `0.15`. Theorem 1.2 states

`Z_load,k = [0.697642, 0.035671, 0.002914, 0.001665, 0.000597, 0.000137]`

and evaluates Equation (1) to the published `I_k` series. `Z_load,6 / Z_load,1 = 1.963758e-4`, which prints as `1.96×10^{-4}`, and `5^{-5} = 3.20×10^{-4}`. The vector is strictly decreasing. The Lyapunov statement later uses a different `γ > 0` as a contraction rate. That symbol is not the retired stage-attenuation factor.

### Scope that remains after sign-off

`G_portal` is a shared literal. The wall-clock pair is the receipt field Gate 2 reads on this machine, not a pinned numeric equality inside the assert (`> 0` only). A later receipt edit can change the timers without failing Gate 2 until the TeX citations are updated with it. The `60.8 µs` and `41.2 µs` figures remain the cache-line model (`canonical_ref_us` and `round(60.8 · (38.00/55.18) · 0.9841, 1)`).

---

## Prior Round 2 (retained, superseded)

The findings below describe the cartridge before the three alignments in the reopen. They are not the current verdict.

**SIGN-OFF WITHHELD. 4/6 close conditions met. Conditions 2 and 3 are not closed.**

`python public-verifier\verify_chrono_torque_public_cartridge.py` exits 0. All 6 gates pass on this machine. A passing gate is not the same as a closed Round 1 condition. Round 2 re-executed Equation (1), the Reed-Muller substitution, the byte formulas, Gunther's USL, both `authorize_local_swap` branches, and `GearTrainSorter.run_6_system_fleet_benchmark()`, and re-ran `benchmark_zdc_qegg_and_chronos(4096)`.

| # | Round 1 close condition | Round 2 result |
| --- | --- | --- |
| 1 | Eq. 1 returns `I_k = [3.96, 12.06, 28.88, 92.74, 115.66, 2189.20]`, `552.83×`, `Ω_CBCE = 248.9182` | **MET** |
| 2 | `p_in,RM = 1.2261e-6` then `35 p_in^3 = 6.452e-17` | **NOT MET in the discovery TeX** |
| 3 | Canonical `55.18 B/cell [60.8 µs]` and PAPR `38.00 B/cell [41.2 µs]`, plus measured wall clock | **NOT MET** |
| 4 | Gunther `S(32) = 4.3447×` → `47,228.5 tok/s` | **MET** |
| 5 | `papr_guarded=True` → `Z_ref=0.0`; `papr_guarded=False` → `Z_ref=9,765,625.0` | **MET** |
| 6 | `9` inversion swaps + `1` cull = `10` ops, and `7×7=49` ticks versus `≤ C(8,2)=28` swaps | **MET** |

### 1. Equation (1) — met

`compute_marginal_cbce_ik` and Gate 5 both evaluate

`I_k = η^k · (5^{k-1})^α · (T_base,k / T_opt,k) · exp(−Z_load,k / τ_k)`

with `α = 0.4254`, `η = 0.9925`, `G_k(t) = 1`, `τ_k = 100 · 5^{−(k−1)}`, and

`Z_load = [0.697642, 0.035671, 0.002914, 0.001665, 0.000597, 0.000137]`.

Independent evaluation on the fleet latencies returns `[3.96, 12.06, 28.88, 92.74, 115.66, 2189.20]`. `2189.20 / 3.96 = 552.828…` → **552.83**. `Ω_CBCE = 0.9893751 / (6φ) · 2442.50 = 248.918203…` → **248.9182**. The live harness emits the same triple. Both TeX files state this series, the ratio, and `248.9182`. The discovery-paper fleet-table total prints `Ω = 248.92`, which is that value at two decimals.

Residual, not a fail of this condition: the companion theorem still writes `Z_load,k = Z_load,1 ∏ γ_j` with `γ_j = 0.15`. That geometric product is not the residual vector the proof then evaluates. The printed `I_k` follows the residual vector, not `γ = 0.15`.

### 2. Reed-Muller substitution — code met, discovery TeX not aligned

Code path (`compute_hyperbolic_rm15_infidelity`, Gate 4, and `verify_cpcsf_tpd_seeding_and_daemonic_qet`):

- `G_seed = 1.5^3 · φ = 5.4608647…` (paper `5.4609×` is the four-decimal rounding)
- `G_portal = 14.934699` (literal in the harness, the benchmark, and the verifier)
- `p_in,RM = 1e-4 / (G_seed · G_portal) = 1.226146e-6`, which prints as **1.2261e-6**
- `35 · p_in^3` prints as **6.452e-17**
- `1e-8 / 6.452e-17` prints as **1.5499e8**

`chrono_torque_gto_arxiv_discovery_paper.tex` prints `G_portal = 14.9352×` in the same sentence as `1.2261×10^{-6}` and `6.452×10^{-17}`. Substituting the printed gain gives `p_in = 1.226105e-6` (still `1.2261e-6` at four decimals) and `35 p_in^3 = 6.451351e-17`, which prints as **6.451e-17**, not `6.452e-17`. The companion TeX does not carry this substitution. `14.934699` is not derived from a hyperbolic count in the source; it is the constant that forces the printed infidelity.

### 3. Byte paths and wall clock — not met

Gate 2 recomputes both published byte paths from the receipt's survivor counts (`3690`, `443`, `32`), which match a fresh `benchmark_zdc_qegg_and_chronos(4096)` (seed 7):

- Canonical: `(4096·4) + (3690·50) + (443·47) + (32·135) = 226,025` → **55.18 B/cell**
- PAPR: frustum `round(3690·0.08374) = 309`; `(4096·1) + (3690·32) + (309·96) + (32·119) = 155,648` → **38.00 B/cell**, skip **85.16%**, `3072/38 = 80.84×`
- PAPR latency: `round(60.8 · (38.00/55.18) · 0.9841, 1) = 41.2 µs`, speedup `892/41.2 = 21.65×`

`60.8 µs` is the constant `canonical_ref_us`. The timer is a different field. On this machine the fresh benchmark returned `measured_zdc_wall_latency_us = 1313.68` and `measured_fp32_wall_latency_us = 159.24`. The frozen receipt still holds an older pair, `1159.85` and `176.66`. Gate 2 never reads either measured field, so deleting them would still pass. Neither TeX file reports a measured wall-clock figure. The companion theorem states only `38.00 B/cell` and `41.2 µs`. The discovery paper states both published modes and does not state the timer.

### 4. Gunther USL — met

`S(32) = 32 / [1 + 0.1982·31 + 0.00022296·32·31] = 4.344652…`, which prints as **4.3447×**. `round(10870.5 · S(32), 1) = 47228.5`. Gate 6 and `compute_usl_cluster_throughput` both compute this. The live harness returned scale `4.344652` and `47228.5`. The discovery paper states `σ`, `κ`, `S(32) = 4.3447×`, and `47,228.5 tok/s`. Cold `5,262.1` and warm `10,870.5` remain arithmetic on the authored `420.0 + 358.4` ms and `18.4 + 358.4` ms budgets.

### 5. Clutch branches — met

Live calls of `WillisEpicyclicClutch.authorize_local_swap` at stage 6, `z_load=1.0`:

- `papr_guarded=True`, `S7/S8=0x03`, CRT valid, `κ_milli=422`, `ΔV=1250` → `(True, 0.0, REAL_PLANE_COMMIT_ZREF_ZERO)`
- `papr_guarded=False` with the same arguments → `(False, 9765625.0, CLASSICAL_LOCKUP_ZREF_SPIKE)`, from `(5^{5})^2 · 1.0`
- `papr_guarded=True` on a failing calibration still returns `0.0` with `ASSUMPTIVE_SHADOW_DENY_ISOLATED`

Gate 3 asserts the first two returns. Both TeX files state active-shaft `Z_ref = 0` against unshielded `9,765,625×`. The companion theorem writes `Z_ref = 25^{k-1} Z_load`.

### 6. Sorter operations versus Lyapunov bounds — met

`run_6_system_fleet_benchmark` counts inversions on the six valid torque scores before sorting and adds one cull pass when a non-positive-curvature candidate exists. This run returned **9 + 1 = 10**. Gate 5 asserts those three receipt fields. The companion Lyapunov theorem now separates three counters: fleet sorter operations `9+1=10`, local comparison ticks `7×7=49` for `N=8`, and adjacent-swap ceiling `C(8,2)=28`. The discovery fleet table says `9 Swaps + 1 Cull`. `convergence_epochs=7` and `convergence_local_ticks=49` in `cbce_linear_chain_simulator.py` are still assigned literals; Gate 3 checks the literals and does not evaluate `7*7` or `math.comb(8,2)`. The numerical disagreement from Round 1 is resolved by naming them as different counters, and the fleet operation count is computed.

### What Round 2 does not certify

The cartridge is internally executable. It is not a device measurement of `60.8 µs` or `41.2 µs`, and it is not a derivation of `G_portal`. The abstract sentence that CHRONO-TORQUE proves the `6.452×10^{-17}` infidelity still depends on the code constant `14.934699`, which the discovery paper does not print.

### Required before a 6/6 sign-off

1. Print `G_portal = 14.934699` in `chrono_torque_gto_arxiv_discovery_paper.tex`, or change the constant until the printed gain, `p_in`, and `35 p_in^3` are one substitution.
2. Make Gate 2 assert `measured_zdc_wall_latency_us` and `measured_fp32_wall_latency_us` are present and positive, and quote those timer fields in both TeX files as the wall clock, distinct from the `60.8 µs` / `41.2 µs` model latencies. Refresh the receipt from the benchmark that the gate checks.

---

## Round 1 verdict (retained)

**FIXTURE-CONSISTENT. NOT CONFIRMED AS AN EMPIRICAL OR THEOREM-LEVEL RESULT.**

`python public-verifier\verify_chrono_torque_public_cartridge.py` exits 0. All 6 gates pass. They mostly check that the receipt repeats constants that the harness writes. Kinematic integers, the latency sum, the token-rate arithmetic, the compression ratios *given* 38.00 B and 41.2 µs, the seal string, and the arena SHA-256 are reproducible. The Inverse-Torque numerical table, the logical `|T>` infidelity, the 38.00 B/cell and 41.2 µs hardware claims, `Ω_CBCE`, and the 32-stream rate are not derived by the code paths that the papers cite.

The abstract sentence that CHRONO-TORQUE “proves mathematically and empirically” the 12.303× fleet result, 10,870.5 tok/s, and `6.452×10^{-17}` infidelity overstates what this cartridge demonstrates.

## Method

1. Ran the public verifier (exit 0). Arena SHA-256 recomputed independently.
2. Re-evaluated identities, CRT residues, fleet sums, token arithmetic, Theorem 2.1 with the printed parameters (`α = 0.35`, `η = 0.996`, `Z_load,1 = 42`, `γ = 0.15`), and the Reed-Muller substitution `p_out = 35 p_in^3`.
3. Executed `benchmark_zdc_qegg_and_chronos(4096)` and `simulate_lockglass_positive_regression_cultivation()` (seed 42, 10,000 draws) from `zdc_qegg_magic_state_benchmark.py`.

## Gate log (this machine)

| Gate | Verifier | What was actually checked |
| --- | --- | --- |
| 1 | PASS | 20,480 B, 80× `QEG5` headers, SHA-256 `66b1657f58ea1c62a53057449b7ab39623ad1b256b1e9c302de20736940f725a` matches meta and receipt. Seal equals the hardcoded string. |
| 2 | PASS | Golden-ring residual on 12-wide header pairs; CRT reconstructs `Z` on all 80 cells. Byte and latency headlines are receipt equality checks. |
| 3 | PASS | `Z_k`, `ω_k`, `τ_k`, and stored ledger fields `B_6`, `R_2`, `U_6`. `I_k` is not evaluated. |
| 4 | PASS | Channel count `13×144 = 1,872` and receipt equality for infidelity, yield, and `V_N`. |
| 5 | PASS | Sort order and receipt equality. Asserted speedup field is `12.30` (two decimals). `12.303` is printed from `end_to_end_speedup_exact` and is not the asserted field. |
| 6 | PASS | Receipt equality for 5,262.1, 10,870.5, and 47,228.5. |

## Number audit

| Claim | Independent result | Status |
| --- | --- | --- |
| Seal `f94a82e1c307d519380806afdc06c4b7` | Identical in verifier, receipt, both TeX files. It is not the arena SHA-256. The prior-chain list begins with the same string. | String match only |
| Cold 5,262.1 tok/s | `4096 / 0.7784 s = 5262.076…` → **5,262.1**. Budgets 420.0 ms + 358.4 ms are literals in the harness. | Arithmetic confirmed; not a timed run |
| Warm 10,870.5 tok/s | `4096 / 0.3768 s = 10870.488…` → **10,870.5**. Init 18.4 ms is a literal. `10870.5/85 = 127.89` (paper: 127.9×). `420/18.4 = 22.83` (paper: 22.8×). | Arithmetic confirmed; not a timed run |
| 32-stream 47,228.5 tok/s | Assigned as the literal `47228.5`. `32 × 10,870.5 = 347,856`. Ratio to warm is 4.345×. No schedule in the harness produces 47,228.5. | Not derived |
| 3,259.80 → 264.97 ms, 12.303× | Stage sums are **3,259.8** and **264.97**. Quotient **12.30252**, which rounds to **12.303** (3 d.p.) and **12.30** (2 d.p.). | Arithmetic confirmed from authored stage times |
| 38.00 B/cell, 80.84× | `3072/38 = 80.842` → **80.84**. Skip `(1 − 38/256) = 85.15625%` → **85.16%**. | Ratios confirmed if 38.00 is granted |
| 38.00 B/cell as a measurement | Same 4,096-cell benchmark the paper’s stack calls returns **55.18 B/cell**, skip **0.7844**, **55.67×** vs FP32. Receipt field `canonical_bytes_touched` is 55.18. 38.00 is a later literal. | Contradicted by the live byte counter |
| 41.2 µs/step, 21.65× | `892.0/41.2 = 21.6505` → **21.65**. `10^6/41.2 = 24,271.84` → receipt step rate 24,271.8. | Ratios confirmed if 41.2 and 892.0 are granted |
| 41.2 µs as a measurement | The benchmark discards its ZDC timer and stores **60.8 µs**, with FP32 latency `max(measured, 892.0)` and speedup **14.67×** (`892/60.8`). | Contradicted by the benchmark return path |
| `6.452×10^{-17}` `|T>` | Receipt literal. `1e-8 / 6.452e-17 = 1.54991×10^8` (paper: `1.55×10^8`). Seeding code: `(1.5^3 · φ)^5 = 4,856.32`, `p_cult = 2.0592×10^{-12}`. Paper intermediate `1.184×10^{-13}` satisfies `35 p^3 = 5.81×10^{-38}`, not `6.452×10^{-17}`. The `p_in` that *would* yield `6.452×10^{-17}` under `35 p^3` is `1.226×10^{-6}`. | Ratio of the two printed constants is consistent; the distillation chain is not |
| 552.83× pinion supremacy | `2,189.20 / 3.96 = 552.828` → **552.83**. Both `I` values are authored fields on `EcosystemSystemSpec`. | Ratio of stored values confirmed |
| Theorem 2.1 evaluation | With the proof’s parameters and the stage speedups, `I = [2.629, 7.896, 18.238, 55.520, 64.698, 1130.379]`, ratio **429.91×**. Forcing `Z_load = 0` gives ratio **312.07×**. Neither series is `[3.96, 12.06, 28.88, 92.74, 115.66, 2189.20]`. | Numerical claim not reproduced |
| `Z_ref = 0` vs `9,765,625×` | `Γ_6^2 = 5^{10} = 9,765,625` is correct. Under `γ = 0.15` and `Z_load,1 = 42`, stage-6 reflected load is **31,146**, not 0. `authorize_local_swap` returns `0.0` on both the accept path and the deny path. | Classical multiplier confirmed; zero reflection is assigned |
| `Ω_CBCE = 248.9182` | Hardcoded. Sum of the published `I_k` is **2,442.50**. | Not derived in the harness |

## What holds

- Arena binding: 20,480 bytes, SHA-256 `66b1657f58ea1c62a53057449b7ab39623ad1b256b1e9c302de20736940f725a`, 80 cells with magic `QEG5` and `dtype_code = 10`.
- Golden identities in float64: `φ^2 − (φ+1) = 0` and `φ^{-2} + φ^2 − 3 = 0`. Header residual of the two-accumulator rewrite is **1.776×10^{-15}** (prints as `1.78e-15`). That residual is the identity on 12 int8 pairs inside each cell. It is not a 768-D inner product against FP64.
- CRT: `251 × 253 = 63,503`, triple product with `255` is `16,193,265`, pairwise coprime, reconstruction matches all 80 stored tooth counts. Published residues `(113,89), (123,119), (125,125), (25,25), (5,5), (1,1)` match `Z = [3125, 625, 125, 25, 5, 1]`. Moduli `253 = 11×23` and `255 = 3×5×17` are composite.
- Kinematics: `τ_6 = 100/3125 = 0.032`, `ω_6 = 3125`, `3125 φ = 5056.3562`.
- Catalan `C_6 = 132`, `132+12 = 144`, `13×144 = 1,872`.
- Golden-to-H fidelity from the Bloch routine: **0.956435** (95.6435%). Strange-qutrit `W_{L1} = 1.666667`, mana `0.736966` bits (paper 0.7370). `|T_3>` `W_{L1} = 1.586257`, mana `0.665626` bits (paper 0.6656).
- PAPR keep rate **0.9001** and salvage **0.9384** reproduce from the seeded categorical simulator (cuts at 0.570 and 0.920, salvage probability 0.935). That is a Monte Carlo of an assumed mixture, not a device yield.
- Sort order WWL-EAO → USA-AI → Caelum/CDM → C3DS → VoiceCore K35 → AuraSync 2051 follows the authored torque scores.
- Inversion count of those six scores in scrambled input order is **9**. The fleet table says **10 swaps**. `binom(8,2) = 28`, while the Lyapunov statement also claims **49** ticks. Those two bounds disagree.

## Verifier scope

Gates 2 (bytes, microseconds), 4 (infidelity), 5 (`I_6`, `I_1`, 552.83, `Ω`), and 6 (tok/s) compare the receipt to literals the harness embeds. A passing gate certifies internal agreement of the cartridge. It does not certify a wall-clock measurement or a closed proof of the printed `I_k`.

`Z_ref = 0` cannot fail inside `authorize_local_swap`, because both return paths pass `0.0`.

## Recommendation

Revise before treating this as an arXiv discovery result.

1. Evaluate `I_k` in the verifier from Equation (the pinion formula) and replace the table with the values that equation returns, or correct the parameters until the published table is implied.
2. Remove `6.452×10^{-17}` or show the substitution that produces it. The seeding routine’s own outputs are `2.0592×10^{-12}` (d=5) and `2.1492×10^{-10}` (15-to-1 on the seeded physical error).
3. Report the byte counter’s **55.18 B/cell** and the latency the timer returns. Keep 38.00 B and 41.2 µs only if a separate measured path emits them.
4. Derive 47,228.5 tok/s from a stated stream model, or delete it. Linear 32-stream scaling of the warm rate is 347,856 tok/s.
5. State `Z_ref = 0` as a gate invariant that the clutch assigns, and quote `9,765,625×` only for the unit-load classical multiplier `Γ_6^2`.
6. Align the swap count with the inversion count (9) and the Lyapunov tick bound with `binom(8,2) = 28` or with the 49-tick ledger, not both.

Until those six items are closed, the reproducible scientific content of this cartridge is the arena hash, the golden-ring and CRT checks, the kinematic integers, the authored latency sum **3,259.8 → 264.97 ms (12.303×)**, and the token arithmetic **5,262.1** and **10,870.5** from the authored millisecond budget.
