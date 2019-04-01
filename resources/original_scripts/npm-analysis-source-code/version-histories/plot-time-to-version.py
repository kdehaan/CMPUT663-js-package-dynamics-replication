import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def color_from_mp(mp):
    (m,p) = mp
    m = int(m)
    p = int(p)
    if m == 0 and p == 0:
        return "blue"
    elif p == 0:
        return "red"
    else:
        return "green"

if __name__ == "__main__":
    input_file = sys.argv[0].replace("plot-", "data-").replace(".py", ".dat")

    frame = pd.read_csv(input_file)

    width = 5.0

    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rc("text", usetex=True)
    plt.rc("figure", figsize=(width, 3.5*width/4.0))
    plt.rc("axes", linewidth=0.5)

    versions = frame["linearized"]
    months   = frame["avg_time"] / 60 / 60 / 24 / 30.5

    color_in = zip(list(frame["minor"]), list(frame["patch"]))
    colors = map(color_from_mp, color_in)

    plt.scatter(versions, months, marker='+', c=colors)

    axes = plt.gca()

    axes.set_xlabel("Version number")
    axes.set_xlim([ 0, 7 ])
    plt.xticks(range(0,8), map(lambda n: "%d.0.0" % n, range(0,8)), rotation=45, ha='right')

    axes.set_ylabel("Months")
    axes.set_ylim([ 0, 13 ])
    axes.xaxis.grid(True, which='major')

    # plt.xticks(range(0,11))

    plt.tight_layout()

    # plt.show()

    plot_file = sys.argv[0].replace("plot-", "").replace(".py", ".pdf") 
    plt.savefig(plot_file, format="pdf")
