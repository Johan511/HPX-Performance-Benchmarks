set(algorithms
"all_of"
"copy_if-heavy"
"copy_if"
"copy"
"count"
"find"
"find_if"
"for_each"
"for_each-heavy"
"remove"
"reverse"
"search"
"sort"
"transform"
"transform-heavy"
)

#fork_join executor only works with algorithms that use bulk_x_execute
set(fork_join_algorithms
"copy"
"find"
"reverse"
"transform"
"transform-heavy"
)



# Build the standard executables

foreach(algorithm ${algorithms})
    add_exe(${algorithm} STD_SEQ)
    add_exe(${algorithm} HPX_PAR_SCS)
endforeach(algorithm)


# Build with the scheduler / fork-join executors

if(BUILD_SCHED_EXEC)
    foreach(algorithm ${algorithms})
        add_exe(${algorithm} HPX_PAR_SCHED_EXEC)
    endforeach(algorithm)
endif()


if(BUILD_FORK_JOIN_EXEC)
    foreach(algorithm ${fork_join_algorithms})
        add_exe(${algorithm} HPX_PAR_SCHED_EXEC)
    endforeach(algorithm)
endif()



