from   conans       import ConanFile, CMake, tools
from   conans.tools import download, unzip
import os

class RttrConan(ConanFile):
    name            = "rttr"
    version         = "b3a131c"     
    description     = "Conan package for rttr."           
    url             = "https://github.com/rttrorg/rttr"
    license         = "MIT"                                         
    settings        = "arch", "build_type", "compiler", "os"
    generators      = "cmake"
    options         = {"shared": [True, False], 
                       "build_unit_tests": [True, False],
                       "build_with_static_runtime_libs": [True, False],
                       "build_with_rtti": [True, False],
                       "build_benchmarks": [True, False],
                       "build_examples": [True, False],
                       "build_documentation": [True, False],
                       "build_installer": [True, False],
                       "build_package": [True, False],
                       "use_pch": [True, False],
                       "custom_doxygen_style": [True, False],
                       "build_website_docu": [True, False]} 
    default_options = "shared=True", "build_unit_tests=False", "build_with_static_runtime_libs=False", "build_with_rtti=True", "build_benchmarks=False", "build_examples=False", "build_documentation=False", "build_installer=True", "build_package=True", "use_pch=True", "custom_doxygen_style=True", "build_website_docu=False"

    def source(self):
        project_folder = "%s-%s" % (self.name, self.version)
        zip_name = "v%s.zip" % self.version
        download ("%s/archive/%s" % (self.url, zip_name), zip_name, verify=True)
        unzip    (zip_name)
        os.unlink(zip_name)

        tools.replace_in_file("rttr/CMakeLists.txt", '''project ("rttr" LANGUAGES CXX)''',
                              '''project ("rttr" LANGUAGES CXX)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)

        cmake.definitions["BUILD_STATIC"] = not self.options.shared
        cmake.definitions["BUILD_RTTR_DYNAMIC"] = self.options.shared
        cmake.definitions["BUILD_UNIT_TESTS"] = self.options.build_unit_tests
        cmake.definitions["BUILD_WITH_STATIC_RUNTIME_LIBS"] = self.options.build_with_static_runtime_libs
        cmake.definitions["BUILD_WITH_RTTI"] = self.options.build_with_rtti
        cmake.definitions["BUILD_BENCHMARKS"] = self.options.build_benchmarks
        cmake.definitions["BUILD_EXAMPLES"] = self.options.build_examples
        cmake.definitions["BUILD_DOCUMENTATION"] = self.options.build_documentation
        cmake.definitions["BUILD_INSTALLER"] = self.options.build_installer
        cmake.definitions["BUILD_PACKAGE"] = self.options.build_package
        cmake.definitions["USE_PCH"] = self.options.use_pch
        cmake.definitions["CUSTOM_DOXYGEN_STYLE"] = self.options.custom_doxygen_style
        cmake.definitions["BUILD_WEBSITE_DOCU"] = self.options.build_website_docu

        project_folder = "%s-%s" % (self.name, self.version)

        cmake.configure( source_folder="%s" % (project_folder))
        cmake.build()

    def package(self):
        project_folder = "%s-%s" % (self.name, self.version)
        include_folder = "%s/src/rttr" % (project_folder)
        self.copy("*.h"  , dst="include/rttr", src=include_folder)
        self.copy("registration", dst="include/rttr", src=include_folder)
        self.copy("type", dst="include/rttr", src=include_folder)
        self.copy("*.h", dst="include/rttr", src="src/rttr")
        self.copy("*.a"  , dst="lib", keep_path=False)
        self.copy("*.so*" , dst="lib", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libdirs = ["lib", "bin"]
        self.cpp_info.libs = tools.collect_libs(self)

        if self.settings.os == "Linux":
            self.cpp_info.libs += ["dl"]
