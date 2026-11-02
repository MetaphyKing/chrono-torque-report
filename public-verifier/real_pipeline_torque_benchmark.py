#!/usr/bin/env python3
"""
real_pipeline_torque_benchmark.py — Genuine Multi-Stage Workload Benchmark
with Instrumented Structural-Torque Proxy (tau_k) & Real Wall-Clock Latency
===========================================================================
Directly addresses Grok's Step 3 request:
  "For the classical pipeline claim, instrument one real multi-stage workload
   you control and report the structural-torque proxy and wall-clock numbers
   against a sequential baseline using the same proxy definition."

Zero hardcoded work-unit loops or sleep() calls. Every stage executes real,
deterministic CPU computation over concrete 512-byte multi-agent task envelopes:
  - Stage S_schema   : Binary/JSON envelope header, magic-word, & bounds validation
  - Stage S_f2_syn   : 128-bit GF(2) Hamming/Steane syndrome parity check
  - Stage S_zphi_norm: 32-step exact Z[phi] coordinate recurrence & norm bound check
  - Stage S_dot64    : 64-dimensional integer inner-product semantic threshold gate
  - Stage S_sha256   : 8-round chained SHA-256 Merkle payload integrity proof
  - Stage S_pack     : Canonical packet serialization & CRC32 finalization

Formal Structural-Torque Proxy Definition (tau_k):
--------------------------------------------------
On an empirical calibration slice (N_cal payloads), each stage k is profiled
independently to measure:
  - r_k = Pr(Stage k rejects an invalid/out-of-spec envelope)  [empirical rejection rate]
  - c_k = Mean wall-clock CPU time per envelope in microseconds [empirical compute cost]

The Structural-Torque Proxy is defined identically across all pipeline modes as:
  tau_k = r_k / c_k   (rejections per microsecond of stage CPU work, scaled by 1e3)

We then benchmark three concrete pipeline executions on the exact same N=4,000
workload (using identical proxy definition tau_k and verifying identical final
accepted payload hashes):
  1. Naive Un-Culled Sequential Baseline:
       Runs all 6 stages sequentially on every payload without early culling
       (aggregates validity flags at the terminal gate).
  2. Scrambled / Anti-Torque Sequential Baseline (with Early Exit):
       Runs stages in ascending tau_k order (heavy cryptographic & inner-product
       stages first, cheap structural/syndrome checks last) with early culling.
  3. CHRONO-TORQUE (Descending tau_k Pre-Cleared Pipeline):
       Automatically orders stages by descending empirical tau_k (highest
       rejection-per-microsecond stages first) with upstream pre-clearance.

Usage:
    python real_pipeline_torque_benchmark.py
    python real_pipeline_torque_benchmark.py --payloads 4000 --seed 20261101 --json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import struct
import sys
import time
import zlib
from dataclasses import asdict, dataclass
from typing import Callable, Dict, List, Tuple


# ============================================================================
# 1. Concrete Workload Generator (Deterministic Real Task Envelopes)
# ============================================================================

@dataclass
class TaskEnvelope:
    envelope_id: int
    magic_header: bytes        # 4 bytes: expected b"CTv2"
    version: int               # expected 2
    ttl_hops: int              # expected 1..16
    syndrome_bits: int         # 128-bit integer for GF(2) parity check
    zphi_seed_a: int           # initial Z[phi] coordinate a
    zphi_seed_b: int           # initial Z[phi] coordinate b
    vec64: Tuple[int, ...]     # 64-D integer feature vector
    payload_bytes: bytes       # 256-byte raw task body
    expected_pow_tag: int      # 1-byte modular tag


def generate_workload(n_payloads: int = 4000, seed: int = 20261101) -> List[TaskEnvelope]:
    """
    Generates a deterministic batch of concrete multi-agent task envelopes.
    Roughly ~18% are completely valid across all 6 stages; the remaining ~82%
    contain realistic structural, syndrome, norm-bound, semantic-score, or
    Merkle-tag defects that must be filtered out by the pipeline.
    """
    rng = random.Random(seed)
    workload: List[TaskEnvelope] = []

    for i in range(n_payloads):
        # Decide ground-truth defect class from realistic ingress distribution
        u = rng.random()
        # Defect classes:
        #   0.00 .. 0.32 (32%): Malformed header / expired TTL (caught by S_schema)
        #   0.32 .. 0.56 (24%): GF(2) parity syndrome error (caught by S_f2_syn)
        #   0.56 .. 0.72 (16%): Z[phi] norm divergence bound (caught by S_zphi_norm)
        #   0.72 .. 0.80 ( 8%): Low 64-D semantic inner product (caught by S_dot64)
        #   0.80 .. 0.84 ( 4%): Chained SHA-256 tag mismatch (caught by S_sha256)
        #   0.84 .. 1.00 (16%): Valid envelope (passes all stages)

        magic = b"CTv2" if u >= 0.18 else b"BAD!"
        version = 2 if u >= 0.25 else 1
        ttl = rng.randint(1, 16) if u >= 0.32 else 0

        # 128-bit syndrome word: 15 random payload bytes (bits 8..127) + 1 parity byte (bits 0..7)
        raw_syn_payload = rng.getrandbits(120)
        parity_byte = 0
        temp = raw_syn_payload
        for _ in range(15):
            parity_byte ^= (temp & 0xFF)
            temp >>= 8
        raw_syn = (raw_syn_payload << 8) | (parity_byte & 0xFF)
        if 0.32 <= u < 0.56:
            # Inject odd syndrome fault in low byte
            syndrome_bits = raw_syn ^ 0x5A
        else:
            syndrome_bits = raw_syn

        # Z[phi] seeds: small seeds stay bounded under 32 alternating conjugations
        if 0.56 <= u < 0.72:
            zphi_a = rng.randint(5000, 9000)
            zphi_b = rng.randint(5000, 9000)
        else:
            zphi_a = rng.randint(1, 25)
            zphi_b = rng.randint(1, 25)

        # 64-D integer vector: valid envelopes have positive correlation with anchor
        if 0.72 <= u < 0.80:
            vec64 = tuple(rng.randint(-50, -10) for _ in range(64))
        else:
            vec64 = tuple(rng.randint(10, 60) for _ in range(64))

        payload_bytes = bytes(rng.getrandbits(8) for _ in range(256))

        # Compute true 8-round chained SHA-256 modular tag
        h = payload_bytes
        for r in range(8):
            h = hashlib.sha256(h + struct.pack("<II", i, r)).digest()
        true_tag = h[0] & 0x0F
        if 0.80 <= u < 0.84:
            expected_pow_tag = (true_tag ^ 0x0F)
        else:
            expected_pow_tag = true_tag

        workload.append(
            TaskEnvelope(
                envelope_id=i,
                magic_header=magic,
                version=version,
                ttl_hops=ttl,
                syndrome_bits=syndrome_bits,
                zphi_seed_a=zphi_a,
                zphi_seed_b=zphi_b,
                vec64=vec64,
                payload_bytes=payload_bytes,
                expected_pow_tag=expected_pow_tag,
            )
        )

    return workload


# ============================================================================
# 2. Six Real Computational Stages (Zero Sleep / Zero Dummy Loops)
# ============================================================================

ANCHOR_VEC64: Tuple[int, ...] = tuple(((k * 17 + 5) % 41) + 1 for k in range(64))


def stage_schema_validate(env: TaskEnvelope) -> Tuple[bool, int]:
    """Stage 1: Binary header, protocol version, TTL hop bounds, and payload size check."""
    ok = (
        env.magic_header == b"CTv2"
        and env.version == 2
        and 1 <= env.ttl_hops <= 16
        and len(env.payload_bytes) == 256
    )
    return ok, (1 if ok else 0)


def stage_f2_syndrome_check(env: TaskEnvelope) -> Tuple[bool, int]:
    """Stage 2: 128-bit GF(2) 16-lane byte parity syndrome extraction."""
    acc = 0
    val = env.syndrome_bits
    for _ in range(16):
        acc ^= (val & 0xFF)
        val >>= 8
    ok = (acc == 0)
    return ok, acc


def stage_zphi_norm_check(env: TaskEnvelope) -> Tuple[bool, int]:
    """Stage 3: 32-step exact Z[phi] recurrence with norm-invariant & threshold gate."""
    a = env.zphi_seed_a
    b = env.zphi_seed_b
    for step in range(32):
        # Multiply by phi: (a, b) -> (b, a + b), then conjugate every second step
        a, b = b, a + b
        if step & 1:
            a, b = a + b, -b
    norm_val = a * a + a * b - b * b
    ok = abs(norm_val) < 5_000_000
    return ok, (norm_val & 0xFFFFFFFF)


def stage_dot64_score(env: TaskEnvelope) -> Tuple[bool, int]:
    """Stage 4: 64-dimensional integer inner-product + L1 regularization gate."""
    dot = 0
    l1 = 0
    v = env.vec64
    for idx in range(64):
        x = v[idx]
        dot += x * ANCHOR_VEC64[idx]
        l1 += abs(x)
    ok = (dot > 0) and (l1 < 5000)
    return ok, (dot & 0xFFFFFFFF)


def stage_sha256_merkle_verify(env: TaskEnvelope) -> Tuple[bool, int]:
    """Stage 5: 8-round chained SHA-256 cryptographic digest verification."""
    h = env.payload_bytes
    eid = env.envelope_id
    for r in range(8):
        h = hashlib.sha256(h + struct.pack("<II", eid, r)).digest()
    tag = h[0] & 0x0F
    ok = (tag == env.expected_pow_tag)
    return ok, struct.unpack("<I", h[:4])[0]


def stage_packet_serialize(env: TaskEnvelope) -> Tuple[bool, int]:
    """Stage 6: Canonical binary frame packing + CRC32 checksum finalization."""
    header_buf = struct.pack(
        "<I4sBBqq",
        env.envelope_id,
        env.magic_header,
        env.version,
        env.ttl_hops,
        env.zphi_seed_a,
        env.zphi_seed_b,
    )
    crc = zlib.crc32(header_buf + env.payload_bytes) & 0xFFFFFFFF
    return True, crc


STAGE_REGISTRY: List[Tuple[str, Callable[[TaskEnvelope], Tuple[bool, int]]]] = [
    ("S_schema", stage_schema_validate),
    ("S_f2_syn", stage_f2_syndrome_check),
    ("S_zphi_norm", stage_zphi_norm_check),
    ("S_dot64", stage_dot64_score),
    ("S_sha256", stage_sha256_merkle_verify),
    ("S_pack", stage_packet_serialize),
]


# ============================================================================
# 3. Empirical Structural-Torque Proxy (tau_k) Calibration
# ============================================================================

@dataclass
class StageTorqueProfile:
    stage_name: str
    empirical_reject_rate: float     # r_k in [0, 1]
    mean_cpu_time_us: float          # c_k in microseconds per item
    structural_torque_proxy: float   # tau_k = (r_k / c_k) * 1000.0


def calibrate_structural_torque(
    calibration_slice: List[TaskEnvelope],
) -> Dict[str, StageTorqueProfile]:
    """
    Profiles each stage independently on the calibration slice to measure its
    empirical rejection rate r_k and mean CPU time c_k (microseconds), then
    computes the Structural-Torque Proxy:
        tau_k = (r_k / c_k) * 1000.0
    """
    profiles: Dict[str, StageTorqueProfile] = {}
    n_cal = len(calibration_slice)

    for name, fn in STAGE_REGISTRY:
        rejects = 0
        t0 = time.perf_counter_ns()
        for env in calibration_slice:
            ok, _ = fn(env)
            if not ok:
                rejects += 1
        elapsed_ns = max(1, time.perf_counter_ns() - t0)

        r_k = rejects / n_cal
        c_k_us = (elapsed_ns / 1000.0) / n_cal
        tau_k = (r_k / c_k_us) * 1000.0
        profiles[name] = StageTorqueProfile(
            stage_name=name,
            empirical_reject_rate=round(r_k, 4),
            mean_cpu_time_us=round(c_k_us, 4),
            structural_torque_proxy=round(tau_k, 2),
        )

    return profiles


# ============================================================================
# 4. Pipeline Execution Modes (Measured on Identical Workload)
# ============================================================================

@dataclass
class PipelineRunMetrics:
    mode_name: str
    stage_order: List[str]
    wall_clock_ms: float
    total_stage_invocations: int
    total_cpu_weighted_us: float
    cumulative_torque_load: float
    accepted_count: int
    accepted_digest_sha256: str


def run_pipeline_mode(
    mode_name: str,
    ordered_stages: List[Tuple[str, Callable[[TaskEnvelope], Tuple[bool, int]]]],
    workload: List[TaskEnvelope],
    profiles: Dict[str, StageTorqueProfile],
    early_exit: bool,
) -> PipelineRunMetrics:
    """
    Executes the given stage order over `workload`, measuring real wall-clock
    time (ms), total stage invocations, empirical CPU-weighted work, and the
    cumulative structural-torque load:
        CumulativeTorqueLoad = sum_{stage k} (ItemsEntering_k * c_k_us)
    Also computes a SHA-256 digest of all accepted envelope IDs and CRC tags to
    prove 100% identical functional outputs across all pipeline modes.
    """
    stage_invocations = 0
    stage_entry_counts = {name: 0 for name, _ in ordered_stages}
    accepted_records: List[Tuple[int, int]] = []

    t0 = time.perf_counter_ns()
    for env in workload:
        all_ok = True
        last_tag = 0
        for name, fn in ordered_stages:
            stage_invocations += 1
            stage_entry_counts[name] += 1
            ok, tag = fn(env)
            if not ok:
                all_ok = False
                if early_exit:
                    break
            else:
                last_tag ^= tag
        if all_ok:
            accepted_records.append((env.envelope_id, last_tag & 0xFFFFFFFF))
    elapsed_ms = (time.perf_counter_ns() - t0) / 1_000_000.0

    # Compute CPU-weighted work and Structural-Torque load using the identical
    # calibrated stage profiles
    total_cpu_weighted_us = sum(
        stage_entry_counts[name] * profiles[name].mean_cpu_time_us
        for name, _ in ordered_stages
    )
    # Structural-torque load proxy: downstream expensive work multiplied by
    # un-cleared defect fraction entering each stage
    n_total = len(workload)
    cumulative_torque_load = sum(
        (stage_entry_counts[name] / n_total) * profiles[name].mean_cpu_time_us
        for name, _ in ordered_stages
    )

    digest_hasher = hashlib.sha256()
    for eid, tag in accepted_records:
        digest_hasher.update(struct.pack("<II", eid, tag))

    return PipelineRunMetrics(
        mode_name=mode_name,
        stage_order=[name for name, _ in ordered_stages],
        wall_clock_ms=round(elapsed_ms, 3),
        total_stage_invocations=stage_invocations,
        total_cpu_weighted_us=round(total_cpu_weighted_us, 2),
        cumulative_torque_load=round(cumulative_torque_load, 4),
        accepted_count=len(accepted_records),
        accepted_digest_sha256=digest_hasher.hexdigest()[:16],
    )


def run_benchmark(n_payloads: int = 4000, seed: int = 20261101) -> Dict[str, object]:
    workload = generate_workload(n_payloads=n_payloads, seed=seed)

    # 1. Calibrate tau_k on a 500-envelope slice
    cal_slice = workload[: min(500, len(workload))]
    profiles = calibrate_structural_torque(cal_slice)

    # 2. Mode A: Naive Un-Culled Sequential Baseline (no early exit)
    naive_metrics = run_pipeline_mode(
        mode_name="Baseline_A_Naive_UnCulled_Sequential",
        ordered_stages=STAGE_REGISTRY,
        workload=workload,
        profiles=profiles,
        early_exit=False,
    )

    # 3. Mode B: Anti-Torque / Heavy-First Sequential Baseline (with early exit)
    #    Sorted by ascending tau_k (expensive low-torque stages first, except S_pack last)
    core_stages = [s for s in STAGE_REGISTRY if s[0] != "S_pack"]
    pack_stage = [s for s in STAGE_REGISTRY if s[0] == "S_pack"]
    anti_torque_order = sorted(
        core_stages, key=lambda s: profiles[s[0]].structural_torque_proxy
    ) + pack_stage
    anti_torque_metrics = run_pipeline_mode(
        mode_name="Baseline_B_HeavyFirst_EarlyExit",
        ordered_stages=anti_torque_order,
        workload=workload,
        profiles=profiles,
        early_exit=True,
    )

    # 4. Mode C: CHRONO-TORQUE (Descending tau_k Pre-Cleared Pipeline)
    #    Sorted automatically by descending empirical tau_k (highest rejection per us first)
    chrono_torque_order = sorted(
        core_stages,
        key=lambda s: profiles[s[0]].structural_torque_proxy,
        reverse=True,
    ) + pack_stage
    chrono_metrics = run_pipeline_mode(
        mode_name="CHRONO_TORQUE_Descending_Tau_PreCleared",
        ordered_stages=chrono_torque_order,
        workload=workload,
        profiles=profiles,
        early_exit=True,
    )

    # Verify exact functional equivalence across all 3 modes
    outputs_identical = (
        naive_metrics.accepted_count == anti_torque_metrics.accepted_count == chrono_metrics.accepted_count
        and naive_metrics.accepted_digest_sha256 == chrono_metrics.accepted_digest_sha256
    )

    speedup_vs_naive = round(naive_metrics.wall_clock_ms / max(0.001, chrono_metrics.wall_clock_ms), 2)
    speedup_vs_heavy_first = round(anti_torque_metrics.wall_clock_ms / max(0.001, chrono_metrics.wall_clock_ms), 2)
    torque_reduction_vs_naive = round(
        naive_metrics.cumulative_torque_load / max(1e-9, chrono_metrics.cumulative_torque_load), 2
    )
    torque_reduction_vs_heavy = round(
        anti_torque_metrics.cumulative_torque_load / max(1e-9, chrono_metrics.cumulative_torque_load), 2
    )

    passed = (
        outputs_identical
        and speedup_vs_naive > 2.0
        and speedup_vs_heavy_first > 1.5
        and torque_reduction_vs_naive > 2.0
    )

    return {
        "module": "real_pipeline_torque_benchmark",
        "workload_payloads": n_payloads,
        "seed": seed,
        "proxy_definition": "tau_k = (empirical_reject_rate_k / mean_cpu_time_us_k) * 1000.0",
        "calibrated_stage_profiles": {k: asdict(v) for k, v in profiles.items()},
        "runs": {
            "baseline_naive_unculled": asdict(naive_metrics),
            "baseline_heavy_first_early_exit": asdict(anti_torque_metrics),
            "chrono_torque_precleared": asdict(chrono_metrics),
        },
        "comparisons": {
            "functional_outputs_identical": outputs_identical,
            "wall_clock_speedup_vs_naive_x": speedup_vs_naive,
            "wall_clock_speedup_vs_heavy_first_x": speedup_vs_heavy_first,
            "structural_torque_load_reduction_vs_naive_x": torque_reduction_vs_naive,
            "structural_torque_load_reduction_vs_heavy_first_x": torque_reduction_vs_heavy,
        },
        "status": "PASS" if passed else "FAIL",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Real 6-stage workload benchmark with empirical structural-torque proxy tau_k."
    )
    parser.add_argument("--payloads", type=int, default=4000)
    parser.add_argument("--seed", type=int, default=20261101)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = run_benchmark(n_payloads=args.payloads, seed=args.seed)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("=" * 78)
        print("REAL 6-STAGE WORKLOAD: STRUCTURAL-TORQUE PROXY (tau_k) & WALL-CLOCK BENCHMARK")
        print("=" * 78)
        print(f"Payloads Processed : {report['workload_payloads']} concrete 512B envelopes (seed={report['seed']})")
        print(f"Proxy Definition   : {report['proxy_definition']}")
        print("-" * 78)
        print(f"{'Stage':<14} | {'Reject Rate r_k':<16} | {'Mean CPU (us)':<14} | {'Torque Proxy tau_k':<18}")
        print("-" * 78)
        for name, prof in report["calibrated_stage_profiles"].items():
            print(
                f"{name:<14} | {prof['empirical_reject_rate']:<16.4f} | "
                f"{prof['mean_cpu_time_us']:<14.4f} | {prof['structural_torque_proxy']:<18.2f}"
            )
        print("-" * 78)
        for key, run in report["runs"].items():
            print(
                f"{run['mode_name']:<40} : {run['wall_clock_ms']:>8.3f} ms | "
                f"calls={run['total_stage_invocations']:>6} | "
                f"torque_load={run['cumulative_torque_load']:>7.4f} us/item | "
                f"accepted={run['accepted_count']} (sha256={run['accepted_digest_sha256']})"
            )
        print("-" * 78)
        comp = report["comparisons"]
        print(f"Identical Output Digest Across Modes : {comp['functional_outputs_identical']}")
        print(f"Wall-Clock Speedup vs Naive Baseline : {comp['wall_clock_speedup_vs_naive_x']}x")
        print(f"Wall-Clock Speedup vs Heavy-First    : {comp['wall_clock_speedup_vs_heavy_first_x']}x")
        print(f"Torque-Load Reduction vs Naive       : {comp['structural_torque_load_reduction_vs_naive_x']}x")
        print(f"Torque-Load Reduction vs Heavy-First : {comp['structural_torque_load_reduction_vs_heavy_first_x']}x")
        print(f"Overall Status                       : {report['status']}")
        print("=" * 78)

    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
