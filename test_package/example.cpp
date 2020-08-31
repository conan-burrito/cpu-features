#include <iostream>
#include <cpu_features/cpu_features_macros.h>

#ifdef CPU_FEATURES_OS_ANDROID
   #include <cpu-features.h>

   static const uint64_t features = android_getCpuFeatures();
   static const bool has_neon = (features & ANDROID_CPU_ARM_FEATURE_NEON) == ANDROID_CPU_ARM_FEATURE_NEON;
   static const bool has_feature = has_neon;
#else
   #include <cpu_features/cpuinfo_x86.h>
   using namespace cpu_features;

   static const X86Info info = GetX86Info();
   static const X86Microarchitecture uarch = GetX86Microarchitecture(&info);
   static const bool has_fast_avx = info.features.avx && uarch != INTEL_SNB;
   static const bool has_feature = has_fast_avx;
#endif


// use has_fast_avx.
int main() {
   std::cout << "Feature: " << has_feature << std::endl;
   return 0;
}
