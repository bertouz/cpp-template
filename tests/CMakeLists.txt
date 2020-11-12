message(STATUS "Building Tests")
list(APPEND CMAKE_MESSAGE_INDENT "  ")

# Creating target for all unit tests
# I prefer to have one big executable with a filter parameter
add_executable(testu
    main_testu.cpp
    )

target_link_libraries(testu PRIVATE Catch2::Catch2)

# We set the output directory of the target even though in this example it is not necessary
# It's just that if we want to build other test target or if we move this one, we will still have the target in this directory
set_target_properties(testu
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_BINDIR}/tests"
)

# Add the target to the list of ctest's tests
add_test(testu testu)

list(POP_BACK CMAKE_MESSAGE_INDENT)

