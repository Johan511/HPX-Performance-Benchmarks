#include <iostream>
#include <string>
#include <algorithm>
#include <execution>

// define a callable "copy_if" object

struct copy_if_t
{

	void handle_args(std::vector<std::string> args) {}

	template <typename... Args>
	auto operator()(Args &&...args)
	{
		return impl_copy_if(args...);
	}

	template <typename _InputIterator, typename _OutputIterator,
			  typename _Predicate>
	auto impl_copy_if(_InputIterator first, _InputIterator last,
					  _OutputIterator result, _Predicate pred)
	{

		for (; first != last; ++first)
		{
			if (pred(*first))
			{
				*result = *first;
				++result;
			}
		}
		return result;
	}
} copy_if{};

#include "copy_if.hpp"
