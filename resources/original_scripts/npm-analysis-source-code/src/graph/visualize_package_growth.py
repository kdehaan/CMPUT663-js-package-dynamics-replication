#!/usr/bin/env python

#
# Script to visualize growth of the npm ecosystem w.r.t. number
# of packages and number of dependencies between them.
# 
# Input: 
# - Statistics on package and dependency numbers:
#     "npm_graph_stats_weekly_10-01-2010_09-01-2015.csv"
# - Statistics on package and dependency numbers clean (i.e., without inactive packages):
#     "repos_newer_180_days_at_date.csv"
#
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

def visualize_growth(input_file, input_clean):
  df = pd.read_csv(input_file, index_col=0, parse_dates=0).T

  df.rename(columns={'num_vertices': 'Packages', 'num_edges': 'Dependencies'}, inplace=True)

  df_clean = pd.read_csv(input_clean, index_col=0, parse_dates=0)
  df_clean.columns = ['Packages newer than 180 days']

  df = df[['Packages', 'Dependencies']].join(df_clean)

  df['Dependencies per Package'] = pd.DataFrame(df['Dependencies'] / df['Packages'])

  width = 5.0
  plt.rc("figure", figsize=(width, 3.0*width/4.0))

  # plot left:
  ax = df[['Packages', 'Dependencies']].plot(lw=2.0, legend=False)
  ax.set_ylabel('No. of Packages / Dependencies')
  ax.xaxis.grid(True)


  # plot rights:
  ax2 = df['Dependencies per Package'].plot(secondary_y=True, lw=2.0, legend=False)
  ax2.set_ylim(0,10)
  ax2.set_ylabel('Dependencies per Package')

  plt.tight_layout()
  plt.grid()
  plt.show()


if __name__=='__main__':
  if len(sys.argv) < 3:
      print 'usage: %s <input-data> <input-clean-growth>' % (sys.argv[0])
      exit(-1)
  input_file = sys.argv[1]
  input_clean = sys.argv[2]
  visualize_growth(input_file, input_clean)