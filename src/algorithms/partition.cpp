#include <string>
#include <algorithm>
#include <iostream>

#include "../utilities.hpp"
#include "../call_defines.hpp"

utilities::timer timer;
utilities::random_vector_generator gen;

auto pred = [](double num)
{ return ((int)num % 4) < 2; };

double test(std::vector<std::string> args)
{
	int vector_size = stoi(args[0]);
	BENCH_INIT(args);

	auto vec1 = gen.get_doubles(vector_size);
	decltype(vec1) vec2(vec1.size());

	timer.start();
	BENCH_CALL(partition, vec1.begin(), vec1.end(), vec2.begin(), pred);
	timer.stop();

	// use result otherwise compiler will optimize it away:
	if (std::count(vec2.begin(), vec2.end(), 42.0))
	{
		std::cerr << "err42";
	}

	return timer.get();
}

#include "../main.cpp"
