
import math
import multiprocessing
from itertools import product
import os
from pathlib import Path
import pandas as pd
from progressbar import progressbar
import numpy as np
import subprocess


def run_benchmark(executable_path: Path):
    alg_name = executable_path.as_posix().split("/")[1]
    impl = executable_path.as_posix().split("/")[2]

    print("\nStarting benchmark: (" + alg_name + ", " + impl + "):")

    # The sizes of the data the algorithm will process (2^5, 2^6 .... 2^30)
    n_list = [int(2**i) for i in range(5,28)]

    # Will be passed as an argument to the executable
    iterations = 10

    for combination in product(n_list, n_chunks_list, n_threads_list):
        n, n_chunks, n_threads = combination

        chunk_size = 0 if (n_chunks==0) else math.ceil(n / n_chunks)

        command = [executable_path, str(iterations),
                    str(n)
                    #   "--hpx:bind=numa-balanced"
                    ]
        command += [] if (n_chunks == 0) else [str(chunk_size)]
        command += [] if (n_threads == 0) else ["--hpx:threads="+str(n_threads)]

        # Run the algorithm. It will return a collection of floats, each float
        # representing elapsed time(ns) for each algorithm invocation.
        ret = subprocess.run(command, capture_output=True, check=False)

        if (ret.returncode != 0):
            print("\nExecution error:\n")
            print(ret)

        # For every run, attach all relevant data and add in list
        datapoints = [[alg_name, impl, n, n_threads, n_chunks,
                        float(dt)/(10**6)] for dt in ret.stdout.splitlines()]

        result_to_csv(alg_name, datapoints)
    print("Benchmark finished\n")


def result_to_csv(alg_name: str, results: list[list[str, str, int, int, float]]):
    df = pd.DataFrame(results, columns=[
                      "alg_name", "impl", "n", "n_threads", "n_chunks", "time"])
    # print(df)

    filename = 'results.csv'
    df.to_csv(filename, mode='a', index=False,
              header=(not os.path.exists(filename)))



folder = Path("install/")

print("Found algorithms: ", [
    item.with_suffix("").name for item in folder.iterdir()])

for subfolder in folder.iterdir():
    for executable in subfolder.iterdir():
        run_benchmark(executable)
