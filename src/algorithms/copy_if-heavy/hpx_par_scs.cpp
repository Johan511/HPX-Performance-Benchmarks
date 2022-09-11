#include <iostream>
#include <string>
#include <algorithm>
#include <hpx/hpx.hpp>
#include "../utilities.hpp"
#include "ittnotify.h"

// ATTENTION: copy_if function (compatible with std::copy_if)
// needs to be defined before including this file

// define a "double test(int vector_size)" function that returns
// execution time of "copy_if"
__itt_domain *pD = __itt_domain_create("My Domain");

utilities::timer timer;
utilities::random_vector_generator gen;

auto pred = [](double num)
{ return ((int)std::pow(num, 1.2) % 8) < 4; };

double test(int vector_size, std::size_t chunk_size)
{
	auto vec1 = gen.get_doubles(vector_size);
	decltype(vec1) vec2(vec1.size());

	hpx::execution::static_chunk_size scs(chunk_size);

	__itt_frame_begin_v3(pD, NULL);
	timer.start();
	hpx::copy_if(hpx::execution::par.with(scs), vec1.begin(), vec1.end(), vec2.begin(), pred);
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
