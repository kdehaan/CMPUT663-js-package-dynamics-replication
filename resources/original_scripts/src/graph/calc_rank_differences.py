#!/usr/bin/env python

#
# Calculate the differences in rank of packages in the two given 
# files and sort results correspondingly.
# 
# Input (examples):
#   npm_graph_pr_top_1800000_weekly_10-01-2010_09-01-2015.csv
#   npm_graph_downloads-ranks_2015-09-01.csv
#   
#
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter

def calc_rank_differences(input_file_1, input_file_2):
  df = get_dfs(input_file_1, input_file_2)

  col1 = df.ix[:,0]
  name1 = ' '.join(col1.name.split('_')[:4])
  col2 = df.ix[:,1]
  name2 = ' '.join(col2.name.split('_')[:4])
  sub = col1 - col2
  subname = name1 + ' - ' + name2
  sub.name = subname

  df = pd.DataFrame(sub).sort_values(subname, ascending=False)

  df = df.dropna()

  print '\nDoing much better in "%s" than in "%s":' % (name1, name2)
  for index, row in df.tail(10).sort_values(subname).abs().iterrows():
    print '%30s: difference=%s %30s=%s %30s=%s' % (index, row[subname], name1, col1[index], name2, col2[index])
  # print df.tail(10).sort_values(subname).abs()

  print '\nDoing much better in "%s" than in "%s":' % (name2, name1)
  for index, row in df.head(10).iterrows():
    print '%30s: difference=%s %30s=%s %30s=%s' % (index, row[subname], name1, col1[index], name2, col2[index])

  # print df


def get_dfs(input_file_1, input_file_2):
  frames = []

  print '  read %s...' % (input_file_1)
  name_1 = input_file_1.split('/')[-1]
  df_1 = pd.read_csv(input_file_1, index_col=0)
  df_1.columns = [name_1]
  frames.append(df_1)

  print '  read %s...' % (input_file_2)
  name_2 = input_file_2.split('/')[-1]
  df_2 = pd.read_csv(input_file_2, index_col=0)
  print df_2
  df_2.columns = [name_2]
  frames.append(df_2)

  print '  concatenate...'
  df = pd.concat(frames, axis=1)

  return df

if __name__=='__main__':
  if len(sys.argv) < 2:
    print 'usage: %s <input-data-1> <input-data-2>' % (sys.argv[0])
    exit(-1)
  input_file_1 = sys.argv[1]
  input_file_2 = sys.argv[2]
  calc_rank_differences(input_file_1, input_file_2)