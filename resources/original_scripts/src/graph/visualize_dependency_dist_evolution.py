#!/usr/bin/env python

#
# Visualize the distribution of dependencies over time.
# Input: a _hist_ csv, e.g., "npm_graph_hist_in_weekly_10-01-2010_09-01-2015.csv"
# Outputfile: npm_deps_in_degree.pdf

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

def visualize_deps_dist(input_file, pp):
  
  agg_min = 9

  df = pd.read_csv(input_file, index_col=0, parse_dates=[0])
  # df.columns = df.columns.to_datetime()
  df.columns = pd.to_datetime(df.columns)

  # replace entries with percent:
  for colKey in df:
    df[colKey] = 100 * df[colKey] / df[colKey].sum()

  # merge columns:
  num_rows = len(df)
  print num_rows
  # label = '> %d' % (agg_min - 1)
  label = '%d or more' % agg_min
  df.loc[label] = df.ix[agg_min:num_rows,:].sum(axis=0)
  ##df.drop(df.iloc[[0:num_rows-2],:])

  df = df.ix[:agg_min].append(df.loc[label])
#  df = df.loc[:,['2015-08-28']]
  plt.figure()
  plt.clf()
  width = 7.0
  plt.rc("figure", figsize=(width, 3.0*width/4.0))

  # plot as area:
  axes = df.T.plot(kind='area')
  axes.set_ylim(0,100)
  axes.set_ylabel("Percentage of Packages in npm")
  axes.set_yticks(range(0, 110, 10))
  
  # plt.gcf().autofmt_xdate()
#  plt.show()
  plt.tight_layout()
  pp.savefig(plt.gcf())


if __name__=='__main__':
  if len(sys.argv) < 3:
      print 'usage: %s <input-data> <output-file>' % (sys.argv[0])
      exit(-1)
  input_file = sys.argv[1]
  output_file = sys.argv[2]

  #npm_deps_out_degree.pdf
  with PdfPages(output_file) as pp:
    visualize_deps_dist(input_file, pp)
