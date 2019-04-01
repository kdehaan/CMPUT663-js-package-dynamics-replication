import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    def triple_to_float(major, minor, patch):
        K = 0.5
        m = float(major)
        M = float(minor)
        p = float(patch)

        M_p = M + 1.0 - (1.0 / (K*p + 1.0))
        m_M_p = m + 1.0 - (1.0 / (K*M_p + 1.0))

        return m_M_p

    try:
        package = sys.argv[1]
    except:
        print "You need to provide a package name."
        sys.exit(1)

    input_file = sys.argv[0].replace("plot-", "data-").replace(".py", "-%s.dat" % package)

    frame = pd.read_csv(input_file)

    width = 5.0

    plt.rc("text", usetex=True)
    plt.rc("figure", figsize=(width, 3.0*width/4.0))
    plt.rc("axes", linewidth=0.5)

    versions = frame["linearized"]
    dates    = frame["released"] / 60 / 60 / 24 / 30.5

    plt.scatter(dates, versions, marker='+')

    axes = plt.gca()
    # axes.set_xlim([ 0, 7 ])
    axes.set_ylim([ 0.5, 5.5 ])

    # Preparing the ticks.
    ytick_pos = []
    ytick_labels = []
    for major in range(0, 5):
        for minor in [ 2, 4, 6, 8, 10 ]:
            ytick_pos.append(triple_to_float(major, minor, 0))
            ytick_labels.append("%d.%d.0" % (major, minor))
    plt.yticks(ytick_pos, ytick_labels)

    axes.yaxis.grid(True, which='major')

    # plt.xticks(range(0,11))

    plt.show()

    # plot_file = sys.argv[0].replace("plot-", "").replace(".py", ".pdf") 
    # plt.savefig(plot_file, format="pdf")
