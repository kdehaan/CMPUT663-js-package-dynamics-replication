#!/usr/bin/env python

#
# Calculates the changes of repository pageranks between pairs of dates
#
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter


def calculate_pr_dynamics(input_file):
  frames = []

  df = pd.read_csv(input_file, index_col=0, parse_dates=0).T

  # print df

  for i in range(len(df.columns) - 1):
    col1 = df.ix[:,i]
    col2 = df.ix[:,i+1]
    sub = col1 - col2
    sub.name = col2.name # str(col1.name) + '_' + str(col2.name)
    frames.append(pd.DataFrame(sub))
   
  print len(frames)
  df = pd.concat(frames)
  df_change = df.abs().sum()

  axes = df_change.plot(title='Pagerank changes within top 100')
  axes.set_xlabel('date')
  axes.set_ylabel('absolute pagerank changes since one week ago')

  plt.show()


if __name__=='__main__':
  if len(sys.argv) < 2:
    print 'usage: %s [input_file] ' % (sys.argv[0])
    exit(-1)
  input_file = sys.argv[1]
  calculate_pr_dynamics(input_file)