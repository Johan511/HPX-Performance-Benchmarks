import pandas as pd
import seaborn as sns
from pathlib import Path
import numpy as np
import matplotlib
import scipy
import matplotlib.pyplot as plt

def plot_sequence(data: pd.DataFrame):
    sns.set_style("whitegrid")

    alg_name = data["alg_name"].iloc[0]

    data["Total time elapsed (s)"] = data["begin_time"]/1000
    data["Algorithm execution time (ms)"] = data["time"]

    data = data[(data["extern_iter"].isin([1]))]
    # data = data.reset_index()

    fig, ax = plt.subplots(figsize=(20, 5))

    sns.scatterplot(data=data, x="Total time elapsed (s)", y="Algorithm execution time (ms)", s=6, ax=ax)
    # sns.lineplot(data=data, x="Total time elapsed (s)", y="Algorithm execution time (ms)", ax=ax)


    # data = data[(data["time"] < data["time"].quantile(0.995))
    #  & (data["time"] > data["time"].quantile(0.005))
    #  ]

    ax.set(ylim=(data["time"].min(), data["time"].quantile(0.99)))
    ax.xaxis.grid(True, which='minor')

    savepath = Path("plots")
    savepath.mkdir(parents=True, exist_ok=True)
    filename = savepath.as_posix() + "/" + alg_name + ".png"
    plt.savefig(filename, dpi=140)



def plot_single_alg(data: pd.DataFrame):
    alg_name = data["alg_name"].iloc[0]

    # # make speedup column
    # reference_data = data[data["n_threads"] == 1].copy()
    # reference_data["time_inv"] = reference_data["time"].transform(
    #     lambda x: 1/x).copy()
    # reference_avg = 1 / (reference_data.groupby("n")["time_inv"].mean())
    # data = data.merge(reference_avg.rename("ref_avg"), on="n")
    # data["speedup"] = data["ref_avg"]/data["time"]

    print(data)
    plt.clf()
    # fig, ax = plt.subplots(figsize=(8, 10))

    # sns.lineplot(x='n', y='time', hue='extern_iter', data=data, ax=ax, errorbar=None)

    # sns.scatterplot(x="n", y="time", data=data,
    #                 hue="extern_iter",
    #                 legend=None,
    #                 alpha=0.8,
    #                 s=4,
    #                 ax=ax)

    data = data[(data["time"] < data["time"].quantile(0.995))
     & (data["time"] > data["time"].quantile(0.005))
     ]

    # data = data[(data["extern_iter"].isin([2,5]))]

    # ax = sns.catplot(y='time', x='extern_iter', data=data,
    # #  kind="swarm"
    #  )
    
    # ax = sns.scatterplot(y='time', x='extern_iter', data=data, s=1
    # #  kind="swarm"
    #  )
    
    ax = sns.kdeplot( x='time', hue='extern_iter', data=data, 
    # cumulative=True,
    common_norm=False, common_grid=True,
    # binwidth=0.02
    )
    

    
    for name, group in data.groupby("extern_iter"):
        boot_result = scipy.stats.bootstrap((group["time"],), np.median)
        low, high = boot_result.confidence_interval
        ax.axvline(x=group["time"].median(), ls = "--", lw=0.8)
        ax.axvline(x=low, ls = "--", lw=0.5)
        ax.axvline(x=high, ls = "--", lw=0.5)

    
    # ax.set_ylabel("speedup (relative to seq)")
    # ax.set_ylabel("time (ms)")


    # ax.set_yscale("log")
    # ax.set_xscale("log")
    # ax.set_xlim([10**4, 10**8])
    # ax.set(ylim=(0, data["time"].quantile(0.99)))
    # ax.set_ylim([0, data["time"].quantile(0.9)])

    # ax.set_title("Speedup of '" + alg_name)

    savepath = Path("plots")
    savepath.mkdir(parents=True, exist_ok=True)
    filename = savepath.as_posix() + "/" + alg_name + ".png"
    plt.savefig(filename, dpi=140)


data = pd.read_csv("results.csv")

groups = data.groupby("alg_name")
for name, df in groups:
    alg_name = df["alg_name"].iloc[0]

    print("Plotting ", alg_name)
    # plot_single_alg(df)
    plot_sequence(df)

