#include <iostream>
#include <string>
#include <algorithm>
#include "hpx/hpx.hpp"
#include "hpx/hpx_main.hpp"
#include <hpx/include/parallel_executor_parameters.hpp>

// parallel transform using scheduler_executor.

// define a callable "transform" object

struct transform_t
{
	using sched_exec = hpx::execution::experimental::scheduler_executor<
		hpx::execution::experimental::thread_pool_scheduler>;

	int chunk_size = 0;
	hpx::execution::static_chunk_size scs;
	sched_exec exec;

	void handle_args(std::vector<std::string> args)
	{
		if (args.size() > 1)
		{
			chunk_size = std::stoi(args[1]);
			scs = hpx::execution::static_chunk_size();
		}
	}

	template <typename... Args>
	auto operator()(Args &&...args)
	{
		return hpx::transform(hpx::execution::par.on(exec).with(scs), args...);
	}
};

#include "transform.hpp"
