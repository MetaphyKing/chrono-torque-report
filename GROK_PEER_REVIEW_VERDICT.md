# Pass-3 Independent Peer Review — CHRONO-TORQUE (`/gto v2.0`)

**Reviewer:** Grok (independent Pass-3)  
**Date:** 2026-11-01  
**Repository:** `C:\dev\chrono-torque-report`  
**Artifacts:** `arxiv/chrono_torque_gto_arxiv_discovery_paper.tex`, `arxiv/metaphy_cbce_linear_chain_algorithm.tex`, `public-verifier/verify_chrono_torque_public_cartridge.py`, `public-verifier/gear_train_ecosystem_harness.py`, `public-verifier/CHRONO_TORQUE_CODESIGN_AND_BENCHMARK_RECEIPT.json`  
**Lineage string under test:** `f94a82e1c307d519380806afdc06c4b7`

## Verdict

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
