# HPX Performance Benchmarks

Performance benchmarks for HPX implementation of C++ parallel algorithms.
Made as part of [my 2022 GSoC project](https://pansysk75.github.io/blog/summer-of-code-2022/)

## Requirements:

* Functional HPX installation 
* Python & corresponding python modules


## How to run:

* Run ```bash cmake_build.sh```
>Note: You will need to modify HPX_DIR to point to the appropriate HPX installation path.
Executables should be build and installed in install/ folder
* Execute run.py to run the benchmarks. This should generate a results.csv file with all datapoints
* Execute plot.py to generate plots


