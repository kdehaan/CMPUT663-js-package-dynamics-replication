#
# Performs a regression on the given growth data.
#
# Input: npm_graph_stats_weekly_10-01-2010_09-01-2015.csv
#
import sys
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
# import sympy as sym

def visualize_growth(input_file):
  df = pd.read_csv(input_file, index_col=0, parse_dates=[0]).T

  df.index = pd.to_datetime(df.index)

  df.rename(columns={'num_vertices': 'Packages', 'num_edges': 'Dependencies'}, inplace=True)

  # df = df['Packages']

  # print df.index

  def func(x, a, b, c):
    return a * np.exp(-b * x) + c

  # x = the dates / timestanps:
  x = df.index.astype(np.int64) / 10000000000000
  print x
  # y = the values
  y = df['Packages'].astype(np.int64).as_matrix()
  print y

  # plot original data:
  plt.plot(x, y, 'ro',label="Original Data")

  popt, pcov = curve_fit(func, x, y)
  print popt, pcov
  print 'a=%s b=%s' % (popt[0], popt[1])

  plt.plot(x, func(x, *popt), label="Fitted Curve")
  
  plt.legend(loc='upper left')
  # axes = df.plot(logy=True)
  # plt.scatter(df[name_1], df[name_2])
  # axes.set_xscale('log')
  # axes.set_yscale('log')
  # axes.get_xaxis().set_major_formatter(FormatStrFormatter('%.3f'))
  # axes.get_yaxis().set_major_formatter(FormatStrFormatter('%.3f'))
  # axes.set_xlim(0,10000)
  # axes.set_ylim(0,0.002)
  # axes.set_xlabel('used by applications')
  # axes.set_ylabel('number of domains')
  # plt.tight_layout()
  plt.show()


if __name__=='__main__':
  if len(sys.argv) < 2:
      print 'usage: %s <input-data>' % (sys.argv[0])
      exit(-1)
  input_file = sys.argv[1]
  visualize_growth(input_file)
