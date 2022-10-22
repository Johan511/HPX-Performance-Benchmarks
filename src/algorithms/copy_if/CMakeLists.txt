
set(executables
std_seq
hpx_par
hpx_par_scs
my_seq
hpx_par_sched-exec
# hpx_par_fork-join
)

foreach(executable ${executables})
add_exe(${executable})
endforeach(executable)

