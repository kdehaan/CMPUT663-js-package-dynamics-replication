#!/usr/bin/env python

#
# Visualizes the histograms of pagerank values of different datasets
#
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

files = [
  '../../data/pageranks/apps_graph_bipartite_pr-values_top_300000_daily_09-01-2015_09-01-2015.csv',
  '../../data/pageranks/apps_graph_deps_bipartite_pr-values_top_300000_daily_09-01-2015_09-01-2015.csv',
  '../../data/pageranks/apps_graph_dev_bipartite_pr-values_top_300000_daily_09-01-2015_09-01-2015.csv',
  '../../data/pageranks/npm_graph_pr-values_top_300000_daily_09-01-2015_09-01-2015.csv',
  '../../data/pageranks/npm_graph_deps_pr-values_top_300000_daily_09-01-2015_09-01-2015.csv',
  '../../data/pageranks/npm_graph_dev_pr-values_top_300000_daily_09-01-2015_09-01-2015.csv'
]

names = [
  'apps bipartite',
  'apps bipartite - dependencies only',
  'apps bipartite - dev dependencies only',
  'npm',
  'npm - dependencies only',
  'npm - dev dependencies only'
]

frames = []
for i, file_name in enumerate(files):
  print 'processing %s %s...' % (i, file_name)
  frame = pd.read_csv(file_name, index_col=0)
  frame.columns = ['pagerank value ' + names[i]]
  frames.append(frame)


df = pd.concat(frames, axis=1)
print df

df.hist(bins=100, log=True)\

plt.suptitle("Histograms of pagerank values")

plt.show()

  # print df
  # axes = df.plot(kind='hist', logy=True, bins=200, title="test")
  # axes.set_ylim(0,10**7)
  # plt.show()
