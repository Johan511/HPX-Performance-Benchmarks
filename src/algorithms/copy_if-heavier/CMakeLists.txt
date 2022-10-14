
set(executables
std_seq
std_par
hpx_seq
hpx_par
hpx_par_scs
my_hpx_par_scs
)

foreach(executable ${executables})
add_exe(${executable})
endforeach(executable)

