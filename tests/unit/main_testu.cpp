#define CATCH_CONFIG_RUNNER
#include "hello.hpp"
#include <catch2/catch_session.hpp>

int main(int argc, char *argv[])
{
    const int res = Catch::Session().run(argc, argv);
    my_cpp_project::PolitePerson person;
    person.hello();
    return res;
}
