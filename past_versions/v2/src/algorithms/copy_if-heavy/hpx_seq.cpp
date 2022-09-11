#include <iostream>
#include <string>
#include <algorithm>
#include "hpx/hpx.hpp"
#include "hpx/hpx_main.hpp"

//define a callable "copy_if" object

struct copy_if_t {
	template<typename... Args>
	auto operator()(Args&&... args) {
		return hpx::copy_if(args...);
	}
}copy_if{};

#include "copy_if.hpp"

