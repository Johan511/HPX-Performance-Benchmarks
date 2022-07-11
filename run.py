import os
from pathlib import Path
import shutil
import subprocess
from progress.bar import Bar


def run_strong_scaling(executable_path: Path, n, runs=10):
    # delete conflicting csv file if it exists
    if os.path.exists(executable_path.with_suffix(".csv")):
        os.remove(executable_path.with_suffix(".csv"))

    cpu_count = os.cpu_count()
    print("Starting strong scaling test (" + executable_path.name + "):")
    print("n = ", n)
    progress_bar = Bar('Processing', max=cpu_count)

    for cores in range(1, cpu_count+1):
        subprocess.run([
            executable_path, str(n), str(runs), "--hpx:threads="+str(cores)
        ])
        progress_bar.next()
    progress_bar.finish()
    print("Test finished\n")

    executable_name = executable_path.with_suffix("").name
    csv_file_name = executable_path.with_suffix(".csv").name
    save_path = "./results/strong_scaling/" + executable_name + "/"
    save_name = executable_name + " n=" + str(n) + ".csv"

    Path(save_path).mkdir(parents=True, exist_ok=True)
    shutil.move(csv_file_name, save_path + save_name)


folder = Path("install/bin/")

print("Found executables: ", [
    item.with_suffix("").name for item in folder.iterdir()])

executables = [file for file in folder.iterdir() if file.suffix != ".dll"]

# print(executables)
for executable in executables:

    if os.access(executable, os.X_OK):
        print(executable, " is executable")

    csv_path = executable.with_suffix(".csv").name
    print("csv_path: ", csv_path)
    for n in [10**2, 10**3, 10**4, 10**5, 10**6]:
        iters = max(1, 10**4/n)
        run_strong_scaling(executable, n, iters)
