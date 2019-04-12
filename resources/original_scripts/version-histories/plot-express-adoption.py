import datetime
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def month_range(year_from, year_to):
    for y in range(year_from, year_to):
        for m in range(1, 12):
            yield datetime.datetime(y, m, 1, 0, 0, 0, 0)

if __name__ == "__main__":
    input_file = sys.argv[0].replace("plot-", "data-").replace(".py", ".dat")

    frame = pd.read_csv(input_file)

    width = 10.0

    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rc("text", usetex=True)
    plt.rc("figure", figsize=(width, 1.5*width/4.0))
    plt.rc("axes", linewidth=0.5)

    timestamps = list(frame["ts"])
    versions   = list(frame["linearized"])

    def color_from_mp(mp):
        (m,p) = mp
        if m == 0 and p == 0:
            return "blue"
        elif p == 0:
            return "red"
        else:
            return "green"

    colors = map(color_from_mp, zip(list(frame["minor"]), list(frame["patch"])))

    areas = list(np.pi * (frame["frac"] * 17)**2)

    plt.scatter(timestamps, versions, s=areas, c=colors, alpha=0.5)

    months = list(month_range(2012, 2016))[0::5]
    print months

    axes = plt.gca()
    plt.xticks(map(lambda m: (m-datetime.datetime(1970,1,1)).total_seconds(), months), map(lambda m: m.strftime("%b %Y"), months))
    margin = 12 * 24 * 3600
    axes.set_xlim([ min(timestamps) - margin, max(timestamps) + margin])

    axes.set_ylabel("Version")
    axes.yaxis.grid(True, which='major')
    axes.set_ylim(2.9, 5.1)
    plt.yticks([3, 4, 5], ["3.0.0", "4.0.0", "5.0.0"])#range(0,8), map(lambda n: "%d.0.0" % n, range(0,8)), rotation=45, ha='right')

    plt.tight_layout()

    # plt.show()

    plot_file = sys.argv[0].replace("plot-", "").replace(".py", ".pdf") 
    plt.savefig(plot_file, format="pdf")
