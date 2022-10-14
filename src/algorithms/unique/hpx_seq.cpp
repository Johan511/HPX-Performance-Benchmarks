#include <iostream>
#include <string>
#include <algorithm>
#include "hpx/hpx.hpp"
#include "hpx/hpx_main.hpp"

// define a callable "unique_if" object

struct unique_t
{

	void handle_args(std::vector<std::string> args) {}

	template <typename... Args>
	auto operator()(Args &&...args)
	{
		return hpx::unique(args...);
	}
} unique{};

#include "unique.hpp"
