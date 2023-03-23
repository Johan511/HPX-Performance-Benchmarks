#include "./utilities.hpp"

#define WARM_CACHE 500 // number of initial iterations to warm up the cache

class Test
{
public:
    friend class util::Timer;
    virtual ~Test() = default;
};

class AlgorithmTest : Test
{
public:
    virtual ~AlgorithmTest() = default;

    double bench(void (*f)(std::vector<double> &), int n)
    {
        std::vector<double> v = util::get_doubles(n);
        util::Timer t;
        t.start();
        f(v);
        t.stop();
        return t.get();
    }
};

template <class T>
class TestBench
{
public:
    std::vector<double> runTimes;
    TestBench(int n, int itr)
    {
        T t;

        // warming the cache
        for (int i = 0; i < WARM_CACHE; i++)
            t(n);

        // testing
        for (int i = 0; i < itr; i++)
            runTimes.push_back(t(n));
    }

    ~TestBench()
    {
        for (double &dp : runTimes)
            std::cout << dp << '\n';
    }
};