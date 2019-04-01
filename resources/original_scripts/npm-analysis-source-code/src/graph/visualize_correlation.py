#!/usr/bin/env python

#
# Visualizes the pr (values) of two given results data sets
# in one plot.
# 
# Input: "npm_graph_pr-values_top_300000_daily_09-01-2015_09-01-2015.csv"
#        "npm_graph_deps_pr-values_top_300000_daily_09-01-2015_09-01-2015.csv"
#        ...
#
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter

def visualize_correlation(input_file_1, input_file_2, top=sys.maxint):
  df = get_dfs(input_file_1, input_file_2, top)

  # print some useful information:
  print df.describe()
  print 'Spearman correlation: %s' % df[df.columns.values[0]].corr(df[df.columns.values[1]], method='spearman')

  # plot it:
  axes = df.plot(kind='scatter', x=df.columns.values[0], y=df.columns.values[1], logy=True, logx=True)
  #plt.scatter(df[name_1], df[name_2])
  # axes.set_xscale('log')
  # axes.set_yscale('log')
  axes.get_xaxis().set_major_formatter(FormatStrFormatter('%.3f'))
  axes.get_yaxis().set_major_formatter(FormatStrFormatter('%.3f'))
  # axes.set_xlim(0,10000)
  axes.set_ylim(0,0.002)
  # axes.set_xlabel('used by applications')
  # axes.set_ylabel('number of domains')
  plt.tight_layout()
  
  # save the figure:
  # fig = axes.get_figure()
  # fig.savefig('apps_per_domain.pdf')

  plt.show()


def get_dfs(input_file_1, input_file_2, top=sys.maxint):
  print '\ncorrelate %s and %s for the top %s values of the first' % (input_file_1, input_file_2, top)

  frames = []
  
  print '  read %s...' % (input_file_1)
  name_1 = input_file_1.split('/')[-1]
  df_1 = pd.read_csv(input_file_1, index_col=0)
  df_1.columns = [name_1]
  frames.append(df_1)

  print '  read %s...' % (input_file_2)
  name_2 = input_file_2.split('/')[-1]
  df_2 = pd.read_csv(input_file_2, index_col=0)
  df_2.columns = [name_2]
  frames.append(df_2)

  print '  concatenate...'
  df = pd.concat(frames, axis=1)

  # consider only the top ones:
  df.sort_values(name_1, inplace=True, ascending=False) # sort by first column
  df = df.head(top) # select only top entries

  return df


def get_correlation(input_file_1, input_file_2, top=sys.maxint):
  df = get_dfs(input_file_1, input_file_2, top)

  # print df
  return df[df.columns.values[0]].corr(df[df.columns.values[1]], method='spearman')


if __name__=='__main__':
  if len(sys.argv) < 2:
    print 'usage: %s <input-data-1> <input-data-2> <optional: top of the first dataset to consider>' % (sys.argv[0])
    exit(-1)
  input_file_1 = sys.argv[1]
  input_file_2 = sys.argv[2]
  top = sys.maxint
  if len(sys.argv) == 4:
    top = int(sys.argv[3])

  visualize_correlation(input_file_1, input_file_2, top)