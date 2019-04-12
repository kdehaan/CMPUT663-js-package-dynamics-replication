#!/usr/bin/env python

#
# Script to visualize growth of packages vs number of contributors on a
# month by month basis
# 
# Input: 
# - repos_and_devs_by_month.csv

#
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def visualize_growth(input_file, pp):
  df = pd.read_csv(input_file, index_col=0, parse_dates = [0]).T
  
  plt.figure()
  plt.clf()

  axes = df.plot(style=['-','--'], lw=2.0)
  axes.legend(loc='best')
  
  #  plt.tight_layout()
  #  plt.show()
  plt.gcf().autofmt_xdate()
  axes.set_ylabel("Count")
  axes.set_xlabel("Time")

  pp.savefig(plt.gcf())

if __name__=='__main__':
  if len(sys.argv) < 2:
      print 'usage: %s repos_and_devs_per_month.csv' % (sys.argv[0])
      exit(-1)
  input_file = sys.argv[1]
  with PdfPages('repos_and_devs_per_month.pdf') as pp:
    visualize_growth(input_file, pp)
