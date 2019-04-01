#!/usr/bin/env python
import json
import sys
import pytz
import re
import os

from graph_tool.all import *


def page_rank(graph, top=10):
  pr = graph_tool.centrality.pagerank(graph)
  results = ['\n', 'page rank:', '-------------']
  ranking = []
  for v in graph.vertices():
    # print '%s (%s) has pagerank: %s' % (graph.vp.name[v], graph.vp.version[v], pr[v])
    ranking.append({
      'name': graph.vp.name[v],
      'version': graph.vp.version[v],
      'rank': pr[v]
      })
  ranking = sorted(ranking, key=lambda k: k['rank'], reverse=True)
  for i in range(0, top):
    results.append('%s: %s (%s)' % (ranking[i]['rank'], ranking[i]['name'], ranking[i]['version']))
  return '\n'.join(results)


def get_summary(g):
  results = ['graph summary:', '------------']
  results.append('%s vertices' % g.num_vertices())
  repo_counts = {}
  for v in g.vertices():
    name = g.vp.name[v]
    if name in repo_counts:
      repo_counts[name] += 1
    else:
      repo_counts[name] = 1
  results.append('%s repositories' % len(repo_counts))
  results.append('%s versions / repository (average)' % (g.num_vertices() / len(repo_counts)))
  results.append('%s edges' % g.num_edges())
  return '\n'.join(results)


def get_degree_hist(g, threshold=0.5, deg='total'):
  results = ['\n', '%s degree:' % (deg), '-------------']
  vertex_hist = graph_tool.stats.vertex_hist(g, deg)
  for i in range(0, len(vertex_hist[0])):
    num_vs = vertex_hist[0][i]
    num_deps = vertex_hist[1][i]
    percentage = 100 * num_vs / g.num_vertices()
    if percentage > threshold:
      results.append('%s percent of vertices (%s) have %s %s dependencies' % (percentage, int(num_vs), num_deps, deg))
  results.append('--------------')
  total_vertex_average = graph_tool.stats.vertex_average(g, deg)
  results.append('Average: %s dependencies/repository (STD=%s)' % (total_vertex_average[0], total_vertex_average[1]))
  return '\n'.join(results)


if __name__=='__main__':
  if len(sys.argv) < 2:
      print 'usage: %s [graph_file]' % (sys.argv[0])
      exit(-1)
  input_file = sys.argv[1]

  g = load_graph(input_file)
  
  # print some statistics:
  print get_summary(g)

  print get_degree_hist(g, deg='total')

  print get_degree_hist(g, deg='in')

  print get_degree_hist(g, deg='out')

  # perform pagerank:
  print page_rank(g, 25)

