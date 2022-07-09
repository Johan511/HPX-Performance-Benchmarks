#include <vector>
#include <chrono>
#include <random>

namespace utilities{

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

    class csv_result_file {
        //csv structure is hardcoded on purpose

        private:

        std::string filename;


        public:

        csv_result_file(std::string algorithm_name) : filename(algorithm_name + ".csv") {
            //if file doesn't exist, create it
            if (!std::filesystem::exists(filename)) {
                std::ofstream fout(filename);
                fout << "vector_size,threads,std_seq_time,hpx_seq_time,hpx_par_time\n";
                fout.close();
            }
        }

        void append(int vector_size, int threads, double std_seq_time, double hpx_seq_time, double hpx_par_time) {
            std::ofstream fout;
            fout.open(filename, std::ios_base::app);

            fout << std::setprecision(15)
                << vector_size << ","
                << threads << ","
                << std_seq_time << ","
                << hpx_seq_time << ","
                << hpx_par_time << "\n";
            fout.close();
        } 
    };

}