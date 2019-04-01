#!/usr/bin/env python

#
# Visualize number of packages maintained by a developer (not same as num devs/package)
# 
# Input: 
# - repos_per_dev_hist.csv

#
import sys
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import FuncFormatter
from collections import OrderedDict

def to_percent(y, position):
  # Ignore the passed in position. This has the effect of scaling the default
  # tick locations.
  s = str(y)

  # The percent symbol needs escaping in latex
  if matplotlib.rcParams['text.usetex'] is True:
    return s + r'$\%$'
  else:
    return s + '%'

def visualize(hist, pp):
  plt.figure()
  plt.clf()
  N = len(hist)
  indexes = np.arange(1,N+1)
  p1 = plt.bar(indexes, hist.values(), 0.4, color='g', alpha=0.5, align='center')

  plt.xlabel("Packages maintained per Developer")
  plt.xticks(indexes , hist.keys())
  plt.xlim(0,N+1)

  plt.ylabel("Percentage of Developers")
  plt.ylim(0,105)
  plt.yticks(np.arange(0,105,10))
  # Create the formatter using the function to_percent. This multiplies all the
  # default labels by 100, making them all percentages
  yformatter = FuncFormatter(to_percent)
  ##trimming the bins to that it doesn't obscure patterns in the lower ends of X range
#  xformatter = FuncFormatter(last_x)
  
  # Set the formatter
  plt.gca().yaxis.set_major_formatter(yformatter)
#  plt.gca().xaxis.set_major_formatter(xformatter)
#  plt.show()

  pp.savefig(plt.gcf())

def calc_bins(input_file):
  bins = { "1" : 0, "2" : 0, "3-5" : 0, ">5" : 0}
  with open(input_file) as fp:
    for line in fp:
      repos = int(line.rstrip('\n').split(',')[1])
      if repos == 1:
        bins['1'] += 1
      elif repos == 2:
        bins['2'] += 1
      elif repos >2 and repos <=5:
        bins['3-5'] += 1
      else:
        bins['>5'] += 1
  total = sum(bins.values())
  for k in bins:
    bins[k] = 100.0 * bins[k]/total
  
  return OrderedDict(sorted(bins.items(), key = lambda t: t[0]))

if __name__=='__main__':
  if len(sys.argv) < 2:
      print 'usage: %s repos_per_dev_hist.csv' % (sys.argv[0])
      exit(-1)
  input_file = sys.argv[1]
  hist = calc_bins(input_file)

  with PdfPages('repos_per_dev_hist.pdf') as pp:
    visualize(hist, pp)
