
import math
import multiprocessing
import itertools
import os
from pathlib import Path
import pandas as pd
import progressbar as pb
import numpy as np
import subprocess


def run_benchmark_folder(exec_folder_path: Path):
    for executable in exec_folder_path.iterdir():
        run_benchmark(executable)


def run_benchmark(executable_path: Path):
    alg_name = executable_path.as_posix().split("/")[1]
    impl = executable_path.as_posix().split("/")[2]

    print("\nStarting benchmark: (" + alg_name + ", " + impl + "):")

    # We create a list of logarithmically-spaced numbers. Those will
    # be the vector sizes for which the algorithm will be benchmarked.
    n_datapoints = 4
    n_min, n_max = [10**3, 10**7]
    n_list = [int(n) for n in np.logspace(
        math.log10(n_min), math.log10(n_max), n_datapoints)]

    # This may be used to manually select the number of chunks for
    # parallel algorithms. Value of 0 means HPX will use its
    # default heuristic.
    n_chunks_list = [1] if (impl=="STD_SEQ") else [0]


    for combination in pb.progressbar(itertools.product(n_list, n_chunks_list)):
        n, n_chunks = combination
        iterations = 10

        chunk_size = 0 if (n_chunks==0) else math.ceil(n / n_chunks)

        command = [executable_path, str(iterations),
                    str(n), str(chunk_size),
                    #    "--hpx:threads=20",
                    #   "--hpx:bind=numa-balanced"
                    ]

        # Run the algorithm. It will return a collection of floats, each float
        # representing elapsed time(ns) for each algorithm invocation.
        ret = subprocess.run(command, capture_output=True, check=False)

        if (ret.returncode != 0):
            print("\nExecution error:\n")
            print(ret)

        # convert output to list of tuples(alg_name, vector_size, time in ms)
        datapoints = [[alg_name, impl, n, chunk_size,
                        float(dt)/(10**6), n_chunks]
                        for dt in ret.stdout.splitlines()]

        # print("n = ", n, " :  ", datapoints, " ms")
        result_to_csv(alg_name, datapoints)
    print("Benchmark finished\n")


def result_to_csv(alg_name: str, results: list[list[str, str, int, int, float]]):
    df = pd.DataFrame(results, columns=[
                      "alg_name", "impl", "n", "chunk_size", "time", "chunks"])
    # print(df)

    filename = 'results.csv'
    df.to_csv(filename, mode='a', index=False,
              header=(not os.path.exists(filename)))


folder = Path("install/")

print("Found algorithms: ", [
    item.with_suffix("").name for item in folder.iterdir()])

for subfolder in folder.iterdir():
    run_benchmark_folder(subfolder)
