import math
import pandas as pd
import seaborn as sns
from pathlib import Path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def plot_scatter(csv_path: Path):
    raw_data = pd.read_csv(csv_path)
    # raw_data.drop(raw_data[raw_data["alg_name"].str.contains(
    #     "hpx_seq")].index, inplace=True)
    raw_data.drop(raw_data[(raw_data["n"] <= 10**4)
                  | (raw_data["n"] >= 10**9)].index, inplace=True)

    raw_data = raw_data[raw_data["alg_name"].str.contains(
        "copy_if/")]
    # remove stupid naming
    raw_data["alg_name"] = raw_data["alg_name"].str.removeprefix(
        "executables/copy_if/")
    raw_data.drop(
        raw_data[raw_data["alg_name"].str.contains("debug")].index, inplace=True)

    to_keep = [
        # "hpx_par_default_scs10cores",  "hpx_par_default_scs4cores",
        # "hpx_par_scs_with_hint",
        # "hpx_par_scs_with_hint_seqf2",
        # "hpx_par_scs_hint_seqf2_stealing",
        # "hpx_par_scs_numa_hint_seqf2",
        # "hpx_par_scs_numa_hint_seqf2_v2",
        "hpx_par_default",
        # "hpx_par_default_scs",
        "std_seq"]
    raw_data.drop(
        raw_data[~raw_data["alg_name"].isin(to_keep)].index, inplace=True)

    print(raw_data)
    # copy_if_data = raw_data[raw_data["alg_name"].str.contains(
    #     "copy_if/hpx_par_scs|copy_if/std_seq")]
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

        # # make normalized column
        # mean = data.groupby(["n"]).mean()["time"].rename("mean")
        # data = data.merge(mean, on="n")
        # data["normalized"] = data["time"]/data["mean"]

        print(data.groupby("chunks").mean())
        # data["chunks"] = data["n"]/(data["chunk_size"])

        print(data["chunks"])
        # cmap = sns.color_palette("icefire", as_cmap=True)
        # norm=matplotlib.colors.LogNorm(vmin=data["normalized"].min(), vmax=data["normalized"].max())

        # data.drop(
        #     data[~((data["alg_name"] == "hpx_par_default_scs")
        #            & (data["chunks"] == 80))
        #          & ~((data["alg_name"] == "hpx_par_default_scs")
        #              & (data["chunks"] == 160))
        #          & ~((data["alg_name"] == "hpx_par_default")
        #              & (data["chunks"] == 160))
        #          ].index, inplace=True)

        # select chunk sizes

        data.drop(data[~data["chunks"].isin(
            [
                # 20,
                # 40,
                # 80,
                160,
                # 320,
                # 640,
                # 1280
            ])].index, inplace=True)

        # hue_norm = matplotlib.colors.LogNorm(
        #     vmin=80, vmax=320)
        hue_norm = matplotlib.colors.LogNorm(
            vmin=data["chunks"].min(), vmax=data["chunks"].max())

        fig, ax = plt.subplots(figsize=(10, 6))

        palette = sns.diverging_palette(
            250, 30, l=65, center="dark", as_cmap=True)

        sns.scatterplot(x="n", y="speedup", data=data,
                        hue="alg_name",
                        # hue="chunks",
                        legend="full",
                        # palette=palette,
                        # hue_norm=hue_norm,
                        # norm=norm,
                        # cmap=cmap,
                        alpha=0.8,
                        s=4,
                        ax=ax)

        sns.lineplot(x="n", y="speedup", data=data,
                     hue="alg_name",
                     # hue="chunks",

                     legend=None,

                     #  palette=palette,
                     ci=None,
                     # err_style="bars",
                     #  hue_norm=hue_norm,
                     # norm=norm,
                     ax=ax)
        # cache lines
        # sns.lineplot(x=[32000/4, 32000/4], y=[0, 12], ax=ax, color="black")
        # sns.lineplot(x=[1024000/4, 1024000/4], y=[0, 12], ax=ax, color="black")
        # sns.lineplot(x=[16896000/4, 16896000/4],
        #              y=[0, 12], ax=ax, color="black")

        ax.set_ylabel("speedup (relative to sequential)")

        # # ax.set_yscale("log")
        ax.set_xscale("log")
        # ax.set_ylim([0, 15])
        ax.set_ylim(bottom=0)

        ax.set_title(
            "Speedup of parallel 'copy_if'\n(40 core CPU, 160 chunks)")

        savepath = Path("plots/scatter/")
        savepath.mkdir(parents=True, exist_ok=True)
        plt.savefig(savepath.as_posix() + "/" + alg_name + ".png", dpi=140)
        data.to_csv("formatted_data.csv")


plot_scatter(Path("results.csv"))
