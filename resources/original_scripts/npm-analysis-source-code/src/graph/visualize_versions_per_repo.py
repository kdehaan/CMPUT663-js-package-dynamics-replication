#!/usr/bin/env python

#
# Script to visualize growth of packages vs number of contributors on a
# month by month basis
# 
# Input: 
# - devs_and_versions_per_repo.csv

#
import sys
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import FuncFormatter


def to_percent(y, position):
  # Ignore the passed in position. This has the effect of scaling the default
  # tick locations.
  s = str(100 * y)

  # The percent symbol needs escaping in latex
  if matplotlib.rcParams['text.usetex'] is True:
    return s + r'$\%$'
  else:
    return s + '%'

def last_x(x, position):
  # Ignore the passed in position. This has the effect of scaling the default
  # tick locations.
  if (x < 100):
    s = str(x)
  else:
    s = ">=100"
  return s

def visualize_growth(input_file, pp):
  df = pd.read_csv(input_file, index_col=0).T
  
  plt.figure()
  plt.clf()

  axes=df['Versions'].hist(bins=100,range=(1,100), normed=1,alpha=0.5,cumulative=True,lw=1.5,histtype='step')
  axes.set_ylabel("Percentage of Packages")
  axes.set_xlabel("Number of Versions")
  axes.set_ylim(0,1.05)
  axes.set_xlim(0,110)
  axes.set_xticks(range(0,110,10))

  # Create the formatter using the function to_percent. This multiplies all the
  # default labels by 100, making them all percentages
  yformatter = FuncFormatter(to_percent)
  ##trimming the bins to that it doesn't obscure patterns in the lower ends of X range
  xformatter = FuncFormatter(last_x)
  
  # Set the formatter
  plt.gca().yaxis.set_major_formatter(yformatter)
  plt.gca().xaxis.set_major_formatter(xformatter)
#  plt.show()

  pp.savefig(plt.gcf())

if __name__=='__main__':
  if len(sys.argv) < 2:
      print 'usage: %s devs_versions_per_repo_hist.csv' % (sys.argv[0])
      exit(-1)
  input_file = sys.argv[1]
  with PdfPages('versions_per_repo_hist.pdf') as pp:
    visualize_growth(input_file, pp)
