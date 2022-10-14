#include <iostream>
#include <string>
#include <algorithm>
#include "hpx/hpx.hpp"
#include "hpx/hpx_main.hpp"

// define a callable "transform" object

struct transform_t
{

	void handle_args(std::vector<std::string> args) {}

	template <typename... Args>
	auto operator()(Args &&...args)
	{
		return hpx::transform(hpx::execution::par, args...);
	}
} transform{};

#include "transform.hpp"
