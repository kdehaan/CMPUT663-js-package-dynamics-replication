import json
import sys
import pytz
import re
import os
import glob
import csv

from graph_tool.all import *

def create_pageranks():
  # obtain list of all graph files (*.gt):
  graph_file_list = glob.glob('../../data/graphs/*.gt')

  # determine page rank and store results as CSVs:
  for file_name in graph_file_list:
    print 'perform page rank for %s' % file_name
    
    ranking = []

    g = load_graph(file_name)
    pr = graph_tool.centrality.pagerank(g)
    
    for v in g.vertices():
      # print '%s (%s) has pagerank: %s' % (graph.vp.name[v], graph.vp.version[v], pr[v])
      ranking.append({
        'name_and_version': g.vp.name[v] + '_' + g.vp.version[v],
        'name': g.vp.name[v],
        'version': g.vp.version[v],
        'pr_value': pr[v]
        })

    # sort results by rank:
    ranking = sorted(ranking, key=lambda k: k['pr_value'], reverse=True)

    for i in range(0, len(ranking)):
      ranking[i]['rank'] = i + 1

    # store results under the right date:
    date = re.search('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]', file_name).group(0) # os.path.splitext(file_name)[0]
    output_file = '../../data/pageranks/%s_pagerank.csv' % (date)
    
    keys = ranking[0].keys()
    with open(output_file, 'wb') as of:
      dict_writer = csv.DictWriter(of, keys)
      dict_writer.writeheader()
      dict_writer.writerows(ranking)
    print 'written results of %s to %s' % (file_name, output_file)

  # outfile = 'top_%s_results.json' % str(top)
  # with open(outfile, 'w') as outfile:
  #   json.dump(overall_results, outfile, sort_keys=True, indent=4)
  # print 'results written to %s' % outfile


if __name__=='__main__':
  g = create_pageranks()