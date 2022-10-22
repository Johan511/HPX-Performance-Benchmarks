
set(executables
std_seq
hpx_par
hpx_par_scs
)

foreach(executable ${executables})
add_exe(${executable})
endforeach(executable)

