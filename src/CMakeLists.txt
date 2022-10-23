
function(add_exe alg_name call_define)
    set (target ${alg_name}_${call_define} )
    add_hpx_executable(
        ${target}
        SOURCES ${alg_name}.cpp
        HEADERS ../utilities.hpp ../call_defines.hpp
        COMPILE_FLAGS -DBENCH_${call_define}
        INSTALL_SUFFIX ${alg_name}/
    )
    
    set_target_properties(${target} 
    PROPERTIES OUTPUT_NAME ${call_define}
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/${alg_name})
endfunction()



add_subdirectory(algorithms)

