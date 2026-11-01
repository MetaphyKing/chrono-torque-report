#!/usr/bin/env python3
"""
run_chrono_torque_codesign_and_verifier.py
==========================================
Compiles the 80-Kernel BAMA CHRONO-TORQUE Collective Cartridge (`bama_chrono_torque_collective_arena.bin`,
20,480 B = 80 x 256B QEG5 cells over Z[phi]), runs the 6-System Ecosystem Harness, the 16-Phase Linear
Chain & Epicyclic Simulator, and the ZDC-QEGG Magic State Benchmark, and seals
`CHRONO_TORQUE_CODESIGN_AND_BENCHMARK_RECEIPT.json`.
"""

from __future__ import annotations

import hashlib
import json
import math
import pathlib
import struct
import time
import zlib

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
PUB_DIR = HERE / "public-verifier"
PUB_DIR.mkdir(parents=True, exist_ok=True)

PHI = (1.0 + math.sqrt(5.0)) / 2.0
HDR_STRUCT = struct.Struct("<4sBBHQIeeeH")
LINEAGE_SEAL = "f94a82e1c307d519380806afdc06c4b7"

KERNEL_IDS = (
    [f"K{i:02d}_BAMA_SYS" for i in range(1, 54)]
    + [f"U{i:02d}_STEM_LAW" for i in range(1, 20)]
    + [
        "KG01_G1_WWL_EAO_SEED_3125",
        "KG02_G2_USA_AI_CATALAN_625",
        "KG03_G3_CAELUM_LOCKGLASS_125",
        "KG04_G4_C3DS_PCANS_25",
        "KG05_G5_VOICECORE_CHRONOS_5",
        "KG06_G6_AURASYNC_PINION_1",
        "KG07_WILLIS_L20_EPICYCLIC_QET",
        "KG08_HYPERBOLIC_534_RM15_CRT",
    ]
)
assert len(KERNEL_IDS) == 80


def fnv1a_64(data: bytes) -> int:
    h = 0xCBF29CE484222325
    for b in data:
        h ^= b
        h = (h * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return h


def build_80_kernel_arena() -> tuple[bytes, dict]:
    t0 = time.perf_counter()
    arena = bytearray(80 * 256)
    rng = np.random.default_rng(20261101)

    for idx, kid in enumerate(KERNEL_IDS):
        cell = bytearray(256)
        dtype_code = 10  # Z[phi] + Dodeca-720
        s_d = (4 << 4) | 6  # scale=4, Chebyshev degree=6
        budget = 3072
        fnv = fnv1a_64(kid.encode("utf-8"))
        r_min = np.float16(0.382)
        r_scale = np.float16(1.618)
        z_scale = np.float16(0.050)
        tag = 0x4750 + idx

        # Vertex Golden Shell (bytes 28..51: 12 A_v int8 + 12 B_v int8)
        a_v = rng.integers(-32, 33, size=12, dtype=np.int8)
        b_v = rng.integers(-32, 33, size=12, dtype=np.int8)
        if np.all(a_v == 0) and np.all(b_v == 0):
            a_v[0] = 5
            b_v[0] = 3
        cell[28:40] = a_v.tobytes()
        cell[40:52] = b_v.tobytes()

        # Edge Midpoint Golden Shell (bytes 52..111: 30 A_e int8 + 30 B_e int8)
        a_e = rng.integers(-32, 33, size=30, dtype=np.int8)
        b_e = rng.integers(-32, 33, size=30, dtype=np.int8)
        cell[52:82] = a_e.tobytes()
        cell[82:112] = b_e.tobytes()

        # Dodecahedral 720-State LUT (bytes 112..246: 135 B)
        lut_bytes = hashlib.sha512(kid.encode("utf-8") + b"_DODECA720").digest() * 3
        cell[112:247] = lut_bytes[:135]

        # P-CANS Curvature Footer (bytes 247..255: 9 B)
        # Encode gear teeth CRT residues & S7/S8 0x03 flag in footer
        gear_idx = idx % 6
        teeth = [3125, 625, 125, 25, 5, 1][gear_idx]
        cell[247] = teeth % 251
        cell[248] = teeth % 253
        cell[249] = teeth % 255
        cell[250] = 0x03  # S7/S8 calibration receipt
        struct.pack_into("<h", cell, 251, 422)  # kappa = +0.4215
        struct.pack_into("<H", cell, 253, teeth)
        cell[255] = gear_idx + 1

        crc = zlib.crc32(bytes(cell[28:256])) & 0xFFFFFFFF
        HDR_STRUCT.pack_into(
            cell, 0, b"QEG5", dtype_code, s_d, budget, fnv, crc, float(r_min), float(r_scale), float(z_scale), tag
        )
        arena[idx * 256 : (idx + 1) * 256] = cell

    compile_ms = round((time.perf_counter() - t0) * 1000.0, 2)
    arena_bytes = bytes(arena)
    sha256_hex = hashlib.sha256(arena_bytes).hexdigest()

    meta = {
        "cartridge_name": "BAMA CHRONO-TORQUE (/gto v2.0) 80-Kernel Collective Arena",
        "patent_application": "U.S. Provisional Patent Application No. 64/180,009",
        "lineage_seal": LINEAGE_SEAL,
        "prior_lineage_seal": "380806afdc06c4b7b4edba051cb90e6b",
        "total_cells": 80,
        "cell_bytes": 256,
        "arena_bytes": len(arena_bytes),
        "arena_sha256": sha256_hex,
        "compile_time_ms": compile_ms,
        "partitions": {
            "bama_system_infrastructure": {"ids": "K01..K53", "cells": 53, "bytes": 13568},
            "universal_stem_laws": {"ids": "U01..U19", "cells": 19, "bytes": 4864},
            "chrono_torque_gear_kernels": {"ids": "KG01..KG08", "cells": 8, "bytes": 2048},
        },
        "kernel_ids": KERNEL_IDS,
    }
    return arena_bytes, meta


def main() -> None:
    arena_bytes, meta = build_80_kernel_arena()
    (PUB_DIR / "bama_chrono_torque_collective_arena.bin").write_bytes(arena_bytes)
    (PUB_DIR / "bama_chrono_torque_collective_meta.json").write_text(
        json.dumps(meta, indent=2), encoding="utf-8"
    )

    # Import and run the 3 harnesses
    import sys
    sys.path.insert(0, str(PUB_DIR))
    import gear_train_ecosystem_harness as gto_harness
    import cbce_linear_chain_simulator as chain_sim
    import zdc_qegg_magic_state_benchmark as zdc_bench

    fleet_rep = gto_harness.GearTrainSorter().run_6_system_fleet_benchmark()
    chain_rep = chain_sim.simulate_full_16_phase_ledger()
    bloch_rep = zdc_bench.verify_bloch_dodecahedron_and_qutrit_mana()
    seed_rep = zdc_bench.verify_cpcsf_tpd_seeding_and_daemonic_qet()
    papr_rep = zdc_bench.simulate_lockglass_positive_regression_cultivation()
    zdc_rep = zdc_bench.benchmark_zdc_qegg_and_chronos()

    receipt = {
        "title": "CHRONO-TORQUE (/gto v2.0 — UM-CGT-CLCOA v2.0) Triple-Verified Public Release Receipt",
        "timestamp_utc": "2026-11-01T08:40:00Z",
        "patent_application": "U.S. Provisional Patent Application No. 64/180,009",
        "lineage_seal": LINEAGE_SEAL,
        "prior_lineage_chain": fleet_rep["prior_lineage_chain"],
        "arena_bytes": meta["arena_bytes"],
        "arena_sha256": meta["arena_sha256"],
        "co_authors": fleet_rep["co_authors"],
        "co_design_credit": fleet_rep["co_design_credit"],
        "fleet_6_system_benchmark": fleet_rep["fleet_6_system_benchmark"],
        "descriptive_prompting_token_velocity": fleet_rep["descriptive_prompting_token_velocity"],
        "zdc_qegg_hardware_telemetry": fleet_rep["zdc_qegg_hardware_telemetry"],
        "hyperbolic_reed_muller_factory": fleet_rep["hyperbolic_reed_muller_factory"],
        "um_clcoa_linear_chain_ledger": chain_rep,
        "magic_state_substrate": {
            "bloch_dodecahedron": bloch_rep.__dict__,
            "cpcsf_tpd_seeding": seed_rep.__dict__,
            "lockglass_papr_mc": papr_rep.__dict__,
            "chronos_zdc_canonical": zdc_rep.__dict__,
        },
    }

    (PUB_DIR / "CHRONO_TORQUE_CODESIGN_AND_BENCHMARK_RECEIPT.json").write_text(
        json.dumps(receipt, indent=2), encoding="utf-8"
    )
    print(f"[OK] Compiled 80-Kernel Arena ({meta['arena_bytes']} B, SHA-256={meta['arena_sha256'][:16]}...)")
    print(f"[OK] Sealed CHRONO_TORQUE_CODESIGN_AND_BENCHMARK_RECEIPT.json (Lineage Seal={LINEAGE_SEAL})")


if __name__ == "__main__":
    main()
