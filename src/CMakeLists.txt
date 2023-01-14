cmake_minimum_required (VERSION 3.8)

SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

project ("HPX_Bench")
find_package(HPX REQUIRED)


# Define build options
option(BUILD_SCHED_EXEC "Build executables that use the scheduler executor" OFF)
option(BUILD_FORK_JOIN_EXEC "Build executables that use the scheduler executor" OFF)


# Function that makes the HPX executables
# Possible call defines are in src/call_defines.hpp file

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

add_subdirectory ("algorithms")

