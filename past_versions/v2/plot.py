import math
import pandas as pd
import seaborn as sns
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def plot_scatter(csv_path: Path):
    raw_data = pd.read_csv(csv_path)
    raw_data.drop(raw_data[raw_data["alg_name"].str.contains(
        "hpx_seq")].index, inplace=True)
    raw_data.drop(raw_data[(raw_data["n"] <= 10**2)
                  | (raw_data["n"] >= 10**9)].index, inplace=True)
    # remove stupid naming
    raw_data["alg_name"] = raw_data["alg_name"].str.removeprefix(
        "executables/")
    print(raw_data)

    copy_if_data = raw_data[raw_data["alg_name"].str.contains("copy_if/")]
    copy_if_heavy_data = raw_data[raw_data["alg_name"].str.contains(
        "copy_if-heavy/")]

    for alg_name, data in [("copy_if", copy_if_data),
                           ("copy_if-heavy", copy_if_heavy_data)]:

        # make speedup column
        seq_data = data[data["alg_name"].str.contains("seq")]
        seq_mean = seq_data.groupby("n").mean()["time"].rename("seq_avg")
        data = data.merge(seq_mean, on="n")
        data["speedup"] = data["seq_avg"]/data["time"]

        # make normalized column
        mean = data.groupby(["n", "alg_name"]).mean()["time"].rename("mean")
        data = data.merge(mean, on="n")
        data["normalized"] = data["time"]/data["mean"]

        data = data[data["alg_name"].str.endswith(
            ("hpx_par",
             #  "hpx_par_panos2",
             "hpx_par_panos",
             #  "hpx_par_panos_sync",
             #  "hpx_par_panos2_1",
             "std_par",
             "std_seq"))]
        # data = data[~data["alg_name"].str.contains("hpx_seq")]
        averages = data.groupby(["n", "alg_name"]).mean()

        print(data)
        print(averages)

        # make group averages for plotting line

        palette = sns.color_palette()

        fig, ax = plt.subplots(figsize=(12, 8))
        # sns.scatterplot(x="n", y="speedup", data=data, hue="alg_name",
        #                 # palette=palette,
        #                 legend=False,
        #                 s=4, alpha=0.8, ax=ax)

        sns.lineplot(x="n", y="speedup", data=data,
                     # palette=palette,
                     hue="alg_name",  # legend=False,
                     ax=ax)

        # ax.set_ylabel("speedup relative to seq")
        ax.set_ylabel("speedup (relative to sequential)")

        # # ax.set_yscale("log")
        ax.set_xscale("log")
        # ax.set_ylim([0, 18])

        savepath = Path("plots/scatter/")
        savepath.mkdir(parents=True, exist_ok=True)
        plt.savefig(savepath.as_posix() + "/" + alg_name + ".png")


def plot_violin(csv_path: Path):
    raw_data = pd.read_csv(csv_path)

    # remove stupid naming
    raw_data["alg_name"] = raw_data["alg_name"].str.removeprefix(
        "executables/")

    copy_if_data = raw_data[raw_data["alg_name"].str.contains("copy_if/")]
    copy_if_heavy_data = raw_data[raw_data["alg_name"].str.contains(
        "copy_if-heavy/")]

    for alg_name, alg_data in [("copy_if", copy_if_data),
                               ("copy_if-heavy", copy_if_heavy_data)]:
        groups = alg_data.groupby("n")
        # mean, std = groups.transform("mean"), groups.transform("std")
        # normalized = (data[mean.columns] - mean) / std

        for n, data in groups:
            palette = sns.diverging_palette(
                250, 30, l=65, center="dark", as_cmap=True)

            fig, ax = plt.subplots(figsize=(12, 8))
            ax = sns.violinplot(
                x="n", y="time",
                data=data, palette=palette,
                hue="alg_name", inner="points")

            ax.set_ylabel("time (ms)")
            ax.set_ylim(bottom=0)

            savepath = Path("plots_/violin/" + alg_name)
            savepath.mkdir(parents=True, exist_ok=True)
            plt.savefig(savepath.as_posix() + "/n=" +
                        str(n) + ".png")


# plot_violin(Path("results_old.csv"))
plot_scatter(Path("results.csv"))
