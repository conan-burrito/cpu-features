from conans import tools, ConanFile, CMake
import os


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


    @property
    def _source_subfolder(self):
        return "src"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        # It's a C project - remove irrelevant settings
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        archive_name = "cpu_features-{0}".format(self.version)
        os.rename(archive_name, self._source_subfolder)

        for patch in self.conan_data.get("patches", {}).get(self.version, []):
            tools.patch(**patch)

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_subfolder)
        cmake.definitions['BUILD_PIC'] = 'ON' if self.options.fPIC else 'OFF'

        cmake.build()
        cmake.install()

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        self.cpp_info.libs = ['cpu_features']
        if self.settings.os == 'Android':
            self.cpp_info.libs.append('ndk_compat')

        self.cpp_info.includedirs = ['include', os.path.join('include', 'ndk_compat')]
