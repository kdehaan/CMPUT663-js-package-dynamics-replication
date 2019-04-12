import sys
import math
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def linear_regression(x, y):
    A = np.vstack([ x, np.ones(len(x)) ]).T
    m,c = np.linalg.lstsq(A, y)[0]
    return m,c

def scale_data(x):
    """Returns (xs, a, b) such that x = a + xs*b."""
    m = np.min(x)
    x0 = x - m
    M = np.max(x0)
    x1 = x0 / M
    return (x1, m, M)

def f(x0, a, b, c):
    return a * np.exp(b * x0) + c

def fit_exp(x, y):
    popt, pcov = curve_fit(f, x, y, maxfev=100000000)
    print popt
    print pcov
    return (popt[0], popt[1], popt[2])

def work(input_file):
    df = pd.read_csv(input_file).T

    df = df.ix[1:]

    df.index = pd.to_datetime(df.index)

    x = df.index.astype(np.int64).astype(np.float64) / 10000000000000.0
    y = df[4].astype(np.float64).as_matrix()

    (xs, xa, xb) = scale_data(x)
    (ys, ya, yb) = scale_data(y)

    (a,b,c) = fit_exp(xs, ys)

    ys_approx = f(xs, a, b, c)
    y_approx  = ya + yb * ys_approx

    plt.plot(x, y, label="Number of packages")

    plt.plot(x, y_approx, label="Approximation")

    plt.show()

if __name__ == "__main__":
  if len(sys.argv) < 2:
      sys.stderr.write("Usage: %s <input-data>\n" % sys.argv[0])
      sys.exit(1)

  input_file = sys.argv[1]
  work(input_file)
