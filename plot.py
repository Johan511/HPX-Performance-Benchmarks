import pandas as pd
import seaborn as sns
from pathlib import Path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def plot_scatter(csv_path: Path):
    raw_data = pd.read_csv(csv_path)

    # # select range of data
    # raw_data.drop(raw_data[(raw_data["n"] < 10**2)
    #               | (raw_data["n"] > 10**7)].index, inplace=True)

    groups = raw_data.groupby("alg_name")
    for name, df in groups:
        print("Plotting ", df["alg_name"].iloc[0])
        plot_single_alg(df)


def plot_single_alg(data: pd.DataFrame):
    alg_name = data["alg_name"].iloc[0]
    # make speedup column
    seq_data = data[data["impl"] == "STD_SEQ"]
    # print(seq_data)

    seq_mean = seq_data.groupby("n").mean()["time"].rename("seq_avg")
    print(seq_mean)
    data = data.merge(seq_mean, on="n")
    data["speedup"] = data["seq_avg"]/data["time"]

    # select chunk sizes to be plotted
    data.drop(
        data[~(
            (data["impl"].isin(["HPX_PAR_SCS", "HPX_PAR_SCHED_EXEC"]))
            & (data["chunks"].isin([160])))

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
                    hue=data[["impl", "chunks"]].apply(tuple, axis=1),
                    # hue="chunks",
                    legend="full",
                    # palette=palette,
                    alpha=0.8,
                    s=4,
                    ax=ax)

    sns.lineplot(x="n", y="speedup", data=data,
                 hue=data[["impl", "chunks"]].apply(tuple, axis=1),
                 legend=None,
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

    ax.set_title(
        "Speedup of '" + alg_name + "'")

    savepath = Path("plots/" + alg_name)
    savepath.mkdir(parents=True, exist_ok=True)
    plt.savefig(savepath.as_posix() + "/" + alg_name + ".png", dpi=140)


plot_scatter(Path("results.csv"))
