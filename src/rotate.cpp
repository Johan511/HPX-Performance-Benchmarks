#include <hpx/hpx.hpp>
#include <hpx/hpx_main.hpp>
#include <hpx/include/parallel_executor_parameters.hpp>

#include <vector>
#include <string>
#include <algorithm>
#include <iostream>

#include "utilities.hpp"

double test(int vector_size)
{
	utilities::timer timer;
	utilities::random_vector_generator gen;

	auto vec = gen.get_doubles(vector_size);

	// Choose a random integer to rotate to
	int k = gen.get_ints(1, 0, vector_size - 1)[0];

	timer.start();
	hpx::rotate(vec.begin(), vec.begin() + k, vec.end());
	timer.stop();

	// use result otherwise compiler might optimize it away:
	if (std::count(vec.begin(), vec.end(), 42))
	{
		std::cerr << "err42";
	}

	return timer.get();
}

// Run test for many iterations
std::vector<double> test_n(int iterations, int vector_size)
{
	std::vector<double> time_vec;
	for (int i = 0; i < iterations; i++)
	{
		double dt = test(vector_size);
		time_vec.push_back(dt);
	}
	return time_vec;
}

int main(int argc, char *argv[])
{
	// put command line arguements in a vector
	std::vector<std::string> cl_arguments(argv + 1, argv + argc);

	if (cl_arguments.size() < 2)
	{
		std::cout << "Command line arguments not set" << std::endl;
		std::cout << "Please specify iterations, vector size" << std::endl;
		return 1;
	}

	int iterations = stoi(cl_arguments[0]);
	int vector_size = stoi(cl_arguments[1]);
	std::vector<double> time_vec = test_n(iterations, vector_size);

	// Output result

	for (auto datapoint : time_vec)
	{
		std::cout << datapoint << "\n";
	}

	return 0;
}