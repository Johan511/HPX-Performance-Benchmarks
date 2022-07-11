# HPX Scaling Benchmarks

Scaling benchmarks for HPX implementation of C++ parallel algorithms

## Requirements:

* HPX installation
* Pandas, matplotlib and progress python libraries \
Can be installed using `pip install pandas matplotlib progress`



## How to run:

* Build project using `HPX_DIR=/your/HPX/path/ cmake . --preset linux-Release`
* Build executables with `cmake --build ./build`
* Install with `cmake --install ./build` \
(Executables should now be located in ./install/bin/)
* Execute run.py to run the benchmarks
* Execute plot.py to generate plots (saved in results folder)
