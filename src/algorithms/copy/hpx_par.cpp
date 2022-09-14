#include <iostream>
#include <string>
#include <algorithm>
#include "hpx/hpx.hpp"
#include "hpx/hpx_main.hpp"

// define a callable "copy_if" object

struct copy_t
{

	void handle_args(std::vector<std::string> args) {}

	template <typename... Args>
	auto operator()(Args &&...args)
	{
		return hpx::copy(hpx::execution::par, args...);
	}
} copy{};

#include "copy.hpp"
