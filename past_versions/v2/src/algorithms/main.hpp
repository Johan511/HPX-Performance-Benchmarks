
// ATTENTION: double test(int) function
// needs to be defined before including this file
#include <hpx/hpx.hpp>
#include <vector>
#include "ittnotify.h"

std::vector<double> test_n(int iterations, int vector_size)
{
	std::vector<double> time_vec;
	for (int i = 0; i < iterations; i++)
	{
		time_vec.push_back(test(vector_size));
	}
	return time_vec;
}

int main(int argc, char *argv[])
{
	// hpx::scoped_annotation annotate("my_main");

	// handle command line input arguements
	if (argc < 2)
	{
		std::cout << "Command line arguements not set" << std::endl;
		std::cout << "Please specify vector size, iterations" << std::endl;
		return 1;
	}

	int vector_size = std::stoi(argv[1]);
	int iterations = std::stoi(argv[2]);

	std::vector<double> time_vec = test_n(iterations, vector_size);

	// Output result

	for (auto datapoint : time_vec)
	{
		std::cout << datapoint << "\n";
	}

	return 0;
}