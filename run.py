
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
        # __runs only hpx_par__
        if "hpx_par" == executable.stem:
            continue
        benchmark_chunks(executable)


def benchmark_chunks(executable_path: Path):
    alg_name = executable_path.as_posix()
    print("\nStarting benchmark: (" + alg_name + "):")

    # We create a list of logarithmically-spaced numbers. Those will
    # be the vector sizes for which the algorithm will be benchmarked.
    n_datapoints = 20
    n_min, n_max = [10**4, 10**7]

    n_list = [int(n) for n in np.logspace(
        math.log10(n_min), math.log10(n_max), n_datapoints)]

    cores = multiprocessing.cpu_count()
    chunks_list = [80, 160, 320]
    # chunks_list = [160]
    # chunks_list = [pd.NA]

    for n in pb.progressbar(n_list):
        results = list()
        for chunks in chunks_list:
            iterations = 20  # int(max(5, min(10**10/n, 10**4)))
            chunk_size = math.ceil(n / chunks)
            # chunk_size = pd.NA
            command = [executable_path, str(iterations),
                       str(n), str(chunk_size),
                       # "--hpx:threads=4"
                       ]

            # Run the algorithm. It will return a collection of floats, each float
            # representing elapsed time(ns) for each algorithm invocation.
            ret = subprocess.run(command, capture_output=True, check=False)

            if (ret.returncode != 0):
                print("\nExecution error:\n")
                print(ret)

            # convert output to list of tuples(alg_name, vector_size, time in ms)
            datapoints = [[alg_name, n, chunk_size, float(dt)/(10**6), chunks]
                          for dt in ret.stdout.splitlines()]

            # print("n = ", n, " :  ", datapoints, " ms")
            results.extend(datapoints)
        result_to_csv(alg_name, results)
    print("Benchmark finished\n")


def result_to_csv(alg_name: str, results: list[list[str, int, int, float]]):
    df = pd.DataFrame(results, columns=[
                      "alg_name", "n", "chunk_size", "time", "chunks"])
    # print(df)

    filename = 'results.csv'
    df.to_csv(filename, mode='a', index=False,
              header=(not os.path.exists(filename)))


def vtune_run_folder(exec_folder_path: Path, vtune_test_type: str, chunks: int):
    for executable in exec_folder_path.iterdir():
        # __select hpx_par executable:__
        if "hpx_par" not in executable.stem:
            continue
        vtune_run_exec(executable, vtune_test_type, chunks)


def vtune_run_exec(executable_path: Path, vtune_test_type: str, chunks: int):
    print("Starting test run (" + executable_path.as_posix() + "):")

    alg_name = executable_path.parts[1]
    alg_impl = executable_path.parts[2]

    print(alg_name, alg_impl)

    n_datapoints = 20
    n_min, n_max = [10**5, 10**7]
    n_list = [int(n) for n in np.logspace(
        math.log10(n_min), math.log10(n_max), n_datapoints)]

    for n in pb.progressbar(n_list):

        iterations = 100  # int(max(5, min(10**7/n, 10**4)))
        vtune_path = Path("/opt/intel/oneapi/vtune/latest/bin64/vtune")
        vtune_results_path = "./vtune_results/" + vtune_test_type + "/" + \
            alg_name + "/n=" + str(n) + "/" + alg_impl + "/"

        vtune_args = ["-collect " + vtune_test_type,
                      "-r " + vtune_results_path,
                      # "-start-paused",
                      #   "-knob sampling-and-waits=hw",
                      #   "-knob sampling-interval=1",
                      # "-knob stack-size=0",
                      "-finalization-mode=full"]

        chunk_size = math.ceil(n/chunks)
        command = [vtune_path, *vtune_args, executable_path, str(n),
                   str(iterations),
                   str(chunk_size),
                   "--hpx:ini=hpx.use_itt_notify!=1"]

        val = subprocess.run(command, capture_output=True, check=False)
        if (val.returncode != 0):
            print("Execution error:")
            print(val)

    print("Run finished\n")


folder = Path("install/")

print("Found algorithms: ", [
    item.with_suffix("").name for item in folder.iterdir()])

for subfolder in folder.iterdir():

    # select specific folder:
    if subfolder.stem != "copy_if":
        continue

    # vtune_run_folder(subfolder, "threading", 40)
    benchmark_folder(subfolder)
