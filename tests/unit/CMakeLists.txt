message(STATUS "Building Unit Tests")
list(APPEND CMAKE_MESSAGE_INDENT " ")

# Creating target for all unit tests
# I prefer to have one big executable with a filter parameter

add_executable(testu
    main_testu.cpp
    hello-test.cpp
    )

target_link_libraries(testu PRIVATE Catch2::Catch2 MyCppProject)

# Add the target to the list of ctest's tests
add_test(testu testu)

list(POP_BACK CMAKE_MESSAGE_INDENT)

