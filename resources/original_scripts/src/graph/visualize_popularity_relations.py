#!/usr/bin/env python

#
# Visualizes the relationships (differences in ranks) of different popularity measures.
# Considers only ranks that are NOT random. E.g., filters packages that have all the same
# minimum pagerank value as they don't have any incoming relations.
# 
# It does also re-rank the packages after filtering:
#   Consider two rankings A and B regarding a set of 150 entries.
#   A contains 100 valid ranks, 1 - 100.
#   B contains  50 valid ranks, 1 -  50.
#   Not having a valid value means that the entry performs indistinguishably BAD.
#   A comparison of A and B results in 40 comparisons where entries have valid values in A and B.
#   Theory 1:
#     Re-rank values regarding A and B from 1 - 40.
#     This way, one compares the relative rankings between A and B.
#     Neglects all the packages in either A or B that have no valid value in the other ranking.
#   Theory 2:
#     Compare values of A and B without re-ranking, resulting for example in A = 2, B = 125.
#     This way, one compares the absolute ranks of A and B.
#     The resulting distribution may be skewed, for example, ranks may be comparatively lower in A.
#     But doesn't that account for the fact, that there are entries that rank higher in A and comparatively 
#     low in B (= they don't even have a valid rank)?
#
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

files = [
  {
    'name': 'GitHub',
    'path': '../../data/pageranks/apps_graph_bipartite_in-deg_daily_09-01-2015_09-01-2015.csv'
  }
  ,
  {
    'name': 'npm',
    'path': '../../data/pageranks/npm_graph_pr-values_top_300000_daily_09-01-2015_09-01-2015.csv'
  }
  ,
  {
    'name': 'downloads',
    'path': '../../data/downloads/npm_graph_download-ranks_2015-08-01_2015-09-01.csv'
  }
]

def visualize_popularity_relations():
  frames = []

  # get filtered GitHub dependencies:
  frames.append(get_filtered_github(files[0]['path']))

  # get filtered pageranks:
  frames.append(get_filtered_pageranks(files[1]['path']))

  # get filtered downloads: (NO processing needed, all have downloads)
  df_downloads = pd.read_csv(files[2]['path'], index_col=0)
  df_downloads.columns = ['downloads']
  frames.append(df_downloads)

  # create overall dataframe:
  df = pd.concat(frames, axis=1)
  
  # create difference dataframes:
  df_diff_1 = get_diff_df(df, 'npm pagerank', 'GitHub dependencies')

  df_diff_2 = get_diff_df(df, 'npm pagerank', 'downloads')

  df_diff_3 = get_diff_df(df, 'downloads', 'GitHub dependencies')

  # plot them:
  width = 10.0
  fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(width, 3.0*width/6.5))

  ax1 = df_diff_1.plot(ax=axs[0, 0], ylim=(-len(df_diff_1), len(df_diff_1)), legend=False)
  ax1.set_xlabel("Package")
  ax1.set_ylabel("Diff. npm pagerank\nand GitHub rank")
  ax1.grid(True)

  ax11 = df_diff_1.plot(kind='hist', ax=axs[1, 0], ylim=(0, 0.5 * len(df_diff_1)), legend=False)
  ax11.set_xlabel("Diff. npm pagerank\nand GitHub rank")
  ax11.grid(True)
  ax11.xaxis.set_ticks([-20000, 0, 20000])

  ax2 = df_diff_2.plot(ax=axs[0, 1], ylim=(-len(df_diff_2), len(df_diff_2)), legend=False)
  ax2.set_xlabel("Package")
  ax2.set_ylabel("Diff. npm pagerank\nand download rank")
  ax2.grid(True)

  ax21 = df_diff_2.plot(kind='hist', ax=axs[1, 1], ylim=(0,  0.5 * len(df_diff_2)), legend=False)
  ax21.set_xlabel("Diff. npm pagerank\nand download rank")
  ax21.grid(True)
  ax21.xaxis.set_ticks([-40000, 0, 40000])

  ax3 = df_diff_3.plot(ax=axs[0, 2], ylim=(-len(df_diff_3), len(df_diff_3)), legend=False)
  ax3.set_xlabel("Package")
  ax3.set_ylabel("Diff. GitHub rank\nand download rank")
  ax3.grid(True)
  ax3.xaxis.set_ticks([0, 10000, 20000, 30000])

  ax31 = df_diff_3.plot(kind='hist', ax=axs[1, 2], ylim=(0, 0.5 * len(df_diff_3)), legend=False)
  ax31.set_xlabel("Diff. GitHub rank\nand download rank")
  ax31.grid(True)
  ax31.xaxis.set_ticks([-30000, 0, 30000])


  plt.tight_layout()

  # fig.set_size_inches(18.5, 10.5, forward=True)
  fig.subplots_adjust(wspace=0.5, left=0.12, right=0.99, top=0.975, bottom=0.15)
  plt.show()


def get_diff_df(df, name1, name2):
  # create DataFrame only containing rows with both values:
  df = df[[name1, name2]]
  df.dropna(how='any', inplace=True)

  # re-rank column 1:
  df.sort_values(name1, ascending=True, inplace=True)
  df[name1] = range(1, len(df) + 1)
  
  # re-rank column 2:
  df.sort_values(name2, ascending=True, inplace=True)
  df[name2] = range(1, len(df) + 1)

  # create difference:
  df_diff = pd.DataFrame(df[name1] - df[name2])
  name = name1 + ' - ' + name2
  df_diff.columns = [name]
  df_diff.sort_values(name, ascending=False, inplace=True)
  df_diff.index = range(len(df_diff))

  # calculate correlation:
  spearman = df[df.columns.values[0]].corr(df[df.columns.values[1]], method='spearman')
  print 'Spearman correlation between %s and %s: %s' % (name1, name2, spearman)

  return df_diff


def get_filtered_pageranks(file_name):
  df = pd.read_csv(file_name, index_col=0)
  # filter min values:
  min_pagerank_value = df.min()[0]
  df_filtered = df[(df['2015-09-01'] != min_pagerank_value)]
  
  # create ranking:
  df_filtered.sort_values('2015-09-01', ascending=False, inplace=True)
  df_filtered['npm pagerank'] = range(1, len(df_filtered) + 1)

  return pd.DataFrame(df_filtered['npm pagerank'])


def get_filtered_github(file_name):
  df = pd.read_csv(file_name, index_col=0)
  # filter min values:
  df_filtered = df[(df['2015-09-01'] != 0)]

  # create ranking:
  df_filtered.sort_values('2015-09-01', ascending=False, inplace=True)
  df_filtered['GitHub dependencies'] = range(1, len(df_filtered) + 1)

  return pd.DataFrame(df_filtered['GitHub dependencies'])


if __name__=='__main__':
  visualize_popularity_relations()