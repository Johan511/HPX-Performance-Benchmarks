set(algorithms
"copy_if-heavy"
"copy_if"
"copy"
"count"
"find"
"remove"
"reverse"
"sort"
"transform"
"transform-heavy"
)
set(vtune_dir "C:/Program Files (x86)/Intel/oneAPI/vtune/latest/sdk")

#fork_join executor only works with algorithms that use bulk_x_execute
set(fork_join_algorithms
"copy"
"find"
"reverse"
"transform"
"transform-heavy"
)



set(call_defines
STD_SEQ
HPX_PAR_SCS
HPX_PAR_SCHED_EXEC
)


foreach(algorithm ${algorithms})
    foreach(call_define ${call_defines})
    add_exe(${algorithm} ${call_define})
    endforeach(call_define)
endforeach(algorithm)

foreach(algorithm ${fork_join_algorithms})
    add_exe(${algorithm} HPX_PAR_FORK_JOIN)
endforeach(algorithm)


