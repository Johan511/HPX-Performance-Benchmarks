#include <string>
#include <algorithm>
#include <iostream>

#include "../utilities.hpp"
#include "../call_defines.hpp"

utilities::timer timer;
utilities::random_vector_generator gen;

double test(std::vector<std::string> args)
{
    int vector_size = std::stoi(args[0]);
    BENCH_INIT(args);

    auto vec1 = gen.get_doubles(vector_size);

    timer.start();
    BENCH_CALL(sort, vec1.begin(), vec1.end());
    timer.stop();

    // use result otherwise compiler will optimize it away:
    if (std::count(vec1.begin(), vec1.end(), 42.0))
    {
        std::cerr << "err42";
    }

    return timer.get();
}

#include "../main.cpp"
