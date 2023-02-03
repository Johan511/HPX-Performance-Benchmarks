cmake_minimum_required (VERSION 3.8)

SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

project ("HPX_Benchmark")
find_package(HPX REQUIRED)

add_hpx_executable(
    scale
    SOURCES scale.cpp
    HEADERS utilities.hpp
)

add_hpx_executable(
    add
    SOURCES add.cpp
    HEADERS utilities.hpp
)



