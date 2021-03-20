cmake_minimum_required(VERSION 3.14)

project(MyCppProject
    VERSION 0.0.1
    LANGUAGES CXX
    )

## When we do conan install we download and/or build the dependencies
## Then a conanbuildinfo.cmake file is generated with the variables defining the targets
## to those dependencies
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

#############################
### Project Options
#############################
include(CMakeDependentOption)

option(BUILD_DOC "Build documentation" OFF) 
option(BUILD_TESTS "Build unit testing" ON)
option(USE_CONAN "Define if we want to use conan for handling dependencies if its available" ON)
option(ENABLE_CODE_COVERAGE "Add gcov/lcov analysis to process" OFF)
option(ENABLE_CLANG_TIDY "Add clang-tidy analysis to source code" ON)
option(ENABLE_CLANG_FORMAT "Add clang-format to build process" ON)


####################################
### Include cmake scripts and config
####################################
if(CONAN_CMAKE_CXX_STANDARD)
	set(CMAKE_CXX_STANDARD ${CONAN_CMAKE_CXX_STANDARD})
else()
	set(CMAKE_CXX_STANDARD 14)
endif()

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake/)

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)
include(FindPackageHandleStandardArgs)


if(ENABLE_CLANG_TIDY)
    message(STATUS "Enabling code static analysis with clang-tidy")
    list(APPEND CMAKE_MESSAGE_INDENT "  ")
    include(UseClangTidy)
    list(POP_BACK CMAKE_MESSAGE_INDENT)
endif(ENABLE_CLANG_TIDY)

if(ENABLE_CLANG_FORMAT)
    list(APPEND CMAKE_MESSAGE_INDENT "  ")
    message(STATUS "Enabling code formatting with clang-format")
    include(UseClangFormat)
    list(POP_BACK CMAKE_MESSAGE_INDENT)
endif(ENABLE_CLANG_FORMAT)

if(ENABLE_CODE_COVERAGE)
    message(STATUS "Enabling code coverage with gcov")
    list(APPEND CMAKE_MESSAGE_INDENT "  ")
    include(UseCodeCoverage)
    append_coverage_compiler_flags()
    setup_target_for_coverage_gcovr_html(
        NAME coverage
        EXECUTABLE ctest
        DEPENCIES testu
        EXCLUDE tests
        )
    list(POP_BACK CMAKE_MESSAGE_INDENT )
endif(ENABLE_CODE_COVERAGE)

if (CMAKE_BINARY_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR)
    message(FATAL_ERROR "Building in-source is not supported! Create a build dir and remove ${CMAKE_SOURCE_DIR}/CMakeCache.txt")
endif()



#############################
### Dependencies
#############################
# I prefer to look for all the dependecies at the start
# to avoid a user to look for different find_package in dedicated subdirectory
# Also if possible I add the possibility to use external dependencies in submodules to simplify a first use

if(BUILD_DOC)
	find_package(Doxygen REQUIRED)
	#find_package(Sphinx REQUIRED)
	find_program(SPHINX_EXECUTABLE NAMES sphinx-build DOC "Path to sphinx-build executable")
	find_package_handle_standard_args(Sphinx "Failed to find sphinx-build executable" SPHINX_EXECUTABLE)
endif(BUILD_DOC)

if(BUILD_TESTS)
	find_package(Catch2 REQUIRED)
endif(BUILD_TESTS)

#############################
### MyCppProject
#############################
add_library(MyCppProject SHARED "" )
add_subdirectory(src)


#############################
### Tests
#############################
if(BUILD_TESTS)
    include(CTest)
    add_subdirectory(tests)
endif(BUILD_TESTS)

#############################
### Documentation
#############################
if(BUILD_DOC)
   add_subdirectory(doc)
endif(BUILD_DOC)

#############################
### Installation
#############################

# Install documentation
if(BUILD_DOC)
    install( DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/doc/doxygen" DESTINATION "${CMAKE_INSTALL_DOCDIR}" )
endif(BUILD_DOC)

# Configuration
set(config_install_dir "${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}")
set(generated_dir "${CMAKE_CURRENT_BINARY_DIR}/generated")
set(version_config "${generated_dir}/${PROJECT_NAME}ConfigVersion.cmake")
set(project_config "${generated_dir}/${PROJECT_NAME}Config.cmake")
set(TARGETS_EXPORT_NAME "${PROJECT_NAME}Targets")
set(namespace "${PROJECT_NAME}::")

# Write the version config file
write_basic_package_version_file( "${version_config}" COMPATIBILITY SameMajorVersion )

# Write package config file
configure_package_config_file(
    "cmake/MyCppProjectConfig.cmake.in"
    "${project_config}"
    INSTALL_DESTINATION "${config_install_dir}"
)

# Install targets
install(
    TARGETS MyCppProject #plus others if there is
    EXPORT "${TARGETS_EXPORT_NAME}"
    LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}/${PROJECT_NAME}"
    ARCHIVE DESTINATION "${CMAKE_INSTALL_LIBDIR}/${PROJECT_NAME}"
    RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}"
    PUBLIC_HEADER DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_NAME}"
)

#Install version config file
install( FILES "${project_config}" "${version_config}" DESTINATION "${config_install_dir}" )

#Install config file for exported targets
install( EXPORT "${TARGETS_EXPORT_NAME}" NAMESPACE "${namespace}" DESTINATION "${config_install_dir}" )

#Install includes 
install(DIRECTORY ${CMAKE_SOURCE_DIR}/src/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_NAME} FILES_MATCHING PATTERN *.h*)
