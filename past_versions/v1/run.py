import math
import os
from pathlib import Path
import shutil
import subprocess
from progress.bar import Bar
import numpy as np


def run_speedup_test(executable_path: Path, cores, max_n):
    # delete conflicting csv file if it exists
    if os.path.exists(executable_path.stem+".csv"):
        os.remove(executable_path.stem+".csv")

    print("Starting speedup test (" + executable_path.name + "):")
    print("cores = ", cores)

    n_values = [int(n) for n in np.logspace(3, math.log10(max_n), 50)]

    progress_bar = Bar('Processing', max=len(n_values))

    for n in n_values:
        iterations = int(max(1, min(10**7/n, 10**4)))
        subprocess.run([
            executable_path, str(n), str(
                iterations), "--hpx:threads="+str(cores)
        ])
        progress_bar.next()
    progress_bar.finish()
    print("Test finished\n")

    executable_name = executable_path.with_suffix("").name
    csv_file_name = executable_path.with_suffix(".csv").name
    save_path = "./results/speedup_test/" + executable_name + "/"
    save_name = executable_name + \
        " (cores=" + str(cores) + ").csv"

    Path(save_path).mkdir(parents=True, exist_ok=True)
    shutil.move(csv_file_name, save_path + save_name)


def run_weak_scaling(executable_path: Path, max_n):
    # delete conflicting csv file if it exists
    if os.path.exists(executable_path.stem+".csv"):
        os.remove(executable_path.stem+".csv")

    cpu_count = os.cpu_count()
    print("Starting weak scaling test (" + executable_path.name + "):")
    print("max_n = ", max_n)
    progress_bar = Bar('Processing', max=cpu_count)

    for cores in range(1, cpu_count+1):
        n = max_n*cores/cpu_count
        iterations = int(max(1, min(10**7/n, 10**4)))
        subprocess.run([
            executable_path, str(n), str(
                iterations), "--hpx:threads="+str(cores)
        ])
        progress_bar.next()
    progress_bar.finish()
    print("Test finished\n")

    executable_name = executable_path.with_suffix("").name
    csv_file_name = executable_path.with_suffix(".csv").name
    save_path = "./results/weak_scaling/" + executable_name + "/"
    save_name = executable_name + \
        " (max_n=10^" + str(int(math.log10(max_n))) + ").csv"

    Path(save_path).mkdir(parents=True, exist_ok=True)
    shutil.move(csv_file_name, save_path + save_name)


def run_strong_scaling(executable_path: Path, n):
    # delete conflicting csv file if it exists
    if os.path.exists(executable_path.stem+".csv"):
        os.remove(executable_path.stem+".csv")

    cpu_count = os.cpu_count()
    print("Starting strong scaling test (" + executable_path.name + "):")
    print("n = ", n)
    progress_bar = Bar('Processing', max=cpu_count)

    iterations = max(1, min(10**7/n, 10**4))
    for cores in range(1, cpu_count+1):
        subprocess.run([
            executable_path, str(n), str(
                iterations), "--hpx:threads="+str(cores)
        ])
        progress_bar.next()
    progress_bar.finish()
    print("Test finished\n")

    executable_name = executable_path.with_suffix("").name
    csv_file_name = executable_path.with_suffix(".csv").name
    save_path = "./results/strong_scaling/" + executable_name + "/"
    save_name = executable_name + " (n=10^" + str(int(math.log10(n))) + ").csv"

    Path(save_path).mkdir(parents=True, exist_ok=True)
    shutil.move(csv_file_name, save_path + save_name)


folder = Path("install/bin/")

print("Found executables: ", [
    item.with_suffix("").name for item in folder.iterdir()])

executables = [file for file in folder.iterdir() if file.suffix != ".dll"]

# print(executables)
for executable in executables:

    for n in [10**3, 10**4, 10**5, 10**6, 10**7, 10**8]:
        run_weak_scaling(executable, n)
        run_strong_scaling(executable, n)

    cores_list = [2**k for k in range(0, int(math.log2(os.cpu_count())) + 1)]
    cores_list.append(os.cpu_count())
    for cores in cores_list:
        run_speedup_test(executable, cores, 10**8)
