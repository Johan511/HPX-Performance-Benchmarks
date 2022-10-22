#include <iostream>
#include <string>
#include <algorithm>
#include "hpx/hpx.hpp"
#include "hpx/hpx_main.hpp"
#include <hpx/include/parallel_executor_parameters.hpp>

// parallel copy_if using fork-join executor.

// define a callable "copy_if" object

struct copy_if_t
{
	int chunk_size = 0;
	hpx::execution::static_chunk_size scs;
	hpx::execution::experimental::fork_join_executor exec;

	void handle_args(std::vector<std::string> args)
	{
		if (args.size() > 1)
		{
			chunk_size = std::stoi(args[1]);
			scs = hpx::execution::static_chunk_size(chunk_size);
		}
	}

	template <typename... Args>
	auto operator()(Args &&...args)
	{
		return hpx::copy_if(hpx::execution::par.on(exec).with(scs), args...);
	}
};

#include "copy_if.hpp"
