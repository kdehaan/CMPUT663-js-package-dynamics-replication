#!/usr/bin/env python

#
# Visualizes a table including all Spearman rank correlation coefficients
# between the popularity measures provided in the files list.
# 

import visualize_correlation

top = 1000

# pageranks:
files = [
  {
    'name': 'npm downloads 1 month',
    'path': '../../data/downloads/npm_graph_downloads_2015-08-01_2015-09-01.csv'
  }
  ,
  {
    'name': 'Bipartite pagerank values',
    'path': '../../data/pageranks/apps_graph_bipartite_pr-values_top_300000_daily_09-01-2015_09-01-2015.csv'
  }
  ,
  # {
  #   'name': 'Bipartite pagerank values DEPS only',
  #   'path': '../../data/pageranks/apps_graph_deps_bipartite_pr-values_top_300000_daily_09-01-2015_09-01-2015.csv'
  # }
  # ,
  # {
  #   'name': 'Bipartite pagerank values DEV only',
  #   'path': '../../data/pageranks/apps_graph_dev_bipartite_pr-values_top_300000_daily_09-01-2015_09-01-2015.csv'
  # }
  # ,
  {
    'name': 'npm pagerank values',
    'path': '../../data/pageranks/npm_graph_pr-values_top_300000_daily_09-01-2015_09-01-2015.csv'
  }
  ,
  # {
  #   'name': 'npm pagerank values DEPS only',
  #   'path': '../../data/pageranks/npm_graph_deps_pr-values_top_300000_daily_09-01-2015_09-01-2015.csv'
  # }
  # ,
  # {
  #   'name': 'npm pagerank values DEV only',
  #   'path': '../../data/pageranks/npm_graph_dev_pr-values_top_300000_daily_09-01-2015_09-01-2015.csv'
  # }
  # ,
  # {
  #   'name': 'npm downloads overall',
  #   'path': '../../data/downloads/npm_graph_downloads_2010-01-01_2015-09-01.csv'
  # }
  # ,
  # ,
  # {
  #   'name': 'npm downloads 1 week',
  #   'path': '../../data/downloads/npm_graph_downloads_2015-08-26_2015-09-01.csv'
  # }
]

results = []
for idx in range(0, len(files)):
  if idx < len(files):
    for idx2 in range(idx+1, len(files)):
      f1 = files[idx]['path']
      f2 = files[idx2]['path']
      name1 = files[idx]['name']
      name2 = files[idx2]['name']
      spearman = visualize_correlation.get_correlation(f1, f2, top)
      results.append((name1, name2, spearman))
      print 'Correlation: %s' % (spearman)

results.sort(key=lambda tup: tup[2], reverse=True)

print '\n\nRESULTS (top %s):\n------------' % top
for e in results:
  print '%-35s - %-35s: %s' % (e[0], e[1], e[2])