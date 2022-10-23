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

    auto vec1 = gen.get_ints(vector_size, 0, vector_size / 4);

    timer.start();
    auto result = BENCH_CALL(find, vec1.begin(), vec1.end(), 2);
    timer.stop();

    // use result otherwise compiler will optimize it away:
    if (std::distance(vec1.begin(), result) == 42)
    {
        std::cerr << "err42";
    }

    return timer.get();
}

#include "../main.cpp"
