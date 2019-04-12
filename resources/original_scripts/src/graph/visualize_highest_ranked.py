#!/usr/bin/env python

#
# Script to identify and visualize packages whose pagerank 
# has been the highest over time.
# 
# Input: "npm_graph_pr_top_180000_weekly_10-01-2010_09-01-2015.csv"
#
import sys
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from matplotlib.backends.backend_pdf import PdfPages
from scipy.stats import gmean
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

def visualize_highest_ranked(input_file):
  
  num_packages = 5

  df = pd.read_csv(input_file, index_col=0, parse_dates=[0])
  # df.columns = df.columns.to_datetime()
  # df.columns = pd.to_datetime(df.columns)

  # Reverse rank sum:
  # visualize_reverse_rank(df, num_packages)

  # Average rank:
  # visualzie_avg_rank(df, num_packages)

  # Geometric mean rank:
  # visualize_geo_rank(df, num_packages)

  # Relative rank (from 0 - 1):
  # visualize_relative_rank(df, num_packages)

  # Select packages:
  # packages = ['underscore', 'lodash', 'lazy.js', 'sugar', 'valentine', 'babel', 'typescript']
  # visualize_select_packages(df, packages)

  # Average rank per year:
  visualize_avg_rank_per_year(df, num_packages)


def visualize_reverse_rank(df, num_packages):
  df['overall_score'] = df.T.apply(lambda x: 300000 - x).sum()
  df.sort_values('overall_score', ascending=True, inplace=True)
  df.drop('overall_score', axis=1, inplace=True)
  ax = df[:num_packages].plot()
  plt.tight_layout()
  plt.gca().invert_yaxis()
  plt.savefig('reverse_rank.png')
  #plt.show()


def visualize_select_packages(df, packages):
  df_select = df.ix[packages]
  print(type(df_select.columns))
  df_select.columns = pd.to_datetime(df_select.columns)

  width = 5.0
  plt.rc("figure", figsize=(width, 3.0*width/4.0))

  axes = df_select.T.plot()
  plt.tight_layout()
  axes.set_ylim(-150, 10000)
  plt.yticks(get_y_ticks(axes.get_ylim()[1], 10))
  axes.set_ylabel('Pagerank')
  plt.gca().invert_yaxis()
  plt.grid()
  plt.tight_layout()
  plt.savefig('select_packages.png')
  #plt.show()

def get_y_ticks(ylimit, num_ticks):
  ticks = [1]
  interval = ylimit / num_ticks
  for i in range(1, num_ticks):
    ticks.append(interval * i)
  print ticks
  return ticks

def visualize_relative_rank(df, num_packages):
  df = df.apply(lambda x: x / x.count())
  axes = df[:num_packages].T.plot()
  plt.tight_layout()
  plt.gca().invert_yaxis()
  plt.savefig('relative_rank.png')
  #plt.show()


def visualzie_avg_rank(df, num_packages):
  df['overall_score'] = df.T.mean()
  df.sort_values('overall_score', ascending=True, inplace=True)
  df.drop('overall_score', axis=1, inplace=True)
  axes = df[:num_packages].T.plot()
  plt.tight_layout()
  plt.gca().invert_yaxis()
  plt.savefig('avg_rank.png')
  #plt.show()


def visualize_geo_rank(df, num_packages):
  def geo_mean(x):
    return gmean(list(x.dropna()))
  df['overall_score'] = df.T.apply(geo_mean) # df.T.mean()
  df.sort_values('overall_score', ascending=True, inplace=True)
  df.drop('overall_score', axis=1, inplace=True)
  df_select = df.ix[:num_packages,:]
  # re-mark columns:
  df_select.columns = pd.to_datetime(df_select.columns)

  width = 5.0
  plt.rc("figure", figsize=(width, 3.0*width/4.0))

  axes = df_select.T.plot()
  axes.set_ylim(0,100)
  plt.yticks(get_y_ticks(axes.get_ylim()[1], 10))
  axes.set_ylabel('Pagerank')
  plt.tight_layout()
  plt.gca().invert_yaxis()
  plt.grid()
  plt.savefig('geo_mean_rank.png')
  #plt.show()


def visualize_avg_rank_per_year(df, num_packages):
  year_dfs = []
  # year_dfs.append(df.iloc[:,0:52]) # 2010
  # year_dfs.append(df.iloc[:,53:104]) # 2011
  # year_dfs.append(df.iloc[:,105:158]) # 2012
  # year_dfs.append(df.iloc[:,159:212]) # 2013
  # year_dfs.append(df.iloc[:,213:266]) # 2014
  # year_dfs.append(df.iloc[:,267:320]) # 2015
  # year_dfs.append(df.iloc[:,321:374]) # 2016
  # year_dfs.append(df.iloc[:,375:428]) # 2017
  # year_dfs.append(df.iloc[:,429:482]) # 2018
  # year_dfs.append(df.iloc[:,9:12]) # 2010
  year_dfs.append(df.iloc[:,11:24]) # 2011
  year_dfs.append(df.iloc[:,24:36]) # 2012
  year_dfs.append(df.iloc[:,36:48]) # 2013
  year_dfs.append(df.iloc[:,48:60]) # 2014
  year_dfs.append(df.iloc[:,60:72]) # 2015
  year_dfs.append(df.iloc[:,72:84]) # 2016
  year_dfs.append(df.iloc[:,84:96]) # 2017
  year_dfs.append(df.iloc[:,96:108]) # 2018
  year_dfs.append(df.iloc[:,108:]) # 2019

  width = 15.0
  # fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(width*1.75, width))
  fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(width, 1.2*width))

  for i, df in enumerate(year_dfs):
    print i
    def geo_mean(x):
      return gmean(list(x.dropna()))

    df['overall_score'] = df.T.apply(geo_mean) # .mean()
    df.sort_values('overall_score', ascending=True, inplace=True)
    df.drop('overall_score', axis=1, inplace=True)
    
    # ax = df[:num_packages].T.fillna(0).plot(ax=axs[int(math.floor(i/5)), i%5], rot=45, fontsize=10)
    ax = df[:num_packages].T.fillna(0).plot(ax=axs[int(math.floor(i/3)), i%3], rot=45, fontsize=10)

    # # Shrink current axis's height by 10% on the bottom
    # box = ax.get_position()
    # ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])

    # # Put a legend below current axis
    # ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.34), fancybox=True, shadow=True, ncol=2, fontsize='medium')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5,-0.25), fancybox=True, shadow=True, ncol=2, fontsize='medium')

    # plt.gca().invert_yaxis()
    if i == 0:
      ax.set_ylabel('Pagerank')
    ax.set_ylim(0,12)
    ax.set_yticks((1, 2, 3, 4, 5, 6,7,8,9,10,11,12))
    ax.set_xlim(pd.Timestamp('201%s-01-01' % (i + 1)), pd.Timestamp('201%s-12-31' % (i + 1)))
    ax.set_ylim(ax.get_ylim()[::-1])
  # fig.subplots_adjust(wspace=0.25, left=0.04, right=0.99, top=0.975, bottom=0.45)
  fig.subplots_adjust(hspace=0.8, bottom=0.2)
  # fig.delaxes(axs[1,4])
  #plt.show()

if __name__=='__main__':
  if len(sys.argv) < 1:
      print 'usage: %s <input-data>' % (sys.argv[0])
      exit(-1)
  input_file = sys.argv[1]
  visualize_highest_ranked(input_file)
  
  with PdfPages("highest_ranked.pdf") as pp:
      pp.savefig(plt.gcf())
