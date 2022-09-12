import math
import pandas as pd
import seaborn as sns
from pathlib import Path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def plot_scatter(csv_path: Path):
    raw_data = pd.read_csv(csv_path)

    # select range of data
    raw_data.drop(raw_data[(raw_data["n"] <= 10**4)
                  | (raw_data["n"] >= 10**9)].index, inplace=True)

    # keep results only from copy_if algorithm
    raw_data = raw_data[raw_data["alg_name"].str.contains(
        "install/copy_if/")]

    # remove prefix naming
    raw_data["alg_name"] = raw_data["alg_name"].str.removeprefix(
        "install/copy_if/")

    # select implementation to be plotted
    to_keep = [
        "hpx_par",
        # "hpx_par_scs",
        # "std_par"
        "std_seq"]

    raw_data.drop(
        raw_data[~raw_data["alg_name"].isin(to_keep)].index, inplace=True)

    print(raw_data)

    copy_if_data = raw_data

    for alg_name, data in [("copy_if", copy_if_data)]:

        # make speedup column
        seq_data = data[data["alg_name"].str.contains("std_seq")]
        print(seq_data)
        seq_mean = seq_data.groupby("n").mean()["time"].rename("seq_avg")
        data = data.merge(seq_mean, on="n")
        data["speedup"] = data["seq_avg"]/data["time"]

        print(data["speedup"])

        # drop seq algorithm
        data.drop(data[data["alg_name"].str.contains(
            "std_seq")].index, inplace=True)

        print(data.groupby("chunks").mean())
        # data["chunks"] = data["n"]/(data["chunk_size"])

        print(data["chunks"])

        # select chunk sizes to be plotted
        data.drop(
            data[~((data["alg_name"] == "hpx_par_scs")
                   & (data["chunks"] == 80))
                 & ~((data["alg_name"] == "hpx_par_scs")
                     & (data["chunks"] == 160))
                 & ~((data["alg_name"] == "hpx_par")
                     & (data["chunks"] == 160))
                 ].index, inplace=True)

        fig, ax = plt.subplots(figsize=(10, 6))

        palette = sns.diverging_palette(
            250, 30, l=65, center="dark", as_cmap=True)

        sns.scatterplot(x="n", y="speedup", data=data,
                        hue="alg_name",
                        # hue="chunks",
                        legend="full",
                        # palette=palette,
                        alpha=0.8,
                        s=4,
                        ax=ax)

        sns.lineplot(x="n", y="speedup", data=data,
                     hue="alg_name",
                     # hue="chunks",
                     legend=None,
                     #  palette=palette,
                     ci=None,
                     ax=ax)

        ax.set_ylabel("speedup (relative to sequential)")

        ax.set_xscale("log")
        ax.set_ylim(bottom=0)
        # ax.set_ylim([0, 15])

        ax.set_title(
            "Speedup of parallel 'copy_if'")

        savepath = Path("plots/scatter/")
        savepath.mkdir(parents=True, exist_ok=True)
        plt.savefig(savepath.as_posix() + "/" + alg_name + ".png", dpi=140)


plot_scatter(Path("results.csv"))
