find_program(CLANG_TIDY_EXECUTABLE clang-tidy REQUIRED)
if(CLANG_TIDY_EXECUTABLE)
    message(STATUS "Found clang-tidy = ${CLANG_TIDY_EXECUTABLE}")
endif(CLANG_TIDY_EXECUTABLE)
