import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


def plot_speedup_test(csv_path: Path):
    data = pd.read_csv(csv_path)

    plot_title = "Speedup Test\n" + csv_path.stem

    speedup_data = pd.DataFrame()
    speedup_data["hpx_par"] = data["hpx_seq_time"]/data["hpx_par_time"]
    speedup_data["hpx_seq"] = data["hpx_seq_time"]/data["hpx_seq_time"]
    speedup_data["vector_size"] = data["vector_size"]

    fig, ax = plt.subplots()
    speedup_data.plot(x="vector_size", title=plot_title, ax=ax)
    ax.set_xlabel("Vector size")
    ax.set_ylabel("Speedup (relative to seq)")
    ax.set_xscale("log")

    ax.legend()

    img_path = csv_path.parent / Path("./plots/")
    img_path.mkdir(parents=True, exist_ok=True)

    plt.savefig(img_path / Path(csv_path.stem + ".png"))
    plt.show()


def plot_weak_scaling(csv_path: Path):
    data = pd.read_csv(csv_path)

    plot_title = "Weak Scaling\n" + csv_path.stem

    max_cores = data["threads"].max()

    eff_data = pd.DataFrame()
    eff_data["hpx_par"] = (data["hpx_par_time"] /
                           data["hpx_par_time"][0]).apply(lambda x: 1/x)
    eff_data["hpx_seq"] = (data["hpx_seq_time"] /
                           data["hpx_seq_time"][0]).apply(lambda x: 1/x)
    eff_data["threads"] = data["threads"]

    fig, ax = plt.subplots()
    # ax.hlines(data["hpx_par_time"][0], data["threads"])
    eff_data.plot(x="threads", title=plot_title, ax=ax)
    ax.hlines(y=1, xmin=1, xmax=max_cores,
              linestyle='dashed', label="ideal efficiency", color="green")
    ax.set_ylabel("Efficiency")
    ax.set_xlabel("Cores")
    ax.legend()

    img_path = csv_path.parent / Path("./plots/")
    img_path.mkdir(parents=True, exist_ok=True)

    plt.savefig(img_path / Path(csv_path.stem + ".png"))
    plt.show()


def plot_threads_vs_time(csv_path: Path):
    data = pd.read_csv(csv_path)
    data["std_seq_time"] *= 10**(-6)
    data["hpx_seq_time"] *= 10**(-6)
    data["hpx_par_time"] *= 10**(-6)

    plot_title = csv_path.stem

    fig, ax = plt.subplots()
    ax.set_title(plot_title)
    data.plot(x="threads", y="std_seq_time", ax=ax)
    data.plot(x="threads", y="hpx_seq_time", ax=ax)
    data.plot(x="threads", y="hpx_par_time", ax=ax)

    ax.set_xlabel("Cores")
    ax.set_ylabel("Time (ms)")
    ax.legend()

    img_path = csv_path.parent / Path("./plots/time/")
    img_path.mkdir(parents=True, exist_ok=True)

    plt.savefig(img_path / Path(csv_path.stem + ".png"))
    plt.show()


def plot_strong_scaling(csv_path: Path):
    data = pd.read_csv(csv_path)

    plot_title = "Strong Scaling\n" + csv_path.stem

    speedup_data = pd.DataFrame()
    speedup_data["hpx_par"] = data["hpx_seq_time"]/data["hpx_par_time"]
    speedup_data["hpx_seq"] = data["hpx_seq_time"]/data["hpx_seq_time"]
    speedup_data["threads"] = data["threads"]

    fig, ax = plt.subplots()
    speedup_data.plot(x="threads", title=plot_title, ax=ax)
    ax.set_xlabel("Cores")
    ax.set_ylabel("Speedup (relative to seq)")
    ax.plot(data["threads"],
            linestyle='dashed', label="ideal speedup", color="green")
    ax.legend()

    img_path = csv_path.parent / Path("./plots/")
    img_path.mkdir(parents=True, exist_ok=True)

    plt.savefig(img_path / Path(csv_path.stem + ".png"))
    plt.show()


folder_strong_scaling = Path("./results/strong_scaling/")

for subfolder in folder_strong_scaling.iterdir():
    for file in subfolder.iterdir():
        if (file.suffix == ".csv"):
            print("Plotting CSV File: ", file)
            plot_threads_vs_time(file)
            plot_strong_scaling(file)


folder_weak_scaling = Path("./results/weak_scaling/")

for subfolder in folder_weak_scaling.iterdir():
    for file in subfolder.iterdir():
        if (file.suffix == ".csv"):
            print("Plotting CSV File: ", file)
            plot_threads_vs_time(file)
            plot_weak_scaling(file)


folder_speedup_test = Path("./results/speedup_test/")

for subfolder in folder_speedup_test.iterdir():
    for file in subfolder.iterdir():
        if (file.suffix == ".csv"):
            print("Plotting CSV File: ", file)
            plot_speedup_test(file)
