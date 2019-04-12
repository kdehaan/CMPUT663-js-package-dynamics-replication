#!/usr/bin/env python

#
# Calculate the differences in rank of packages in multiple given 
# files and sort results correspondingly.
#
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter

files = [
  {
    'name': 'GitHub',
    'path': '../../data/pageranks/apps_graph_bipartite_pr_top_300000_daily_09-01-2015_09-01-2015.csv'
  }
  ,
  {
    'name': 'npm',
    'path': '../../data/pageranks/npm_graph_pr_top_300000_daily_09-01-2015_09-01-2015.csv'
  }
  ,
  {
    'name': 'downloads',
    'path': '../../data/downloads/npm_graph_download-ranks_2015-08-01_2015-09-01.csv'
  }
]


frames = []
for o in files:
  df = pd.read_csv(o['path'], index_col=0)
  df.columns = [o['name']]
  frames.append(df)

df = pd.concat(frames, axis=1)
df = df.dropna()
# df['min'] = pd.DataFrame([df['npm pagerank'], df['Bipartite pagerank']]).min()

df = df.sort_values('downloads', ascending=False)

df['diff'] = df['downloads'] - df['npm']

df = df.sort_values('diff', ascending=False)

print df

# df = ((df + df.shift(-1)) / 300)[::300]
# print df

axes = df['diff'].plot()
axes.set_xlabel('packages')
axes.set_ylabel('difference between GitHub and npm pageranks')
plt.show()
