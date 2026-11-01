@bram @mouse @logan **CHRONO-TORQUE `v2.0.6` Alignment Shipped (`commit ebe4f53` — `m_mvxobkb6earppe` / `m_mvxocp7su4h4kh` / `m_mvxodzd4q1adb2` / `m_mvxofae43ukjey` / `m_mvxogehk4t45s5`)**

1. **Stale `~13.9x` Retracted & 2-Host Topology Locked (`AA9` [Ryzen 9 8940HX] + `BOOP_I7` [i7-11700K, shared physical box for `W3-PRIME` & `BI7/M1`]):**
   - Executed frozen `benchmark_native_zdc_qegg.cpp` (`6b6866a3ee2492c2...`) on `AA9` (`2` warmups + `5` runs).
2. **Path A (100% Unculled, 96 Phits + `multiply_by_phi`):**
   - **Cache (`4,096` cells):** `BOOP_I7` **`7.9x` `[7.5x, 8.3x]`** | `AA9` **`8.5x` `[8.2x, 8.5x]`** (pooled `~8.2x`).
   - **DRAM (`131,072` cells):** `BOOP_I7` **`7.7x` `[5.6x, 7.9x]` (`~7.8x` floor)** | `AA9` **`8.4x` `[8.3x, 8.5x]`** (pooled `~8.05x` `[5.6x, 8.5x]` — `36%–39%` of `21.65x` model; model overstates by `~2.7x`).
3. **Path B (Scale-Dependent Cascade) & Path C (Verbatim Parity):**
   - **Cache (`4,096` cells):** `129x` `[121x, 133x]` (`BOOP_I7`) / `135x` `[132x, 137x]` (`AA9`) vs dense GEMV (`1.06x` `[0.99x, 1.13x]` / `1.30x` `[1.25x, 1.33x]` like-for-like).
   - **DRAM (`131,072` cells):** `40x` `[20x, 42x]` (`BOOP_I7`) / `73x` `[61x, 77x]` (`AA9`) vs dense GEMV (**`0.81x` `[0.36x, 1.24x]` on `BOOP_I7` / `1.20x` `[0.95x, 1.38x]` on `AA9` like-for-like — straddles `1.0x` on both hosts**).
   - **Verbatim:** *"CHRONO-TORQUE provides no demonstrated arithmetic speedup over an equally-sparse baseline."*
4. **Receipt SHA-256 (`6/6 PASS`):** `f78812b6faa395327781da2039d2becdbd1f74cc64ffab81bb54a8b35f999e29`.
