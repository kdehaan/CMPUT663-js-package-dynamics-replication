#!/usr/bin/env python

#
# Visualizes the number of packages entering the top N pageranks for the first time
# over time.
# 
# Input: "npm_graph_pr_top_180000_weekly_10-01-2010_09-01-2015.csv"
#
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)


def visualize_top_newcomers(input_file):
  # list of top values to consider:
  top_list = [10, 100, 250]

  # read CSV:
  df = pd.read_csv(input_file, index_col=0, parse_dates=False)
  df.columns = pd.to_datetime(df.columns)

  # start at 2011-06-01:
  # df = df.ix[:,35:]

  frames = []
  for top in top_list:
    frame = get_newcomers(df, top)
    frames.append(frame)

  df_results = pd.concat(frames, axis=1)

  # print absolute numbers of packages entering per year:
  df_results.resample('A', how='sum').to_csv("top_newcomers_data.csv")
  print "printed stuff"

  width = 6.0
  plt.rc("figure", figsize=(width, 3.0*width/4.0))

  ax = df_results.resample('1M', how='mean').plot(style=['-', '-', '-'], lw=1.5) # resample('4M', how='mean')
  ax.set_ylim(0, 10)
  ax.set_ylabel('No. of Packages')
  plt.tight_layout()
  plt.grid()
  plt.show()


def get_newcomers(df, top):
  seen = []
  results = {}
  for column in df:
    ranks = df[column].sort_values()
    new_packages = 0
    for package_name, value in ranks[:top].iteritems():
      if package_name not in seen:
        new_packages += 1
        seen.append(package_name)
    results[column] = new_packages
  return pd.DataFrame(results, index=['Entering top %s for the first time' % str(top)]).T


if __name__=='__main__':
  if len(sys.argv) < 1:
      print 'usage: %s <input-data>' % (sys.argv[0])
      exit(-1)
  input_file = sys.argv[1]
  visualize_top_newcomers(input_file)
