#include <hpx/hpx.hpp>
#include <hpx/hpx_main.hpp>
#include <hpx/include/parallel_executor_parameters.hpp>

#include <vector>
#include <string>
#include <algorithm>
#include <iostream>
#include <tuple>

#include "utilities.hpp"

double test(int vector_size)
{
	utilities::random_vector_generator gen;
	using utilities::timer;

	std::vector<double> vec1 = gen.get_doubles(vector_size);
	std::vector<double> vec2(vec1.size());

	double factor = 2.123;
	auto scale_func = [factor](double& val){
		return factor*val;
	};

	timer.start();
	hpx::transform(hpx::execution::par, vec1.begin(), vec1.end(), vec2.begin(), scale_func);
	timer.stop();

	// use result otherwise compiler might optimize it away:
	if (std::count(vec1.begin(), vec1.end(), 42))
	{
		std::cerr << "err42";
	}

	return timer.get();
}

// Run test for many iterations
std::vector<std::tuple<double, double>> test_n(int iterations, int vector_size)
{
	//warmup a bit?
	for (int i = 0; i < 500; i++)
	{
	test(vector_size);
	}

	std::vector<std::tuple<double, double>> time_vec;
	for (int i = 0; i < iterations; i++)
	{
		double t = utilities::timer.now();
		double dt = test(vector_size);
		time_vec.push_back({t, dt});
	}
	return time_vec;
}

std::string output_as_json(const std::vector<std::tuple<double, double>>& time_vec){

	auto elem_to_json = [](const std::tuple<double, double>& elem){
		std::string elem_str;
		elem_str += "{\"t\":";
		elem_str += std::to_string(std::get<0>(elem));
		elem_str += ",\"dt\":";
		elem_str += std::to_string(std::get<1>(elem));
		elem_str += "}";
		return elem_str;
	};

	std::string output;
	output += "[";

	for (auto it = time_vec.begin(); it!=time_vec.end()-1; it++){
		output += elem_to_json(*it);
		output += ",";
	}
	output += elem_to_json(time_vec.back());
	
	output += "]";
	
	return output;
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
	std::vector<std::tuple<double, double>> time_vec = test_n(iterations, vector_size);

	// Output result

	std::cout << output_as_json(time_vec) << std::endl;

	return 0;
}