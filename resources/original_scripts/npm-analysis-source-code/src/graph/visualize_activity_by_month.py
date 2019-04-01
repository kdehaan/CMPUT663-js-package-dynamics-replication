#!/usr/bin/env python

#
# Script to visualize growth of the npm ecosystem w.r.t. histograms of
# new packages/month, updates to packages/month
# 
# Input: 
# - new packages per month:
#     "npm_newpkgs_per_month.csv"
# - updates to packages per month:
#     "npm_updates_per_month.csv"
#
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

def visualize_growth(npm_new, npm_updates, pp):
  df_new = pd.read_csv(npm_new, index_col=0, parse_dates=[0])
  df_new.rename(columns={'newrepos': 'New Packages'}, inplace=True)
  
  df_updates = pd.read_csv(npm_updates, index_col=0, parse_dates=[0])
  df_updates.rename(columns={'updatedrepos': 'Updated Packages'}, inplace=True)

  df_to_plot = df_new[['New Packages']].join(df_updates)

  print df_to_plot

  plt.figure()
  plt.clf()

  width = 5.0
  plt.rc("figure", figsize=(width, 3.0*width/4.0))

  axes = df_to_plot.plot(style=['-','-'], lw=2.0)
  axes.legend(loc='best')
  
  axes.set_ylabel("No. of Packages")
  plt.grid()
  plt.tight_layout()


  pp.savefig(plt.gcf())

if __name__=='__main__':
  if len(sys.argv) < 3:
      print 'usage: %s <new-packages> <updated-packages>' % (sys.argv[0])
      exit(-1)
  npm_new = sys.argv[1]
  npm_updates = sys.argv[2]
  with PdfPages('new_vs_updates_by_month.pdf') as pp:
    visualize_growth(npm_new, npm_updates, pp)
