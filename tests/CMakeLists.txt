message(STATUS "Building Tests")
list(APPEND CMAKE_MESSAGE_INDENT "  ")
add_subdirectory(unit)
list(POP_BACK CMAKE_MESSAGE_INDENT)

