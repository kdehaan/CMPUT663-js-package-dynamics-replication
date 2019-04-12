#!/usr/bin/env python

#
# Calculate the number of new packages entering the top N over time.
# 
# Input: 
# - package ranking data over time, e.g., npm_graph_pr_top_100_weekly_...
# - N = the number of top packages to consider
#
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter


def calc_accumulative_top(input_file, top_list):
  frames = []

  df = pd.read_csv(input_file, index_col=0, parse_dates=False)

  # list to store all packages already seen:
  result = {}

  for top in top_list:
    seen_list = []
    # iterate columns:
    for i in range(len(df.columns)):
      col = df.ix[:,i]

      print '%s: seen %s packages in the top %s' % (col.name, len(seen_list), top)
      if col.name not in result:
        result[col.name] = []
      result[col.name].append(len(seen_list))

      # iterate entries in column:
      for index, value in col.iteritems():
        if not np.isnan(value) and value <= top:
          if index not in seen_list:
            seen_list.append(index)
          # print index + ' ' + str(value)

  df_acc = pd.DataFrame(result).T
  df_acc.columns = top_list

  axes = df_acc.plot()
  # axes.set_xlabel('date')
  # axes.set_ylabel('absolute pagerank changes since one week ago')
  plt.show()


if __name__=='__main__':
  if len(sys.argv) < 3:
    print 'usage: %s [input_file, e.g., npm_graph_pr_top_100_weekly_...] [top numbers, e.g., 10 50 100...]' % (sys.argv[0])
    exit(-1)
  input_file = sys.argv[1]
  top_list = map(lambda a : int(a), sys.argv[2:])
  calc_accumulative_top(input_file, top_list)
