import os
from conans import ConanFile, CMake, tools

class Recipe(ConanFile):
    settings = 'os', 'arch', 'compiler', 'build_type'
    generators = 'cmake'

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if "x86" in self.settings.arch and not tools.cross_building(self.settings):
            self.run(os.path.join("bin", "example"), run_environment=True)
