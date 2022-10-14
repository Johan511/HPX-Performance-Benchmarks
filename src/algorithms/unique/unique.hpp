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
	auto vec1 = gen.get_ints(vector_size, 0, 3);

	unique.handle_args(args);

	__itt_frame_begin_v3(pD, NULL);
	timer.start();
	hpx::annotated_function(unique, "unique")(vec1.begin(), vec1.end());
	timer.stop();
	__itt_frame_end_v3(pD, NULL);

	// use result otherwise compiler will optimize it away:
	if (hpx::annotated_function(hpx::count, "count")(vec1.begin(), vec1.end(), 42))
	{
		std::cerr << "err42";
	}

	return timer.get();
}

#include "../main.hpp"
