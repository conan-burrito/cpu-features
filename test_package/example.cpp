#include <cpu_features/cpu_features_macros.h>
#if defined(CPU_FEATURES_OS_ANDROID)
#include <cpu-features.h>
#elif defined(CPU_FEATURES_ARCH_X86)
#include <cpu_features/cpuinfo_x86.h>
#elif defined(CPU_FEATURES_ARCH_ARM)
#include <cpu_features/cpuinfo_arm.h>
#elif defined(CPU_FEATURES_ARCH_AARCH64)
#include <cpu_features/cpuinfo_aarch64.h>
#elif defined(CPU_FEATURES_ARCH_MIPS)
#include <cpu_features/cpuinfo_mips.h>
#elif defined(CPU_FEATURES_ARCH_PPC)
#include <cpu_features/ccpuinfo_ppc.h>
#endif

#include <stdlib.h>
#include <stdio.h>

#if !defined(CPU_FEATURES_OS_ANDROID)
using namespace cpu_features;
#endif

// use has_fast_avx.
int main() {
#if defined(CPU_FEATURES_OS_ANDROID)
    uint64_t features = android_getCpuFeatures();
#elif defined(CPU_FEATURES_ARCH_X86)
    X86Features features = GetX86Info().features;
#elif defined(CPU_FEATURES_ARCH_ARM)
    ArmFeatures features = GetArmInfo().features;
#elif defined(CPU_FEATURES_ARCH_AARCH64)
    Aarch64Features features = GetAarch64Info().features;
#elif defined(CPU_FEATURES_ARCH_MIPS)
    MipsFeatures features = GetMipsInfo().features;
#elif defined(CPU_FEATURES_ARCH_PPC)
    PPCFeatures features = GetPPCInfo().features;
#endif

#if defined(CPU_FEATURES_OS_ANDROID)
    printf("NEON is%s available\n", (features & ANDROID_CPU_ARM_FEATURE_NEON) ? "" : "n't");
#elif defined(CPU_FEATURES_ARCH_X86) || defined(CPU_FEATURES_ARCH_ARM) || defined(CPU_FEATURES_ARCH_AARCH64)
    printf("AES is%s available\n", features.aes ? "" : "n't");
#elif defined(CPU_FEATURES_ARCH_MIPS)
    printf("EVA is%s available\n", features.eva ? "" : "n't");
#elif defined(CPU_FEATURES_ARCH_PPC)
    printf("SPE is%s available\n", features.spe ? "" : "n't");
#endif

   return EXIT_SUCCESS;
}
