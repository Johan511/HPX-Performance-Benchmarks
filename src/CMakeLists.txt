function(add_exe target)
    add_hpx_executable(${target} SOURCES ${target}.cpp)  
    if(WIN32)
        add_custom_command(TARGET ${target} POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_INSTALL_PREFIX}/bin/
            COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_RUNTIME_DLLS:${target}> ${CMAKE_INSTALL_PREFIX}/bin
            COMMAND_EXPAND_LISTS
        )
    endif()
endfunction()

add_exe(copy_if)
add_exe(for_each)
add_exe(transform)
