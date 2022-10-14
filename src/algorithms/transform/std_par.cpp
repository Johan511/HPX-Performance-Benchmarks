#include <iostream>
#include <string>
#include <algorithm>
#include <execution>

// define a callable "transform" object

struct transform_t
{

	void handle_args(std::vector<std::string> args) {}

	template <typename... Args>
	auto operator()(Args &&...args)
	{
		return std::transform(std::execution::par, args...);
	}
} transform{};

#include "transform.hpp"
