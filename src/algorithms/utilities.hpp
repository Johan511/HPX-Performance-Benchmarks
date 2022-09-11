#include <vector>
#include <chrono>
#include <random>
#include <string>

namespace utilities {


	class random_vector_generator {

	private:
		std::mt19937 mersenne_engine{ 42 };
		std::uniform_real_distribution<double> dist_double{ 1, 1024 };

	public:
		std::vector<double> get_doubles(size_t size) {

			auto gen = [this]()
			{
				return dist_double(mersenne_engine);
			};

			std::vector<double> vec(size);
			std::generate(vec.begin(), vec.end(), gen);
			return vec;
		}

	};


	class timer {

	private:
		std::chrono::high_resolution_clock::time_point t1;
		std::chrono::high_resolution_clock::time_point t2;

	public:
		void start() { t1 = std::chrono::high_resolution_clock::now(); }
		void stop() { t2 = std::chrono::high_resolution_clock::now(); }
		double get() { return (double)std::chrono::duration_cast<std::chrono::nanoseconds>(t2 - t1).count(); }

	};


}