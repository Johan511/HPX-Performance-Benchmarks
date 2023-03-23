import pandas as pd
import seaborn as sns
from pathlib import Path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def plot_single_alg(data: pd.DataFrame):
    alg_name = data["alg_name"].iloc[0]
    print(data)

    # make speedup column
    reference_data = data[data["impl"] == "STD_SEQ"].copy()
    reference_data["time_inv"] = reference_data["time"].transform(
        lambda x: 1/x).copy()
    reference_avg = 1 / (reference_data.groupby("n")["time_inv"].mean())
    data = data.merge(reference_avg.rename("ref_avg"), on="n")
    data["speedup"] = data["ref_avg"]/data["time"]

    # print(data_avg.to_string())

    fig, ax = plt.subplots(figsize=(14, 8))

    sns.lineplot(x='n', y='speedup', hue='impl', data=data, ax=ax, errorbar=None)

    sns.scatterplot(x="n", y="speedup", data=data,
                    hue="impl",
                    legend=None,
                    alpha=0.8,
                    s=4,
                    ax=ax)

    ax.set_ylabel("speedup (relative to seq)")

    # ax.set_yscale("log")
    ax.set_xscale("log")
    # ax.set_xlim([10**4, 10**8])
    # ax.set_ylim([0, data_avg["speedup"].max()])

    ax.set_title("Speedup of '" + alg_name)

    savepath = Path("plots")
    savepath.mkdir(parents=True, exist_ok=True)
    filename = savepath.as_posix() + "/" + alg_name + ".png"
    plt.savefig(filename, dpi=140)


data = pd.read_csv("results.csv")

groups = data.groupby("alg_name")
for name, df in groups:
    alg_name = df["alg_name"].iloc[0]

    print("Plotting ", alg_name)
    plot_single_alg(df)
