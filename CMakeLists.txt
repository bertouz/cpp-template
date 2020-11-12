cmake_minimum_required(VERSION 3.14)

project(MyCppProject
    VERSION 0.0.1
    LANGUAGES CXX
    )

#############################
### CMake config
#############################

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)
include(${CMAKE_SOURCE_DIR}/cmake/mycppproject-macro.cmake)
if (CMAKE_BINARY_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR)
    message(FATAL_ERROR "Building in-source is not supported! Create a build dir and remove ${CMAKE_SOURCE_DIR}/CMakeCache.txt")
endif()

#############################
### Project Options
#############################
option(BUILD_DOC "Build documentation" OFF)
option(BUILD_TESTS "Build unit testing" ON)
option(USE_SUBMODULE_Catch2 "Use submodule Catch2" ON)

#############################
### Dependencies
#############################
if(BUILD_DOC)
        find_package(Doxygen REQUIRED)
endif(BUILD_DOC)

# I prefer to look for all the dependecies at the start
# to avoid a user to look for different find_package in dedicated subdirectory
# Also if possible I add the possibility to use external dependencies in submodules to simplify a first use
if(BUILD_TESTS)
    add_submodule_dep(Catch2)
endif(BUILD_TESTS)


#############################
### MyCppProject
#############################
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
    install( DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/doc/doc/" DESTINATION "${CMAKE_INSTALL_DOCDIR}" )
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
