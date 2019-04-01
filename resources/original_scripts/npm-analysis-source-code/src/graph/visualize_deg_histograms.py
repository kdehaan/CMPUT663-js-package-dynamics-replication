#!/usr/bin/env python

#
# Visualizes the histograms of degree values.
# 
# No further input required.
#
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import math

files = [
  '../../data/pageranks/apps_graph_bipartite_hist_in_daily_09-01-2015_09-01-2015.csv',
  '../../data/pageranks/apps_graph_deps_bipartite_hist_in_daily_09-01-2015_09-01-2015.csv',
  '../../data/pageranks/apps_graph_dev_bipartite_hist_in_daily_09-01-2015_09-01-2015.csv',
  '../../data/pageranks/npm_graph_hist_in_daily_09-01-2015_09-01-2015.csv',
  '../../data/pageranks/npm_graph_deps_hist_in_daily_09-01-2015_09-01-2015.csv',
  '../../data/pageranks/npm_graph_dev_hist_in_daily_09-01-2015_09-01-2015.csv'
]

names = [
  'apps bipartite',
  'apps bipartite - deps. only',
  'apps bipartite - dev deps. only',
  'npm',
  'npm - deps. only',
  'npm - dev deps. only'
]

frames = []

num_cols = 3
num_rows = int(math.ceil(len(files) / num_cols))
fig, axs = plt.subplots(nrows=num_rows, ncols=num_cols)

for i, file_name in enumerate(files):
  row = int(math.ceil(i / num_cols))
  col = int(i - row * num_cols)
  print 'processing %s %s...' % (i, file_name)
  print 'row: %s, col: %s' % (row, col)
  frame = pd.read_csv(file_name, index_col=0)
  frame.columns = [names[i]]
  frame.loc[0:500].plot(logy=True, ax=axs[row, col])

plt.suptitle("Histograms of in degrees")

plt.show()