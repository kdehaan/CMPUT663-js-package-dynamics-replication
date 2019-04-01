#!/usr/bin/env python

#
# Creates a dataframe containing all packages from npm
# as well as their ranking regarding different popularity metrics
# and the differences in rank between these metrics.
# 
# The resulting DataFrame will ONLY consider packages that have a valid
# rank regarding at least one popularity measure!
# 
# No further input required.
#
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter

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
  ,
  {
    'name': 'keywords',
    'path': '../../data/npm_repos_keywords.csv'
  }
]

def create_popularity_csv():
  frames = []

  # get filtered GitHub dependencies:
  frames.append(get_filtered_github(files[0]['path']))

  # get filtered pageranks:
  frames.append(get_filtered_pageranks(files[1]['path']))

  # get filtered downloads: (NO processing needed, all have downloads)
  df_downloads = pd.read_csv(files[2]['path'], index_col=0)
  df_downloads.columns = ['downloads']
  frames.append(df_downloads)

  df_keywords = pd.read_csv(files[3]['path'], index_col=0, sep=',')
  df_keywords.columns = [files[3]['name']]
  frames.append(df_keywords)

  # create overall dataframe:
  df = pd.concat(frames, axis=1)

  # # create difference dataframes:
  df_diff_1 = get_diff_df(df, 'npm', 'GitHub')

  df_diff_2 = get_diff_df(df, 'npm', 'downloads')

  df_diff_3 = get_diff_df(df, 'downloads', 'GitHub')

  df = pd.concat([df, df_diff_1, df_diff_2, df_diff_3], axis=1)

  df.to_csv('popularity_measures.csv')


def get_diff_df(df, name1, name2):
  # create DataFrame only containing rows with both values:
  df = df[[name1, name2]]
  df.dropna(how='any', inplace=True)

  # create difference:
  df_diff = pd.DataFrame(df[name1] - df[name2])
  name = name1 + ' - ' + name2
  df_diff.columns = [name]
  df_diff.sort_values(name, ascending=False, inplace=True)

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
  df_filtered['npm'] = range(1, len(df_filtered) + 1)

  return pd.DataFrame(df_filtered['npm'])


def get_filtered_github(file_name):
  df = pd.read_csv(file_name, index_col=0)
  # filter min values:
  df_filtered = df[(df['2015-09-01'] != 0)]

  # create ranking:
  df_filtered.sort_values('2015-09-01', ascending=False, inplace=True)
  df_filtered['GitHub'] = range(1, len(df_filtered) + 1)

  return pd.DataFrame(df_filtered['GitHub'])


if __name__=='__main__':
  create_popularity_csv()