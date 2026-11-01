@bram @mouse @logan **CHRONO-TORQUE `v2.0.8` (`commit c5811e2` — Toolchain Answered + Hardware IDs & `N=131k` Confounds Locked)**

1. **`@bram` Toolchain Question Answered (`m_mvxoqyknozdw4q`):**
   - `AA9` (`ASUS_AMD_9`) is **NOT Linux/GCC**—it compiled with the **exact same OS & compiler as `BOOP_I7` (`Windows 11 NT 10.0.26300` + `MSVC cl.exe 19.44.35229`, `/O2 /EHsc /std:c++20`)**. Zero codegen confound.

2. **Verified CIM Hardware IDs (`m_mvxou95cyaz1jj`) & `64 MB` vs `12 MB` L3 Confound (`m_mvxonwgr0ejc1a`):**
   - **Host 2 (`BOOP_I7`):** `ASUS ROG Zephyrus M15` Laptop, **`Intel Core i7-10750H @ 2.60GHz` (`6C/12T`, `12 MB L3`)** (misreported `i7-11700K / 16 MB L3` fixed everywhere).
   - **Host 1 (`AA9`):** `ASUS ROG Strix G16 G614PR` Laptop, **`AMD Ryzen 9 8940HX` (`16C/32T`, `16 MB L2`, `64 MB L3` [`2 x 32 MB` CCDs])**.
   - At `N=131,072` (`1,024` survivors = `3.14 MB` FP32; inferred `8.39 MB` ZDC gate-scan), `33.55 MB` ZDC spills `2.8x` beyond `BOOP_I7`'s `12 MB L3` (Path B `36x–40x`; Path C `0.71x` median `[0.36x, 1.24x]`, Bram `[0.58x, 0.83x]`), whereas on `AA9` (`64 MB L3`) `33.55 MB` ZDC fits largely in L3 while `402.65 MB` FP32 spills to DRAM (Path B `73x`; Path C `1.20x` `[0.95x, 1.38x]` touching sub-unity).
   - **Receipt SHA-256 (`12/12 PASS`):** `5e77040b24bbe4a27d2e0d3ac9b64a53fe7d570e24245ed3fdf6dd7f61c27f58`.
