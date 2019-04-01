# !/usr/bin/env python

#
# Small script to convert download results for easier processing with pandas:
# - Makes package name the index
# - Creates 2 files, one containing the download rank, the other containing the
#   absolute download figures
# 
# Input example: "npm-downloads-ranking-2010-01-01-to-2015-09-01.csv"
#
import sys
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if __name__=='__main__':
  if len(sys.argv) < 2:
    print 'usage: %s <input-data>' % (sys.argv[0])
    exit(-1)
  input_file = sys.argv[1]
  file_name = input_file.split('/')[-1]
  dates = re.compile(r'(\d+-\d+-\d+)', re.IGNORECASE).findall(file_name)
  from_date = dates[0]
  to_date = dates[1]
  timespan = from_date + '_' + to_date

  df = pd.read_csv(input_file, names=['rank', 'name', 'downloads'], index_col=1)
  
  df_rank = df['rank'].to_frame()
  df_rank.columns = [timespan]
  df_rank.to_csv('npm_graph_download-ranks_' + from_date + '_' + to_date + '.csv')

  df_downloads = df['downloads'].to_frame()
  df_downloads.columns = [timespan]
  df_downloads.to_csv('npm_graph_downloads_' + from_date + '_' + to_date + '.csv')

  # print df_rank