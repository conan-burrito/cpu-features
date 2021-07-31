from conans import tools, ConanFile, CMake
from conans.errors import ConanInvalidConfiguration
import os


# Adapted from the conan center index: https://github.com/conan-io/conan-center-index/tree/master/recipes/cpu_features
class Recipe(ConanFile):
    name = 'cpu-features'
    description = 'A cross-platform C library to retrieve CPU features (such as available instructions) at runtime.'
    url = 'https://github.com/conan-burrito/cpu-features'
    homepage = "https://github.com/google/cpu_features"
    license = "Apache License 2.0"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = 'cmake'
    build_policy = 'missing'
    exports_sources = "patches/**"
    _cmake = None

    @property
    def _source_subfolder(self):
        return "src"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.settings.os == "Emscripten":
            raise ConanInvalidConfiguration("cpu-features does not support emscripten")

        if self.options.shared:
            del self.options.fPIC

        # It's a C project - remove irrelevant settings
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        tools.get(**self.conan_data["sources"][self.version],
                  strip_root=True, destination=self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake

        is_pic = self.options.get_safe("fPIC", False)
        self.output.info('PIC: %s' % is_pic)

        self._cmake = CMake(self)
        self._cmake.definitions["BUILD_PIC"] = 'ON' if is_pic else 'OFF'

        # TODO: should be handled by CMake helper
        if tools.is_apple_os(self.settings.os) and self.settings.arch in ["armv8", "armv8_32", "armv8.3"]:
            self._cmake.definitions["CMAKE_SYSTEM_PROCESSOR"] = "aarch64"

        self._cmake.configure(source_folder=self._source_subfolder) # Does not support out of source builds
        return self._cmake

    def build(self):
        for patch in self.conan_data.get("patches", {}).get(self.version, []):
            tools.patch(**patch)

        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        if self.settings.os == "Linux":
            self.cpp_info.libs.append('dl')

        self.cpp_info.libs = ['cpu_features']
        if self.settings.os == 'Android':
            self.cpp_info.libs.append('ndk_compat')
            self.cpp_info.includedirs = ['include', os.path.join('include', 'ndk_compat')]

        bin_path = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable: {}".format(bin_path))
        self.env_info.PATH.append(bin_path)
