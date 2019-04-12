#!/usr/bin/env python
import glob
import create_graph as g

if __name__=='__main__':
  fake_graph_list = glob.glob('../../data/json-graphs/*.json')
  for fake_graph_path in fake_graph_list:
    print fake_graph_path
    g.create_graph(fake_graph_path)