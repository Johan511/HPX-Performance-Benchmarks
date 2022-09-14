#include <string>
#include <algorithm>
#include "../utilities.hpp"
#include <hpx/hpx.hpp>
#include "ittnotify.h"

// ATTENTION: copy function (compatible with std::copy)
// needs to be defined before including this file

// define a "double test(std::vector<std::string> args)" function that returns
// execution time of "copy"
__itt_domain *pD = __itt_domain_create("My Domain");

utilities::timer timer;
utilities::random_vector_generator gen;

double test(std::vector<std::string> args)
{
	int vector_size = std::stoi(args[0]);
	auto vec1 = gen.get_doubles(vector_size);
	decltype(vec1) vec2(vec1.size());

	copy.handle_args(args);

	__itt_frame_begin_v3(pD, NULL);
	timer.start();
	hpx::annotated_function(copy, "copy")(vec1.begin(), vec1.end(), vec2.begin());
	timer.stop();
	__itt_frame_end_v3(pD, NULL);

	// use result otherwise compiler will optimize it away:
	if (hpx::annotated_function(hpx::count, "count")(vec2.begin(), vec2.end(), 42.0))
	{
		std::cerr << "err42";
	}

	return timer.get();
}

#include "../main.hpp"
