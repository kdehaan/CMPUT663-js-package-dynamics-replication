#!/usr/bin/env python

#
# Visualizes the dependency graph at a certain point in time using graph-tool.
# 
# Input:
# - GT Graph to visualize, e.g., "npm_graph.gt"
# - Date for when to create the graph visualization, e.g., "01-01-2010"
#
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter
from graph_tool.all import *
from dateutil import parser

def visualize_dep_graph(input_file, date_str):
  # load graph:
  g = load_graph(input_file)

  # parse given date:
  date = parser.parse(date_str)

  # filter the graph for that date:
  print 'Filter graph for %s...' % (str(date))  
  date_long = long(date.strftime("%s")) * 1000
  
  graph_filtered = GraphView(g, 
    vfilt=lambda v: long(g.vp.created[v]) <= date_long, 
    efilt=lambda e: long(g.ep.fromdate[e]) <= date_long and long(g.ep.todate[e]) >= date_long)
  print 'Filtered graph:'
  print ' - Vertices: %s (original=%s)' % (graph_filtered.num_vertices(), g.num_vertices())
  print ' - Edges: %s (original=%s)' % (graph_filtered.num_edges(), g.num_edges())

  # visualize it:
  
  # vertex properties:
  vprops = {
    'shape': 'circle', # shape of the vertices
    'size': 1,
    'pen_width': 0.1
  }

  # vertex sizes as function of pagerank value:
  deg = graph_tool.centrality.pagerank(graph_filtered)
  deg.a = np.sqrt(deg.a) * 100 + 0.2 # use numpy for square root!!!
  
  # vertex positioning:
  print 'determine vertex positioning...'
  pos = graph_tool.draw.arf_layout(graph_filtered, max_iter=500)

  # edge properties:
  eprops = {
    'color': [0.4, 0.4, 0.4, 0.4], # color in rgbt, the lower the last number, the more transparent
    'start_marker': 'none',
    'end_marker': 'arrow',
    'pen_width': 0.3
  }

  # draw it using cairo:
  print 'draw graph...'
  graph_draw(graph_filtered,
    pos=pos,
    vprops=vprops,
    vertex_size=deg, 
    eprops=eprops,
    output="dependency_graph_" + str(date).split(' ')[0] + ".pdf")

  # graphviz_draw(graph_filtered, output="viz_dependency_graph_" + str(date).split(' ')[0] + ".pdf")

if __name__=='__main__':
  if len(sys.argv) < 3:
      print 'usage: %s [input_file] [date MM-DD-YYYY]' % (sys.argv[0])
      exit(-1)
  input_file = sys.argv[1]
  date_str = sys.argv[2]
  visualize_dep_graph(input_file, date_str)