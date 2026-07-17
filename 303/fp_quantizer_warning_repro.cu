#include <cstdint>
#include <cuda_fp16.h>

// Minimal extraction from codebase/csrc/fp_quantizer/fp_quantize_impl.cu.
// The expressions below mirror the warning-triggering template instantiations
// reported in bug 7971.

template <typename T, int unroll, int _mantisa_bits, int _exponent_bits, int total_q_bits = 8,
          int q_mantisa_bits = 3, int stochastic_rounding = 0>
__global__ void apply_quantization_warning()
{
    constexpr uint32_t _sign_mask = 1 << (_mantisa_bits + _exponent_bits);
    int mantisa_mask = ((1 << q_mantisa_bits) - 1);
    mantisa_mask <<= (_mantisa_bits - q_mantisa_bits);
    (void)_sign_mask;
    (void)mantisa_mask;
}

template <typename T, int q_mantisa_bits, int total_q_bits = 16, int _mantisa_bits = 3,
          int _exponent_bits = 4>
__global__ void apply_selective_dequantization_warning()
{
    constexpr uint32_t _sign_mask = 1 << (_mantisa_bits + _exponent_bits);
    int mantisa_mask = ((1 << q_mantisa_bits) - 1);
    mantisa_mask <<= (_mantisa_bits - q_mantisa_bits);
    (void)_sign_mask;
    (void)mantisa_mask;
}

template __global__ void apply_quantization_warning<__half, 5, 23, 8, 4, 1, 1>();
template __global__ void apply_selective_dequantization_warning<__half, 10, 16, 3, 4>();

