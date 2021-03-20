from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration


class CppTemplateConan(ConanFile):
    name = "CppTemplate"
    version = "0.0.1"
    license = "MIT Licence"
    author = "Bertouz la tarlouze"
    url = "https://github.com/Bertouz/CppTemplate"
    description = "It is a C++ template project, I want to include all my default config for clang tools, conan, etc..."
    topics = ("template", "c++")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake_find_package"
    requires="catch2/3.0.0@catchorg/stable"

    def configure(self):
        if self.settings.compiler.cppstd not in ["11", "14","17"]:
            raise ConanInvalidConfiguration("C++ standard less than 11 not handled ")

    def source(self):
        self.run("".join(["git clone ",self.url]))

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]

