#include <string>
#include <algorithm>
#include <iostream>

#include "../utilities.hpp"
#include "../call_defines.hpp"

utilities::timer timer;
utilities::random_vector_generator gen;

auto unary_op = [](double &num)
{ num += (10.32 * num) / 2.0; };

double test(std::vector<std::string> args)
{
	int vector_size = stoi(args[0]);
	BENCH_INIT(args);

	auto vec1 = gen.get_doubles(vector_size);

	timer.start();
	BENCH_CALL(for_each, vec1.begin(), vec1.end(), unary_op);
	timer.stop();

	// use result otherwise compiler will optimize it away:
	if (std::count(vec1.begin(), vec1.end(), 42.01002))
	{
		std::cerr << "err42";
	}

	return timer.get();
}

#include "../main.cpp"
