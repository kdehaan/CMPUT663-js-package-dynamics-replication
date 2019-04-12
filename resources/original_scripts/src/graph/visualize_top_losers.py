#!/usr/bin/env python

#
# Visualizes the top losing packages.
#
# Input: "npm_graph_pr_top_180000_weekly_10-01-2010_09-01-2015.csv"
#
import sys
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gmean

def visualize_highest_lossers(input_file):
  
  num_packages = 5

  df = pd.read_csv(input_file, index_col=0, parse_dates=0)
  df.columns = df.columns.to_datetime()

  visualize_loosers_top_1000(df, num_packages)

def get_max_decline(df):
  results = {}
  for index, row in df.iterrows():
    highest_rank = len(df)
    lowest_subsequent_rank = 0
    for rank in row:
      if math.isnan(rank):
        continue
      if rank < highest_rank:
        highest_rank = rank
        lowest_subsequent_rank = 0
      elif rank >= lowest_subsequent_rank and rank < len(df):
        lowest_subsequent_rank = rank
      else:
        continue
    max_decline = lowest_subsequent_rank - highest_rank
    # print '%s: highest=%s, lowest=%s, max-decline=%s' % (index, highest_rank, lowest_subsequent_rank, max_decline)
    results[index] = max_decline
  return pd.DataFrame(results, index=['num_declines']).T


def get_rank_declines(df):
  results = {}
  for index, row in df.iterrows():
    last_rank = 0
    num_declines = 0
    for rank in row:
      if math.isnan(rank):
        continue
      if rank < 1000:
        if last_rank < rank: 
          num_declines += rank - last_rank
        last_rank = rank
    results[index] = num_declines
  return pd.DataFrame(results, index=['num_declines']).T


def visualize_loosers_top_1000(df, num_packages):
  # sort by geometric mean:
  def geo_mean(x):
    return gmean(list(x.dropna()))
  df['overall_score'] = df.T.apply(geo_mean) # df.T.mean()
  df.sort_values('overall_score', ascending=True, inplace=True)
  df.drop('overall_score', axis=1, inplace=True)

  # Consider top 1000 from hereon:
  df = df[:1000]

  # Determine packages loosing the most:
  df['decline'] = get_max_decline(df)
  df.sort_values('decline', ascending=False, inplace=True)
  df.drop('decline', axis=1, inplace=True)
  df.columns = df.columns.to_datetime()

  print df
  axes = df[:num_packages].T.plot()
  axes.set_ylim(-50,3000)
  plt.yticks(get_y_ticks(axes.get_ylim()[1], 10))
  axes.set_ylabel('Pagerank')
  axes.set_xlabel('Time')
  plt.gca().invert_yaxis()
  plt.show()


def get_y_ticks(ylimit, num_ticks):
  ticks = [1]
  interval = ylimit / num_ticks
  for i in range(1, num_ticks):
    ticks.append(interval * i)
  print ticks
  return ticks


if __name__=='__main__':
  if len(sys.argv) < 1:
      print 'usage: %s <input-data>' % (sys.argv[0])
      exit(-1)
  input_file = sys.argv[1]
  visualize_highest_lossers(input_file)