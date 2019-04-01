import json
import sys
import pytz
import re
import os
import glob

from graph_tool.all import *

def get_all_graphs(top=25):
  overall_results = {}

  # obtain list of all graph files (*.gt):
  graph_file_list = glob.glob('../../data/gt-graphs-versioned/*.gt')
  
  for file_name in graph_file_list:
    print 'perform page rank for %s' % file_name
    g = load_graph(file_name)
    pr = graph_tool.centrality.pagerank(g)
    results = []
    ranking = []
    for v in g.vertices():
      # print '%s (%s) has pagerank: %s' % (graph.vp.name[v], graph.vp.version[v], pr[v])
      ranking.append({
        'name': g.vp.name[v],
        'version': g.vp.version[v],
        'rank': pr[v]
        })
    ranking = sorted(ranking, key=lambda k: k['rank'], reverse=True)

    # don't try to use 'top' results, if there are not enough results:
    upper_bound = min(len(ranking), top)

    for i in range(0, upper_bound):
      results.append({
        'name':     ranking[i]['name'],
        'version':  ranking[i]['version'],
        'pagerank': ranking[i]['rank'],
        'rank':     i
      })

    # pad missing entries:
    for i in range(upper_bound, top):
      results.append({
        'name':     'NA',
        'version':  'NA',
        'pagerank': 0,
        'rank':     i
      })

    # store results under the right date:
    date = re.search('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]', file_name).group(0) # os.path.splitext(file_name)[0]
    overall_results[date] = results

  outfile = '../../data/top_%s_results.json' % str(top)
  with open(outfile, 'w') as outfile:
    json.dump(overall_results, outfile, sort_keys=True, indent=4)
  print 'results written to %s' % outfile


if __name__=='__main__':
  g = get_all_graphs(5)