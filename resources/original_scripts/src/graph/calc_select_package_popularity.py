#!/usr/bin/env python

#
# Prints the popularity of selected packages in different measures.
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
]

def calc_popularity(package):
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

  print df.ix[package]


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
  if len(sys.argv) < 2:
      print 'usage: %s package-name' % (sys.argv[0])
      exit(-1)
  package = sys.argv[1]
  calc_popularity(package)