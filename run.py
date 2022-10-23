
import math
import multiprocessing
import os
from pathlib import Path
import pandas as pd
import progressbar as pb
import numpy as np
import subprocess


def benchmark_folder(exec_folder_path: Path):
    for executable in exec_folder_path.iterdir():
        # if executable.stem not in ["hpx_par_scs", "hpx_par_fork-join", "hpx_par_sched-exec"]:
        #     continue
        benchmark_chunks(executable)


def benchmark_chunks(executable_path: Path):
    alg_name = executable_path.as_posix().split("/")[1]
    impl = executable_path.as_posix().split("/")[2]
    print("\nStarting benchmark: (" + alg_name + ", " + impl + "):")

    # We create a list of logarithmically-spaced numbers. Those will
    # be the vector sizes for which the algorithm will be benchmarked.
    n_datapoints = 100
    n_min, n_max = [10**3, 10**7]

    n_list = [int(n) for n in np.logspace(
        math.log10(n_min), math.log10(n_max), n_datapoints)]

    cores = multiprocessing.cpu_count()
    if "STD_SEQ" in alg_name:
        chunks_list = [1]
    else:
        chunks_list = [1, 4, 10, 20, 40, 80, 160, 320, 640]

    for n in pb.progressbar(n_list):
        results = list()
        for n_chunks in chunks_list:
            iterations = 50
            chunk_size = math.ceil(n / n_chunks)
            # chunk_size = 0
            command = [executable_path, str(iterations),
                       str(n), str(chunk_size),
                       #    "--hpx:threads="+str(n_threads)
                       ]

            # Run the algorithm. It will return a collection of floats, each float
            # representing elapsed time(ns) for each algorithm invocation.
            ret = subprocess.run(command, capture_output=True, check=False)

            if (ret.returncode != 0):
                print("\nExecution error:\n")
                print(ret)

            # convert output to list of tuples(alg_name, vector_size, time in ms)
            datapoints = [[alg_name, impl, n, chunk_size, float(dt)/(10**6), n_chunks]
                          for dt in ret.stdout.splitlines()]

            # print("n = ", n, " :  ", datapoints, " ms")
            results.extend(datapoints)
        result_to_csv(alg_name, results)
    print("Benchmark finished\n")


def result_to_csv(alg_name: str, results: list[list[str, str, int, int, float]]):
    df = pd.DataFrame(results, columns=[
                      "alg_name", "impl", "n", "chunk_size", "time", "chunks"])
    # print(df)

    filename = 'results.csv'
    df.to_csv(filename, mode='a', index=False,
              header=(not os.path.exists(filename)))


folder = Path("executables/")

print("Found algorithms: ", [
    item.with_suffix("").name for item in folder.iterdir()])

for subfolder in folder.iterdir():

    # if subfolder.stem not in ["transform"]:
    #     continue

    benchmark_folder(subfolder)
