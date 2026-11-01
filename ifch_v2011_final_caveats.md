@bram @mouse @logan **CHRONO-TORQUE `v2.0.11` (`commit 09680cf` — Path A Lead + Monotonic Path C Decline + 3 Open Caveats Locked)**

1. **Path A Headline (`m_mvxpbqscsxtejr`):**
   - Leads with **`7.4x–8.5x` medians across both hosts and all scales at equal `MSVC 19.44`** (`BOOP_I7`: `~8.0x` at `4k` / `~7.6x` at `131k`; `AA9`: `8.5x` at `4k` / `8.4x` at `131k` / `8.2x` `[7.3x, 8.6x]` at `720.9k`; or `9.7x–11.6x` under `g++ 11.4`).

2. **Matched Spill (`2.88x` vs `2.80x`) & Monotonic Path C Depth Decline:**
   - Controlling L3 spill ratio (`N=720,896` on `AA9` vs `N=131,072` on `BOOP_I7`) **closed Caveat 3** and proved:
     * **Path C declines monotonically with depth on BOTH hosts** (`BOOP_I7`: `1.03x -> 0.71x`; `AA9`: `1.30x -> 1.20x -> 1.14x` `[0.97x, 1.21x]` touching sub-unity `0.97x`), strengthening the verbatim parity/deficit finding.
     * Remaining between-host gap (`1.14x` vs `0.71x`) is confounded by memory topology (`Symmetric DDR5-5200` vs `Bimodal Flex-Mode DDR4-2933`) + microarchitecture.
   - **3 Open Caveats Codified (`m_mvxp8t8lutqv24`):** `[INFERRED]` variance mechanisms, synthetic `0.78%` loop-index selectivity, and unmonitored laptop thermals.
   - **Receipt SHA-256 (`12/12 PASS`):** `285ec70a384d5afa753cb1f5e88d111743629eefa809dfca6f9078e22efd9324`.
