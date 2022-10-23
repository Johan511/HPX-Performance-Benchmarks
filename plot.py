import pandas as pd
import seaborn as sns
from pathlib import Path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def plot_scatter(csv_path: Path):
    raw_data = pd.read_csv(csv_path)

    # select range of data
    raw_data.drop(raw_data[(raw_data["n"] < 10**2)
                  | (raw_data["n"] > 10**7)].index, inplace=True)

    print(raw_data)

    # select what to keep
    raw_data = raw_data[raw_data["alg_name"].str.contains(
        "transform/")]

    raw_data = raw_data[raw_data["alg_name"].str.contains(
        "hpx_par_scs|hpx_par_sched-exec|hpx_par_fork-join|std_seq")]

    # remove prefix naming
    raw_data["alg_name"] = raw_data["alg_name"].str.removeprefix(
        "executables/")

    print(raw_data)

    # # select implementation to be plotted
    # to_keep = [
    #     "copy_if/std_seq",
    #     "copy_if/hpx_par",
    #     # "copy_if/hpx_par_seqf3",
    #     # "copy_if/hpx_par_seqf3",
    # ]

    # raw_data.drop(
    #     raw_data[~raw_data["alg_name"].isin(to_keep)].index, inplace=True)

    data = raw_data

    # make speedup column
    seq_data = data[data["alg_name"].str.contains("std_seq")]
    print(seq_data)

    seq_mean = seq_data.groupby("n").mean()["time"].rename("seq_avg")
    print(seq_mean)
    data = data.merge(seq_mean, on="n")
    data["speedup"] = data["seq_avg"]/data["time"]

    # drop seq algorithm
    # data.drop(data[data["alg_name"].str.contains(
    #     "std_seq")].index, inplace=True)

    # select chunk sizes to be plotted
    data.drop(
        data[~((data["alg_name"] == ("transform/hpx_par_sched-exec"))
               & (data["chunks"] == 40))
             & ~((data["alg_name"] == ("transform/hpx_par_sched-exec"))
                 & (data["chunks"] == 160))
             & ~((data["alg_name"] == ("transform/hpx_par_sched-exec"))
                 & (data["chunks"] == 320))

             #  & ~((data["alg_name"] == ("remove/my_hpx_par_scs"))
             #      & (data["chunks"] == 320))
             #  & ~((data["alg_name"] == ("remove/hpx_par_scs"))
             #      & (data["chunks"] == 320))
             #  & ~((data["alg_name"].str.contains("/my_hpx_par_scs"))
             #      & (data["chunks"] == 40))
             #  & ~((data["alg_name"].str.contains("/std_seq")))
             ].index, inplace=True)

    # data = data.sort_values(by=["alg_name", "n"], ascending=[False, False])
    fig, ax = plt.subplots(figsize=(14, 8))

    # palette = sns.diverging_palette(
    #     250, 30, l=65, center="dark", as_cmap=True)

    sns.scatterplot(x="n", y="speedup", data=data,
                    hue=data[["alg_name", "chunks"]].apply(tuple, axis=1),
                    # hue="chunks",
                    legend="full",
                    # palette=palette,
                    alpha=0.8,
                    s=4,
                    ax=ax)

    sns.lineplot(x="n", y="speedup", data=data,
                 hue=data[["alg_name", "chunks"]].apply(tuple, axis=1),
                 #  legend=None,
                 #  palette=palette,
                 ci=None,
                 ax=ax)

    sns.lineplot(x=[data["n"].min(), data["n"].max()],
                 y=[1, 1], ax=ax, color="black", linestyle="dashed")

    ax.set_ylabel("speedup (relative to seq)")

    # ax.set_yscale("log")
    ax.set_xscale("log")
    # ax.set_ylim(bottom=0)
    # ax.set_ylim([0, 6])

    alg_name = "transform"
    ax.set_title(
        "Speedup of '" + alg_name + "'")

    savepath = Path("plots/scatter/")
    savepath.mkdir(parents=True, exist_ok=True)
    plt.savefig(savepath.as_posix() + "/" + alg_name + ".png", dpi=140)


plot_scatter(Path("results.csv"))
