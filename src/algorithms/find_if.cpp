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
    // In a uniform random distribution vector of size n (k is an integer):
    // P(any element = k) = 1 - P(all elements != k)
    // = 1 - q^n
    // where q = P(single element != k)
    // For a uniform distr in range [1, x], q = 1 - 1/x
    // Thus, we select x so that
    // P(find) = P(any element = k) = 1-q^n = whatever we need

    auto vec1 = gen.get_ints(vector_size, 0, vector_size);
    auto pred = [vector_size](auto num)
    { return ((int)std::pow(num, 1.2) % (vector_size)) == 0; };

    // auto vec1 = gen.get_ints(vector_size, 0, 4);
    // std::vector<int> vec1(vector_size, 0);

    timer.start();
    auto result = BENCH_CALL(find_if, vec1.begin(), vec1.end(), pred);
    timer.stop();

    // use result otherwise compiler will optimize it away:
    if (std::distance(vec1.begin(), result) == 42)
    {
        std::cerr << "err42";
    }

    // if (result != vec1.end())
    // {
    //     auto distance = std::distance(vec1.begin(), result);
    //     std::cout << "Found in chunck: " << distance / (vector_size / 80) << "\n";
    // }

    return timer.get();
}

#include "../main.cpp"
