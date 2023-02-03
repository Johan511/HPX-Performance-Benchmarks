
import math
import multiprocessing
import itertools
import os
from pathlib import Path
import pandas as pd
import progressbar as pb
import numpy as np
import subprocess
import json


def run_benchmark(executable_path: Path):

    alg_name = executable_path.split("/")[-1]
    print("\nStarting benchmark: (" + alg_name + "):")

    # The sizes of the data the algorithm will process (2^5, 2^6 .... 2^30)
    n_list = [2**20]

    # This list is for selecting the number of threads to be tested
    # Value of 0 means all threads
    n_threads_list = [0]

    # Will be passed as an argument to the executable
    iterations = 500

    # How many times to launch the executable
    n_extern_iter = 10

    for combination in pb.progressbar(itertools.product(n_list, n_threads_list, range(n_extern_iter))):
        n, n_threads, extern_iter = combination

        command = [executable_path, str(iterations),
                    str(n)
                    #   "--hpx:bind=numa-balanced"
                    ]

        command += [] if (n_threads == 0) else ["--hpx:threads="+str(n_threads)]

        # Run the algorithm.
        ret = subprocess.run(command, capture_output=True, check=False)

        if (ret.returncode != 0):
            print("\nExecution error:\n")
            print(ret)

        # Parse output. Output is a string in json format (array of dicts)
        data = json.loads(ret.stdout)

        # For every run, attach all relevant data and add in list
        datapoints = [[alg_name, n, n_threads, extern_iter,
                       d["t"]/(10**6),  d["dt"]/(10**6)] for d in data ]

        result_to_csv(alg_name, datapoints)
    print("Benchmark finished\n")


def result_to_csv(alg_name: str, results: list[list[str, str, int, int, int, float]]):
    df = pd.DataFrame(results, columns=[
                      "alg_name", "n", "n_threads", "extern_iter", "begin_time", "time"])
    # print(df)

    filename = 'results.csv'
    df.to_csv(filename, mode='a', index=False,
              header=(not os.path.exists(filename)))



executables_folder = "install/bin/"
for executable in Path(executables_folder).iterdir():
    run_benchmark(str(executable))
