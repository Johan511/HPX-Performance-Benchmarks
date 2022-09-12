
// ATTENTION: double test(int, std::size_t) function
// needs to be defined before including this file
#include <hpx/hpx.hpp>
#include <hpx/hpx_main.hpp>
#include <vector>
#include <string>
#include "ittnotify.h"

std::vector<double> test_n(std::vector<std::string> cl_arguments)
{
	int iterations = std::stoi(cl_arguments[0]);
	cl_arguments.erase(cl_arguments.begin()); // pop first element
	std::vector<double> time_vec;
	for (int i = 0; i < iterations; i++)
	{
		double dt = test(cl_arguments);
		time_vec.push_back(dt);
	}
	return time_vec;
}

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

	std::vector<double> time_vec = test_n(cl_arguments);

	// Output result

	for (auto datapoint : time_vec)
	{
		std::cout << datapoint << "\n";
	}

	return 0;
}