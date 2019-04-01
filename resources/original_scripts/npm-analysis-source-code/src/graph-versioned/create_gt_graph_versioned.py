#!/usr/bin/env python
import json
import sys
import pytz
import re
import os

from graph_tool.all import *


def create_graph(input_file):
  print '--------------'
  fake_graph = load_data(input_file)
  graph = construct_graph(fake_graph)
  save_graph(graph, input_file)


# loads the fake graph and returns it as dict:
def load_data(input_file):
  print 'read input data at %s...' % (input_file)
  with open(input_file) as f:    
    return json.load(f)


def save_graph(graph, input_file):
  # save the graph:
  output_file = '../../data/gt-graphs/' + os.path.splitext(input_file)[0].split('/')[-1] + '.gt'
  graph.save(output_file, fmt='gt')
  print 'done. graph saved to "%s"' % (output_file)


def construct_graph(fake_graph):
  print 'start creating graph...'
  # graph variables:
  g = Graph()
  vprop_name = g.new_vertex_property('string')
  vprop_version = g.new_vertex_property('string')

  # store properties to graph:
  g.vertex_properties["name"] = vprop_name
  g.vertex_properties["version"] = vprop_version

  vprop_dependencies = g.new_vertex_property('object')
  vprop_dev_dependencies = g.new_vertex_property('object')

  # dict to store 'name_version' <> vertex_id:
  id_map = {}

  # add vertices to graph:
  print 'add vertices...'
  for repo_key in fake_graph:
    for version_key in fake_graph[repo_key]:
      v = g.add_vertex()
      vprop_name[v] = repo_key
      vprop_version[v] = version_key

      # hold on to vertex for later edge creation:
      id_map[repo_key + '_' + version_key] = v
      
      try:
        vprop_dependencies[v] = fake_graph[repo_key][version_key]['dependencies']
      except KeyError:
        continue
      try:
        vprop_dev_dependencies[v] = fake_graph[repo_key][version_key]['devDependencies']
      except KeyError:
        continue
  
  # add edges to graph:
  print 'add edges...'
  for v in g.vertices():
    name = vprop_name[v]
    if vprop_dependencies[v]:
      for dep_key in vprop_dependencies[v]:
        try:
          id = dep_key + '_' + str(vprop_dependencies[v][dep_key])
          g.add_edge(v, id_map[id])
        except KeyError:
          continue
        except TypeError:
          print 'Wrong type %s when adding dependency %s for repository %s. Value: \n %s' \
            % (type(vprop_dependencies[v][dep_key]), dep_key, name, vprop_dependencies[v][dep_key])

  return g


if __name__=='__main__':
    if len(sys.argv) < 2:
        print 'usage: %s [input_file]' % (sys.argv[0])
        exit(-1)
    input_file = sys.argv[1]

    create_graph(input_file)
