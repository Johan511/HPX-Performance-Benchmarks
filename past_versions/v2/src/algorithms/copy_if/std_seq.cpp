#include <iostream>
#include <string>
#include <algorithm>
#include <execution>

//define a callable "copy_if" object

struct copy_if_t {
	template<typename... Args>
	auto operator()(Args&&... args){
		return std::copy_if(args...);
	}
}copy_if{};

#include "copy_if.hpp"
