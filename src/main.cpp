
// ATTENTION: double test(int, std::size_t) function
// needs to be defined before including this file
#include <hpx/hpx.hpp>
#include <hpx/hpx_main.hpp>
#include <vector>
#include <string>
#include "./tb.hpp"

class MakeHeapAlgorithmTest : AlgorithmTest
{
public:
	virtual ~MakeHeapAlgorithmTest() = default;
	static inline void f(std::vector<double> &v)
	{
		hpx::make_heap(hpx::execution::par, v.begin(), v.end());
	}

	double operator()(int n)
	{
		return bench(f, n);
	}
};

int main(int argc, char *argv[])
{

	// put command line arguements in a vector
	// (vector size, iterations, optional args...)
	std::vector<std::string> cl_arguments(argv + 1, argv + argc);

	if (cl_arguments.size() < 2)
	{
		std::cout << "Command line arguments not set" << std::endl;
		std::cout << "Please specify iterations, vector size,  (, optional args)" << std::endl;
		return 1;
	}

	if (cl_arguments.size() < 3)
	{
		cl_arguments.push_back("0");
	}

	TestBench<MakeHeapAlgorithmTest>(100000000);
	return 0;
}