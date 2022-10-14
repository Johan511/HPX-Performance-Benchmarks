#include <iostream>
#include <string>
#include <algorithm>
#include "hpx/hpx.hpp"
#include "hpx/hpx_main.hpp"
#include <hpx/include/parallel_executor_parameters.hpp>

// define a callable "unique_if" object

struct unique_t
{
	int chunk_size = 0;

	void handle_args(std::vector<std::string> args)
	{
		if (args.size() > 1)
		{
			chunk_size = std::stoi(args[1]);
		}
	}

	template <typename... Args>
	auto operator()(Args &&...args)
	{
		// ideally construction of the executor should be somehow
		// moved to handle_args, so that it isn't timed by the timer
		hpx::execution::static_chunk_size scs(chunk_size);
		return hpx::unique(hpx::execution::par.with(scs), args...);
	}
} unique{};

#include "unique.hpp"
