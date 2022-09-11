set(vtune_dir "/opt/intel/oneapi/vtune/latest/sdk")

function(add_exe target)
    get_filename_component(alg_name ${CMAKE_CURRENT_SOURCE_DIR} NAME)
    add_hpx_executable(
        ${alg_name}_${target} 
        SOURCES ${target}.cpp
        HEADERS ../utilities.hpp ${vtune_dir}/include
        DEPENDENCIES ${vtune_dir}/lib64/libittnotify.a
        INSTALL_SUFFIX ${alg_name}/
    )
    
    set_target_properties(${alg_name}_${target} PROPERTIES OUTPUT_NAME ${target})
endfunction()


 set(subdirs 
    "copy_if"
    "copy_if-heavy"
)

foreach(subdir ${subdirs})
    message("Adding subdir ${subdir}")
    add_subdirectory(${subdir})
endforeach(subdir)
