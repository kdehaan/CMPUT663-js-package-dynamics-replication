#!/usr/bin/env python

#
# Script to identify and visualize packages whose pagerank 
# has the highest variance over time.
# 
# Input: npm_graph_pr_top_180000_weekly_10-01-2010_09-01-2015.csv
#
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


def get_rank_changes(df):
  results = {}
  for index, row in df.iterrows():
    last_rank = 0
    num_movements = 0
    for rank in row:
      if math.isnan(rank):
        continue
      difference = abs(last_rank - rank)
      num_movements += difference
      last_rank = rank
    results[index] = num_movements
  return pd.DataFrame(results, index=['num_movements']).T


def visualize_strongest_movers(input_file):
  
  num_movers = 5

  df = pd.read_csv(input_file, index_col=0, parse_dates=0)[0:180000]

  movement_df = get_rank_changes(df)

  df = pd.concat([df, movement_df], axis=1)

  df.sort_values('num_movements', ascending=False, inplace=True)

  print df

  df.drop('num_movements', 1, inplace=True)

  axes = df[:num_movers].T.plot()
  plt.gca().invert_yaxis()

  plt.show()

  # df['variance'] = df.T.var()

  # df.sort_values('variance', ascending=False, inplace=True)

  # print df

  # get indexes of packages with highest variance:
  # top_mover_indexes = df.var().sort_values(ascending=False)[:num_movers].index

  # print top_mover_indexes

  # print df[top_mover_indexes]

  # create dataframe of packages and fill empty values:
  # top_movers_df = df[top_mover_indexes].drop(df.index[-1:]).fillna(len(df) + 1)

  # print top_movers_df

  # create plot:
  # axes = top_movers_df.plot()
  # # axes.set_ylim(0,100)
  # for line in axes.lines:
  #   line.set_linewidth(2)
  # plt.gca().invert_yaxis()
  # plt.show()


if __name__=='__main__':
  if len(sys.argv) < 1:
      print 'usage: %s <input-data>' % (sys.argv[0])
      exit(-1)
  input_file = sys.argv[1]
  visualize_strongest_movers(input_file)