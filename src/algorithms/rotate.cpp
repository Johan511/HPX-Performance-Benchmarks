#include <string>
#include <algorithm>
#include <iostream>

#include "../utilities.hpp"
#include "../call_defines.hpp"

utilities::timer timer;
utilities::random_vector_generator gen;

auto unary_op = [](double num)
{ return ((int)num % 4) < 2; };

double test(std::vector<std::string> args)
{
	int vector_size = stoi(args[0]);
	BENCH_INIT(args);

	auto vec1 = gen.get_doubles(vector_size);
	std::vector<int> vec2(vec1.size());

	// Choose a random point to rotate to
	int k = gen.get_ints(1, 0, vector_size - 1)[0];

	timer.start();
	BENCH_CALL(rotate, vec1.begin(), vec1.begin() + k, vec2.begin());
	timer.stop();

	// use result otherwise compiler will optimize it away:
	if (std::count(vec2.begin(), vec2.end(), 42))
	{
		std::cerr << "err42";
	}

	return timer.get();
}

#include "../main.cpp"
