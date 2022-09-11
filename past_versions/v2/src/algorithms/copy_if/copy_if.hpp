#include "../utilities.hpp"
#include <hpx/hpx.hpp>
#include "ittnotify.h"

// ATTENTION: copy_if function (compatible with std::copy_if)
// needs to be defined before including this file

// define a "double test(int vector_size)" function that returns
// execution time of "copy_if"
__itt_domain *pD = __itt_domain_create("My Domain");

utilities::timer timer;
utilities::random_vector_generator gen;

auto pred = [](double num)
{ return ((int)num % 4) < 2; };

double test(int vector_size)
{
	// hpx::scoped_annotation annotate("test");
	auto vec1 = gen.get_doubles(vector_size);
	decltype(vec1) vec2(vec1.size());

	__itt_frame_begin_v3(pD, NULL);
	timer.start();
	hpx::annotated_function(copy_if, "copy_if")(vec1.begin(), vec1.end(), vec2.begin(), pred);
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
