message(STATUS "Building MyCppProject")

list(APPEND CMAKE_MESSAGE_INDENT "  ")

target_sources(MyCppProject PRIVATE hello.cpp)


list(POP_BACK CMAKE_MESSAGE_INDENT)
