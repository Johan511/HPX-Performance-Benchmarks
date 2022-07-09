function(add_exe target)
    add_hpx_executable(${target} SOURCES ${target}.cpp)
    target_compile_options(${target} PRIVATE "-O3")
endfunction()

add_exe(copy_if)
add_exe(for_each)
add_exe(transform)
