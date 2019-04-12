import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    input_file = sys.argv[0].replace("plot-", "data-").replace(".py", ".dat")

    frame = pd.read_csv(input_file)

    print frame

    width = 5.0
    
    bar_width = 0.31

    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rc("text", usetex=True)
    plt.rc("figure", figsize=(width, 3.0*width/4.0))
    plt.rc("axes", linewidth=0.5)

    plt.bar(frame["number"] - 1.5 * bar_width, frame["major"], bar_width, color="blue")
    plt.bar(frame["number"] - 0.5 * bar_width, frame["minor"], bar_width, color="red")
    plt.bar(frame["number"] + 0.5 * bar_width, frame["patch"], bar_width, color="green")

    axes = plt.gca()
    axes.set_xlabel("Number")
    axes.set_xlim([ -2 * bar_width, 9 + 2 * bar_width ])
    plt.xticks(range(0,10), range(0,10))
    # axes.set_ylim([ 0.5, 5.5 ])

    axes.set_ylabel("Frequency")
    axes.set_yscale('log')

    axes.yaxis.grid(True, which='major')

    # plt.xticks(range(0,11))

    plt.tight_layout()

    # plt.show()

    plot_file = sys.argv[0].replace("plot-", "").replace(".py", ".pdf") 
    plt.savefig(plot_file, format="pdf")
