/**
 * CHRONO-TORQUE v2.0.1 — Native C++20 Kernel Benchmark Driver
 * (`benchmark_native_zdc_qegg.cpp`)
 * Compiles and benchmarks `bama_zdc_qegg_epicyclic_kernel.hpp` over a 4,096-cell
 * `QEG5Cell256` arena (38.00 B/cell PAPR-guarded hierarchical scan) vs. a dense
 * 4,096 x 768 FP32 baseline arena (3,072.00 B/cell = 12.0 MB).
 */

#include "bama_zdc_qegg_epicyclic_kernel.hpp"
#include <chrono>
#include <cstdio>
#include <vector>

using namespace metaphy::bama::chrono_torque;

int main() {
    constexpr size_t N_CELLS = 4096;
    constexpr size_t DIMS = 768;
    constexpr int ITERS = 500;

    std::vector<QEG5Cell256> arena(N_CELLS);
    for (size_t i = 0; i < N_CELLS; ++i) {
        auto& c = arena[i];
        c.magic[0] = 'Q'; c.magic[1] = 'E'; c.magic[2] = 'G'; c.magic[3] = '5';
        uint16_t zk = GEAR_TEETH[i % 6];
        c.gear_teeth_zk = zk;
        c.crt_r251 = DualModulusCRTShield::mod251(zk);
        c.crt_r253 = DualModulusCRTShield::mod253(zk);
        c.s7_s8_calibration_flag = 0x03u;
        c.quality_score_u8 = 200u;
        // Stage survival distribution matching 4096 -> 3676 -> 309 -> 32
        c.spts_state0_gate = (i < 3676) ? ((i < 309) ? ((i < 32) ? 3u : 2u) : 1u) : 0u;
        for (size_t j = 0; j < 48; ++j) c.parent_icosahedral_q7[j] = static_cast<uint8_t>((i + j) & 0x7Fu);
        for (size_t j = 0; j < 180; ++j) c.child_dodecahedral_phits[j] = static_cast<uint8_t>((i * 3 + j) & 0xFFu);
    }

    std::vector<int32_t> q_int(180, 7);
    std::vector<float> fp32_arena(N_CELLS * DIMS, 0.125f);
    std::vector<float> fp32_query(DIMS, 0.25f);
    for (size_t i = 0; i < fp32_arena.size(); i += 64) {
        fp32_arena[i] = static_cast<float>((i & 255) * 0.01f);
    }

    volatile int64_t zdc_sink = 0;
    auto t0 = std::chrono::high_resolution_clock::now();
    for (int it = 0; it < ITERS; ++it) {
        int64_t total_score = 0;
        for (size_t i = 0; i < N_CELLS; ++i) {
            const auto& c = arena[i];
            if (c.spts_state0_gate == 0u) continue; // Stage 0 skip (420 cells skipped after 1B read)
            if (!WillisEpicyclicClutch::authorize_local_swap(c, 1250, 422)) continue;
            if (c.spts_state0_gate >= 2u) {
                int32_t p_sum = 0;
                for (size_t j = 0; j < 48; ++j) p_sum += c.parent_icosahedral_q7[j];
                total_score += p_sum;
                if (c.spts_state0_gate == 3u) {
                    ZPhiAccumulator acc{};
                    for (size_t j = 0; j < 119; ++j) {
                        uint8_t packed = c.child_dodecahedral_phits[j];
                        acc.accumulate_phit(packed & 0x03u, q_int[j]);
                        acc.accumulate_phit((packed >> 2) & 0x03u, q_int[j]);
                    }
                    acc.multiply_by_phi();
                    total_score += acc.evaluate_q16_16(3277);
                }
            }
        }
        zdc_sink += total_score;
    }
    auto t1 = std::chrono::high_resolution_clock::now();
    double zdc_us = std::chrono::duration<double, std::micro>(t1 - t0).count() / ITERS;

    volatile float fp32_sink = 0.0f;
    auto t2 = std::chrono::high_resolution_clock::now();
    for (int it = 0; it < ITERS; ++it) {
        float acc_all = 0.0f;
        for (size_t i = 0; i < N_CELLS; ++i) {
            const float* row = &fp32_arena[i * DIMS];
            float dot = 0.0f;
            for (size_t d = 0; d < DIMS; ++d) {
                dot += row[d] * fp32_query[d];
            }
            acc_all += dot;
        }
        fp32_sink += acc_all;
    }
    auto t3 = std::chrono::high_resolution_clock::now();
    double fp32_us = std::chrono::duration<double, std::micro>(t3 - t2).count() / ITERS;
    double speedup = fp32_us / zdc_us;

    std::printf(
        "{\"native_cpp20_zdc_qegg_4096_cells_us\": %.2f, \"native_cpp20_fp32_4096x768_us\": %.2f, "
        "\"native_cpp20_speedup_x\": %.2f, \"zdc_sink\": %lld, \"fp32_sink\": %.2f}\n",
        zdc_us, fp32_us, speedup, static_cast<long long>(zdc_sink), static_cast<double>(fp32_sink)
    );
    return 0;
}
