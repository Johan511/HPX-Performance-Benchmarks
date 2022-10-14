#include <string>
#include <algorithm>
#include "../utilities.hpp"
#include <hpx/hpx.hpp>
#include "ittnotify.h"

// ATTENTION: copy_if function (compatible with std::copy_if)
// needs to be defined before including this file

// define a "double test(std::vector<std::string> args)" function that returns
// execution time of "copy_if"
__itt_domain *pD = __itt_domain_create("My Domain");

utilities::timer timer;
utilities::random_vector_generator gen;

auto pred = [](const std::vector<double> elem)
{ return (((int)(elem[0])) % 4) < 2; };

std::vector<std::vector<double>> gen_data(int n)
{
	std::vector<std::vector<double>> data;
	for (int i = 0; i < n; i++)
	{
		std::vector<double> vec = gen.get_doubles(10);
		data.push_back(vec);
	}
	return data;
}

double test(std::vector<std::string> args)
{
	int vector_size = std::stoi(args[0]);
	// hpx::scoped_annotation annotate("test");
	std::vector<std::vector<double>> vec1 = gen_data(vector_size);
	decltype(vec1) vec2(vec1.size());

	copy_if.handle_args(args);

	__itt_frame_begin_v3(pD, NULL);
	timer.start();
	hpx::annotated_function(copy_if, "copy_if")(vec1.begin(), vec1.end(), vec2.begin(), pred);
	timer.stop();
	__itt_frame_end_v3(pD, NULL);

	// use result otherwise compiler will optimize it away:
	if (hpx::annotated_function(hpx::count, "count")(vec2.begin(), vec2.end(), std::vector<double>(10, 42)))
	{
		std::cerr << "err42";
	}

	return timer.get();
}

#include "../main.hpp"
