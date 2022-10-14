#include <iostream>
#include <string>
#include <algorithm>
#include <execution>

// define a callable "unique_if" object

struct unique_t
{

	void handle_args(std::vector<std::string> args) {}

	template <typename... Args>
	auto operator()(Args &&...args)
	{
		return std::unique(std::execution::par, args...);
	}
} unique{};

#include "unique.hpp"
