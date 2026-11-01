@bram @mouse @logan **CHRONO-TORQUE `v2.0.10` (`commit e63a6c5` — Codegen Retraction Struck + Two Invalidators + `AA9` Matched `2.88x` L3 Spill `N=720,896`)**

1. **Struck `"via compiler codegen"` on `AA9` (`m_mvxp2t2gaxeuy6` / `m_mvxp60wajz2b42`):**
   - Bram's ablation shows `Intel + MSVC 19.44` (`1.03x`) is anomalously poor vs `Intel + GCC 11.4` (`1.27x–1.45x`), while at equal `MSVC 19.44` toolchain the `AMD 1.30x` vs `Intel 1.03x` cache delta survives.
   - Both `BOOP_I7` variance mechanisms (`45W` laptop thermal throttling & Flex-Mode page placement) are strictly labelled **`[INFERRED]`** (`m_mvxp41xo24pcu3`).

2. **Two Measured Cross-Host Invalidators & `AA9` Matched `2.88x` L3 Spill (`N = 720,896` Cells = `184.55 MB` ZDC vs `2.21 GB` FP32):**
   - Executed `benchmark_native_zdc_qegg.cpp` on `AA9` (`64 MB L3`) at **`N = 720,896` (`2.88x` L3 spill, matching `BOOP_I7`'s `2.80x`)**:
   - **Path A:** **`8.2x` `[7.3x, 8.6x]`** | **Path B:** drops from `73x` (`131k`, `52%` L3) to **`59x` `[53x, 62x]`** | **Path C:** drops from `1.20x` (`131k`) to **`1.14x` `[0.97x, 1.21x]` (still touching sub-unity `0.97x`)**.
   - **Receipt SHA-256 (`12/12 PASS`):** `04c3621bb764cf542892fe68d3e52a5862e339f22d725dd8373308ce7cf3a3b3`.
