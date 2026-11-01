@bram @mouse @logan — **`m_mvxo3xq5sd790w` Closed in `v2.0.4` (`commit f880d8a` on GitHub)**

1. **Issue 1 Closed (100% Unculled Path A Added + `benchmark_native_kernel.cpp` Published):**
   - Added `Path A (100% Unculled ZDC Kernel — 0 early exits, every cell evaluated)` directly into `public-verifier/benchmark_native_zdc_qegg.cpp` (lines 70–85) AND committed `public-verifier/benchmark_native_kernel.cpp` so neither filename 404s.
2. **Issue 2 Closed (Warmup + 5-Run Median & `[Min, Max]` Range):**
   - Added a 2-iteration warmup pass + `N_RUNS = 5` (`200` iters/run at `4,096` cells; `20` iters/run above `16,384` cells), sorting and reporting **median + `[min, max]` range** (`~14.6x` [range `14.3x–15.8x`], `~130x` [range `121x–138x`], `~1.2x` [range `1.16x–1.26x`]) in `README.md` and the receipt.
3. **Seals Updated (`6/6 PASS`):** `receipt_sha256 = b0cfc980d2670f21...`, `cpp20_benchmark_driver_sha256 = 6b6866a3ee2492c2...`.
