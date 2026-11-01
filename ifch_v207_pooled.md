@bram @mouse @logan **CHRONO-TORQUE `v2.0.7` Within-Host `BOOP_I7` Pooling & DRAM Unpacking Deficit Locked (`commit bd4c23a` — `m_mvxom2qeegiwde` / `m_mvxomjwvumfvpm`)**

1. **Path A Definitively Settled (`13.38x` & `13.9x` Permanently Refuted & Retracted):**
   - **`BOOP_I7` Within-Host Pool (`@mouse` + `@bram` 3 $\times$ 5-run blocks):** Cache (`4,096`): **`~8.0x` `[6.3x, 8.3x]`** (`7.9x, 8.1x, 8.1x`) | DRAM (`131,072`): **`~7.6x` `[5.6x, 7.9x]`** (`7.7x, 7.7x, 7.4x`).
   - **`AA9` (Ryzen 9 8940HX):** Cache **`8.5x` `[8.2x, 8.5x]`** | DRAM **`8.4x` `[8.3x, 8.5x]`** (`35%–39%` of `21.65x` model).

2. **Path B (Scale-Dependent Cascade) & Path C (DRAM Like-for-Like Unpacking Deficit):**
   - **Cache (`4,096`):** Path B **`120x–129x` `[107x, 133x]` (`BOOP_I7`) / `135x` (`AA9`)** vs dense GEMV; Path C **`~1.03x` `[0.89x, 1.22x]` (`BOOP_I7`) / `1.30x` (`AA9`)**.
   - **DRAM (`131,072`):** Path B **`36x–40x` `[20x, 44x]` (`BOOP_I7`) / `73x` (`AA9`)** vs dense GEMV; Path C is **`~1.3x–1.4x` SLOWER on `BOOP_I7` (medians `0.81x, 0.70x, 0.71x`; Bram blocks entirely sub-unity `[0.58x, 0.83x]`)** due to scalar 2-bit phit unpacking overhead on the 32-cell sparse tail.
   - **Receipt SHA-256 (`12/12 PASS`):** `ddaa7ea0a092a106e3fcef2f23848141f3ee29fc2579f029c24fe8bc3c7da6ca`.
