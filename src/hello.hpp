#ifndef HELLO_HPP
#define HELLO_HPP
#include <iostream>

namespace MyCppProject
{
    /**
     * @brief greet - Function that append to a given stream the message "hello world"
     * @param pOs - stream in which we want to greet
     */
    void greet(std::ostream& pOs);
}

#endif // HELLO_HPP
