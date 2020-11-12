message(STATUS "Building MyCppProject")

list(APPEND CMAKE_MESSAGE_INDENT "  ")

add_library(MyCppProject
    hello.cpp
    )

target_include_directories(MyCppProject PUBLIC
                       $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}> # for headers when building
                       $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

set_target_properties(MyCppProject
    PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_BINDIR}"
    ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR}"
    PUBLIC_HEADER "src/hello.hpp"
)

list(POP_BACK CMAKE_MESSAGE_INDENT)
