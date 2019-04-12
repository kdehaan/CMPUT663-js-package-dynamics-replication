#!/usr/bin/env python

#
# Determine and prints keywords of packages that are comparatively the
# highest ranking in npm as compared to GitHub and vice versa.
#
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter


def get_top_keyword_count_df(df, column_name, top, reverse):
  df.sort_values(column_name, inplace=True, ascending=(not reverse))
  keyword_counts = {}
  for index, row in df[:top].iterrows():
    keyword_list = str(row['keywords']).split(';')
    for name in keyword_list:
      if name not in keyword_counts:
        keyword_counts[name] = 1
      else:
        keyword_counts[name] += 1
  new_column_name = column_name
  if reverse:
    new_column_name = '%s - %s' % (column_name.split(' - ')[1], column_name.split(' - ')[0])
  new_df = pd.DataFrame(keyword_counts, index=['count_' + new_column_name]).T
  return new_df.sort_values('count_' + new_column_name, ascending=False)

# read DataFrame with all popularity measures and their rank differences:
df = pd.read_csv('../../data/popularity_measures.csv', index_col=0)

# count the keywords in the 1000 packages the most better on npm than GitHub:
print '\n\nKeyword count for packages better on npm than on GitHub:'
better_npm_df = get_top_keyword_count_df(df, 'npm - GitHub', 1000, False)
print better_npm_df[:20]

# count the keywords in the 1000 packages the most better on GitHub than npm:
print '\n\nKeyword count for packages better on GitHub than on npm:'
better_github_df = get_top_keyword_count_df(df, 'npm - GitHub', 1000, True)
print better_github_df[:20]

# find keywords with the highest different count between npm- and GitHub-strong packages:
new_df = pd.concat([better_npm_df, better_github_df], axis=1) 
new_df['diff'] = new_df['count_npm - GitHub'] - new_df['count_GitHub - npm']

# print keywords that predominantly appear in npm-strong packages:
print '\n\nKeywords most unilaterally used by npm-strong pacakges:'
new_df.sort_values('diff', ascending=False, inplace=True)
print new_df[:15]

# print keywords that predominantly appear in GitHub-strong packages:
print '\n\nKeywords most unilaterally used by GitHub-strong pacakges:'
new_df.sort_values('diff', ascending=True, inplace=True)
print new_df[:15]