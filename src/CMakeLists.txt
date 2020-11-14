message(STATUS "Building MyCppProject")

list(APPEND CMAKE_MESSAGE_INDENT "  ")

target_sources(MyCppProject PRIVATE hello.cpp)

target_include_directories(MyCppProject PUBLIC
                       $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}> # for headers when building
                       $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

set_target_properties(MyCppProject
    PROPERTIES
    PUBLIC_HEADER "src/hello.hpp"
)

list(POP_BACK CMAKE_MESSAGE_INDENT)
