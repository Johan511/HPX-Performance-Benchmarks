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
    reference_data = data[data["impl"] == "STD_SEQ"]
    reference_avg = reference_data.groupby("n")["time"].mean()

    data_avg = data.groupby(["impl", "n"], as_index=False)["time"].mean()

    data_avg = data_avg.merge(reference_avg.rename("ref_time"), on="n")
    # print(reference_means)
    data_avg["speedup"] = data_avg["ref_time"]/data_avg["time"]

    # print(data_avg.to_string())

    fig, ax = plt.subplots(figsize=(14, 8))

    sns.lineplot(x='n', y='speedup', hue='impl', data=data_avg, ax=ax)

    sns.scatterplot(x="n", y="speedup", data=data_avg,
                    hue="impl",
                    legend=None,
                    alpha=0.8,
                    s=4,
                    ax=ax)

    ax.set_ylabel("speedup (relative to seq)")

    # ax.set_yscale("log")
    ax.set_xscale("log")
    # ax.set_xlim([10**4, 10**8])
    ax.set_ylim([0, data_avg["speedup"].max()])
    # ax.set_ylim([0, 5])

    ax.set_title(
        "Speedup of '" + alg_name)

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
