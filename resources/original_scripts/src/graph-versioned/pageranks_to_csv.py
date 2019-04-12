#!/usr/bin/env python
import glob
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

# obtain list of all pagerank files (*.gt):
pr_files = glob.glob('../../data/pageranks/*.csv')

overall = pd.DataFrame()

frames = []
for file_name in pr_files:
  print 'read pagerank results at %s' % file_name

  date = re.search(r'[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]', file_name, flags=0).group()

  # read the csv:
  df = pd.read_csv(file_name, index_col=['name'])
  
  # rename 'rank' to the 'date':
  df = df.rename(columns={'rank': date})

  # add this Series to the overall dataframe:
  frames.append(pd.DataFrame(df[date]).T)
  # overall = overall.merge(pd.DataFrame(df[date]).T)
  # overall[date] = df[date]

overall = pd.concat(frames)

overall.to_csv('../../data/all_pageranks.csv')