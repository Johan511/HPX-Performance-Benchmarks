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

    // by trial and error, the heuristic below seems to give ~70% of actually finding
    // the succession {1, 1} in vec1
    auto vec1 = gen.get_ints(vector_size, 0, std::max(1.0, std::sqrt(vector_size)));
    // auto vec1 = gen.get_ints(vector_size, 0, std::max(1.0, std::sqrt(vector_size) / 100.0));

    std::vector<int> vec2{0, 0};

    timer.start();
    auto result = BENCH_CALL(search, vec1.begin(), vec1.end(), vec2.begin(), vec2.end());
    timer.stop();

    // use result otherwise compiler will optimize it away:
    if (std::distance(vec1.begin(), result) == 42)
    {
        std::cerr << "err42";
    }

    // if (result != vec1.end())
    // {
    //     std::cout << "YES ";
    // }

    return timer.get();
}

#include "../main.cpp"
