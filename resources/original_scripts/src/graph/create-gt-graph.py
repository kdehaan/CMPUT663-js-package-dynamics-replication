#!/usr/bin/env python

#
# Creates a .gt graph (graph-tool) from given JSON graph.
# The JSON graph is expected to be a JSON object of the following form:
# 
# {
#   "package_a": {
#     "creationDate": 1359595266159,
#     "deps": {
#       "package_b": [
#         {
#           "from": 1359595266159,
#           "to": 1500000000000
#         },
#         ...
#       ]
#     },
#     ...
#   },
#   ...
# }
#

import json
import sys
import pytz
import re
import os

from graph_tool.all import *


def create_graph(input_file, do_bipartite):
  print '--------------'
  fake_graph = load_data(input_file)
  print 'loaded graph with %s nodes' % (len(fake_graph))
  graph = construct_graph(fake_graph, do_bipartite)
  print 'created graph with %s nodes and %s edges' % (graph.num_vertices(), graph.num_edges())
  save_graph(graph, input_file, do_bipartite)


# loads the fake graph and returns it as dict:
def load_data(input_file):
  print 'read input data at %s...' % (input_file)
  with open(input_file) as f:    
    return json.load(f)


def save_graph(graph, input_file, do_bipartite):
  # save the graph:
  output_file = '../../data/gt-graphs/' + os.path.splitext(input_file)[0].split('/')[-1] + '.gt'
  if do_bipartite:
    output_file = '../../data/gt-graphs/' + os.path.splitext(input_file)[0].split('/')[-1] + '_bipartite.gt'
  graph.save(output_file, fmt='gt')
  print 'done. graph saved to "%s"' % (output_file)


def construct_graph(fake_graph, do_bipartite):
  print 'start creating graph...'
  # graph variables:
  g = Graph()
  vprop_name = g.new_vertex_property('string')
  vprop_created = g.new_vertex_property('string')
  eprop_from = g.new_edge_property('long')
  eprop_to = g.new_edge_property('long')

  # store properties to graph:
  g.vertex_properties["name"] = vprop_name
  g.vertex_properties["created"] = vprop_created
  g.edge_properties["fromdate"] = eprop_from
  g.edge_properties["todate"] = eprop_to

  vprop_dependencies = g.new_vertex_property('object')


  # add vertices to graph:
  print 'add vertices...'
  id_map = {}
  
  # add vertices from npm, if you desire a bipartite graph:
  if do_bipartite:
    npm_fake_graph = load_data('../../data/json-graphs/npm_graph.json')
    for repo_key in npm_fake_graph:
      v = g.add_vertex()
      vprop_name[v] = repo_key
      vprop_created[v] = npm_fake_graph[repo_key]['creationDate']

      # hold on to vertex for later edge creation:
      id_map[repo_key] = v
  
  # add actual vertices
  for repo_key in fake_graph:
    v = g.add_vertex()
    vprop_name[v] = repo_key
    vprop_created[v] = fake_graph[repo_key]['creationDate']

    # hold on to vertex for later edge creation:
    id_map[repo_key] = v
  print '  %s nodes were added' % (len(id_map))
  
  # add edges to graph:
  print 'add edges...'
  num_added = 0
  num_failed = 0
  for repo_key in fake_graph:
    for dep_key in fake_graph[repo_key]['deps']:
      for dates in fake_graph[repo_key]['deps'][dep_key]:
        try:
          e = g.add_edge(id_map[repo_key], id_map[dep_key])
          eprop_from[e] = long(dates['from'])
          eprop_to[e] = long(dates['to'])
          num_added += 1
        except KeyError:
          num_failed += 1
  print '  %s edges were added, %s failed' % (num_added, num_failed)
  return g


if __name__=='__main__':
  if len(sys.argv) < 3:
      print 'usage: %s [input_file] [bipartite graph?]' % (sys.argv[0])
      exit(-1)
  input_file = sys.argv[1]
  do_bipartite = sys.argv[2] in ['True', 'true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']

  create_graph(input_file, do_bipartite)
