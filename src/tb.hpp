#include "./utilities.hpp"

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
    TestBench(int n)
    {
        T t;
        std::cout << t(n) << std::endl;
    }
};