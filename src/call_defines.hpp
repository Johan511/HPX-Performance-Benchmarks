#if defined(BENCH_STD_SEQ)

#define BENCH_INIT(...) \
    {                   \
    }
#define BENCH_CALL(name, ...) std::name(__VA_ARGS__)

#elif defined(BENCH_HPX_PAR)

#include <hpx/hpx.hpp>
#include <hpx/include/parallel_executor_parameters.hpp>

#define BENCH_INIT(...) \
    {                   \
    }
#define BENCH_CALL(name, ...) hpx::name(hpx::execution::par __VA_OPT__(, ) __VA_ARGS__)

#elif defined(BENCH_HPX_PAR_SCS)

#include <hpx/hpx.hpp>
#include <hpx/include/parallel_executor_parameters.hpp>

#define BENCH_INIT(argv) \
    hpx::execution::static_chunk_size scs(stoi(argv[1]));

#define BENCH_CALL(name, ...) hpx::name(hpx::execution::par.with(scs) __VA_OPT__(, ) __VA_ARGS__)

#elif defined(BENCH_HPX_PAR_FORK_JOIN)

#include <hpx/hpx.hpp>
#include <hpx/include/parallel_executor_parameters.hpp>

#define BENCH_INIT(argv)                                  \
    hpx::execution::static_chunk_size scs(stoi(argv[1])); \
    hpx::execution::experimental::fork_join_executor exec;

#define BENCH_CALL(name, ...) hpx::name(hpx::execution::par.on(exec).with(scs) __VA_OPT__(, ) __VA_ARGS__)

#elif defined(BENCH_HPX_PAR_SCHED_EXEC)

#include <hpx/hpx.hpp>
#include <hpx/include/parallel_executor_parameters.hpp>

#define BENCH_INIT(argv)                                  \
    hpx::execution::static_chunk_size scs(stoi(argv[1])); \
    hpx::execution::experimental::scheduler_executor<hpx::execution::experimental::thread_pool_scheduler> exec;

#define BENCH_CALL(name, ...) hpx::name(hpx::execution::par.on(exec).with(scs) __VA_OPT__(, ) __VA_ARGS__)

#else
#error No call define

#endif
