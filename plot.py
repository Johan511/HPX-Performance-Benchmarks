import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


def plot_weak_scaling(csv_path: Path):
    data = pd.read_csv(csv_path)

    plot_title = csv_path.stem

    max_cores = data["threads"].max()

    eff_data = data[["hpx_seq_time", "hpx_par_time"]]
    eff_data /= eff_data.iloc[0]  # normalize to time of single core
    # inverse because we want T1core/Tncores
    eff_data = eff_data.apply(lambda x: 1/x)

    eff_data["threads"] = data["threads"]

    fig, ax = plt.subplots()
    # ax.hlines(data["hpx_par_time"][0], data["threads"])
    eff_data.plot(x="threads", title=plot_title, ax=ax)
    ax.hlines(y=1, xmin=1, xmax=max_cores, linestyle='dashed', label="ideal efficiency")
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

    plot_title = csv_path.stem

    seq_time = data["std_seq_time"][0]

    speedup_data = seq_time * \
        (data[["std_seq_time", "hpx_seq_time", "hpx_par_time"]]).apply(
            lambda x: 1/x)

    speedup_data["threads"] = data["threads"]

    fig, ax = plt.subplots()
    speedup_data.plot(x="threads", title=plot_title, ax=ax)
    ax.set_xlabel("Cores")
    ax.set_ylabel("Speedup (relative to seq)")
    ax.plot(data["threads"],
            linestyle='dashed', label="ideal speedup")
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
            # plot_threads_vs_time(file)
            # plot_strong_scaling(file)

folder_weak_scaling = Path("./results/weak_scaling/")
for subfolder in folder_weak_scaling.iterdir():
    for file in subfolder.iterdir():
        if (file.suffix == ".csv"):
            print("Plotting CSV File: ", file)
            plot_threads_vs_time(file)
            plot_weak_scaling(file)
