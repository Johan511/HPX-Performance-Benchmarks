#include <iostream>
#include <string>
#include <algorithm>
#include <execution>

// define a callable "remove_if" object

struct remove_t
{

	void handle_args(std::vector<std::string> args) {}

	template <typename... Args>
	auto operator()(Args &&...args)
	{
		return std::remove(std::execution::par, args...);
	}
} _remove{};

#include "remove.hpp"
