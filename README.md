# HPX Performance Benchmarks

Performance benchmarks for HPX implementation of C++ parallel algorithms.
Made as part of [my 2022 GSoC project](https://pansysk75.github.io/blog/summer-of-code-2022/)

## Requirements:

* Functional HPX installation 
>Note: If you wish to use Intel VTune, build in RelWithDebInfo mode, set HPX_WITH_ITTNOTIFY=ON
>and define the appropriate AMPLIFIER_ROOT directory

* Python & corresponding python modules


## How to run:

* Check CMakePresets.json and choose/create an appropriate preset
>Note: CMake variables (such as HPX_DIR, BOOST_DIR, CMAKE_BUILD_TYPE) can be set here.
* Build project using `HPX_DIR=/your/HPX/path/ cmake . --preset PRESET_NAME`  
(where PRESET_NAME the appropriate preset from CMakePresets.json)
* Build executables with `cmake --build ./build`
* Install with `cmake --install ./build`  
(Executables should now be located in ./install/)
* Execute run.py to run the benchmarks. This should generate a results.csv file with all datapoints
* Execute plot.py to generate plots


