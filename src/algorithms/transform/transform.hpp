#include <string>
#include <algorithm>
#include "../utilities.hpp"
#include <hpx/hpx.hpp>
#include "ittnotify.h"

// ATTENTION: transform function (compatible with std::transform)
// needs to be defined before including this file

// define a "double test(std::vector<std::string> args)" function that returns
// execution time of "transform"
__itt_domain *pD = __itt_domain_create("My Domain");

utilities::timer timer;
utilities::random_vector_generator gen;

auto unary_op = [](double num)
{ return ((int)num % 4) < 2; };

double test(std::vector<std::string> args)
{
	transform_t transform;

	int vector_size = std::stoi(args[0]);
	// hpx::scoped_annotation annotate("test");
	auto vec1 = gen.get_doubles(vector_size);
	std::vector<int> vec2(vec1.size());

	transform.handle_args(args);

	__itt_frame_begin_v3(pD, NULL);
	timer.start();
	hpx::annotated_function(transform, "transform")(vec1.begin(), vec1.end(), vec2.begin(), unary_op);
	timer.stop();
	__itt_frame_end_v3(pD, NULL);

	// use result otherwise compiler will optimize it away:
	if (hpx::annotated_function(hpx::count, "count")(vec2.begin(), vec2.end(), 42))
	{
		std::cerr << "err42";
	}

	return timer.get();
}

#include "../main.hpp"
