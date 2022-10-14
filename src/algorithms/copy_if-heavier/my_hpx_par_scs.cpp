#include <iostream>
#include <string>
#include <algorithm>
#include "hpx/hpx.hpp"
#include "hpx/hpx_main.hpp"

// define a callable "copy_if" object

struct copy_if_t
{

	int chunk_size = 0;

	void handle_args(std::vector<std::string> args)
	{
		if (args.size() > 1)
		{
			chunk_size = std::stoi(args[1]);
		}
	}

	template <typename... Args>
	auto operator()(Args &&...args)
	{
		hpx::execution::static_chunk_size scs(chunk_size);
		return copy_if_impl(hpx::execution::par.with(scs), args...);
	}

	template <typename ExPolicy, typename InIter1, typename InIter2,
			  typename OutIter, typename Pred
			  /*,typename Proj*/>
	OutIter copy_if_impl(ExPolicy &&policy, InIter1 first, InIter2 last,
						 OutIter dest, Pred &&pred
						 /* ,Proj&& proj  = Proj()*/)
	{
		auto count = std::distance(first, last);
		std::vector<uint8_t> flags(count);
		// std::vector<uint32_t> scan_result(count);
		hpx::transform(policy, first, last, flags.begin(),
					   [&pred](const auto &elem)
					   {
						   return pred(elem);
					   });
		// hpx::exclusive_scan(policy, flags.begin(), flags.end(), scan_result.begin(), 0);

		auto flags_it = flags.begin();
		// auto scan_result_it = scan_result.begin();
		while (first != last)
		{
			if (*flags_it++)
			{
				*dest++ = *first;
			}
			first++;
		}
		return dest;
	}

} copy_if{};

#include "copy_if.hpp"
