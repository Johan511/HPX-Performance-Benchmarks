
set(executables
    std_seq
    std_par
    hpx_seq
    hpx_par
)

foreach(executable ${executables})
    add_exe(${executable})
endforeach(executable)

