#!/usr/bin/env python

#
# Calculates pagerank over given period of time.
# 
# Input:
# - GT Graph file, e.g., "npm_graph.gt"
# - Start-date (MM-DD-YYYY)
# - End-date (MM-DD-YYYY)
# - Interval (daily, weekly, monthly)
# - Whether to aggregate results in single file (True/False)
# - The number of top packages to focus on
#

import json
import sys
import pytz
import re
import os
import glob
import csv
import time
import pandas as pd

from graph_tool.all import *
from dateutil import rrule, parser


# where results will be stored to:
output_path = '../../data/pageranks/'
# number of results to hold on PER DATE (aggregate may be higher):

def create_pageranks(input_file, start_date, end_date, interval, aggregate_csv, top):
  print 'Perform %s page rank for %s from %s to %s. Aggregate csv: %s. Keep %s top results.' % (interval, input_file, start_date, end_date, aggregate_csv, top)
  
  global output_path
  output_path = output_path + os.path.splitext(input_file)[0].split('/')[-1]

  dates = get_date_range(start_date, end_date, interval)

  # load graph:
  g = load_graph(input_file)
  
  # array of dataframe for pagerank results:
  pr_frames = []

  # array of dataframe for pagerank value results:
  value_frames = []

  # array of dataframe for graph stats:
  stats_frames = []

  # dataframe for in degree:
  in_frames = []

  # dataframe for in degree:
  out_frames = []

  # dataframe for in degree histogram:
  hist_in_frames = []

  # dataframe for out degree histogram:
  hist_out_frames = []

  # dataframe for total degree histogram:
  hist_total_frames = []

  for date in dates:
    print '----------------'
    print 'Filter graph for %s...' % (str(date))
    
    date_long = long(date.strftime("%s")) * 1000
    
    graph_filtered = GraphView(g, 
      vfilt=lambda v: long(g.vp.created[v]) <= date_long, 
      efilt=lambda e: long(g.ep.fromdate[e]) <= date_long and long(g.ep.todate[e]) >= date_long)
    print 'Filtered graph:'
    print ' - Vertices: %s (original=%s)' % (graph_filtered.num_vertices(), g.num_vertices())
    print ' - Edges: %s (original=%s)' % (graph_filtered.num_edges(), g.num_edges())

    # calculate stats:
    stats_df = pd.DataFrame(get_graph_stats(graph_filtered), index=[date])
    stats_frames.append(stats_df)

    # calculate in degrees:
    in_deg_df = pd.DataFrame()
    in_deg_df[date] = pd.Series(get_deg(graph_filtered, 'in'), name=date)
    in_frames.append(in_deg_df)

    # calculate out degrees:
    out_deg_df = pd.DataFrame()
    out_deg_df[date] = pd.Series(get_deg(graph_filtered, 'out'), name=date)
    out_frames.append(out_deg_df)

    # calculate degree histograms:
    in_df = pd.DataFrame()
    in_df[date] = pd.Series(get_deg_hists(graph_filtered, 'in'), name=date)
    hist_in_frames.append(in_df)

    out_df = pd.DataFrame()
    out_df[date] = pd.Series(get_deg_hists(graph_filtered, 'out'), name=date)
    hist_out_frames.append(out_df)

    total_df = pd.DataFrame()
    total_df[date] = pd.Series(get_deg_hists(graph_filtered, 'total'), name=date)
    hist_total_frames.append(total_df)

    # calculate pageranks:
    pageranks = pagerank_top(graph_filtered, top)

    if aggregate_csv:
      # create new dataframe:
      df = pd.DataFrame(pageranks)

      df = df.set_index(['name'])

      # rename 'rank' to the 'date':
      rank_df = df.rename(columns={'rank': date})
      value_df = df.rename(columns={'pr_value': date})

      # add this Series to the overall dataframe:
      pr_frames.append(pd.DataFrame(rank_df[date]).T)

      value_frames.append(pd.DataFrame(value_df[date]).T)
    else:
      save_results_csv(pageranks, date)

  print "=================================================="

  # print pagerank results:
  if aggregate_csv:
    pr_overall_df = pd.concat(pr_frames)
    pr_filepath = '%s_pr_top_%s_%s_%s_%s.csv' % (output_path, top, interval, start_date, end_date)
    pr_overall_df.T.to_csv(pr_filepath)
    print 'Stored overall pagerank results to %s' % (pr_filepath)

    value_overall_df = pd.concat(value_frames)
    value_filepath = '%s_pr-values_top_%s_%s_%s_%s.csv' % (output_path, top, interval, start_date, end_date)
    value_overall_df.T.to_csv(value_filepath)
    print 'Stored overall pagerank values to %s' % (value_filepath)
  else:
    print 'Stored individual pagerank results in %s' % (output_path)

  # print stats results:
  stats_overall_df = pd.concat(stats_frames)
  stats_filepath = '%s_stats_%s_%s_%s.csv' % (output_path, interval, start_date, end_date)
  stats_overall_df.T.to_csv(stats_filepath)
  print 'Stored overall stats to %s' % (stats_filepath)

  # print in deg:
  in_deg_overall_df = pd.concat(in_frames, axis=1)
  in_deg_filepath = '%s_in-deg_%s_%s_%s.csv' % (output_path, interval, start_date, end_date)
  in_deg_overall_df.to_csv(in_deg_filepath)
  print 'Stored in degrees to %s' % (in_deg_filepath)

  # print out deg:
  out_deg_overall_df = pd.concat(out_frames, axis=1)
  out_deg_filepath = '%s_out-deg_%s_%s_%s.csv' % (output_path, interval, start_date, end_date)
  out_deg_overall_df.to_csv(out_deg_filepath)
  print 'Stored out degrees to %s' % (out_deg_filepath)

  # print deg hists:
  hist_in_overall_df = pd.concat(hist_in_frames, axis=1) #.fillna(0).astype(int)
  hist_in_filepath = '%s_hist_in_%s_%s_%s.csv' % (output_path, interval, start_date, end_date)
  hist_in_overall_df.to_csv(hist_in_filepath)
  print 'Stored in degree histogram to %s' % (hist_in_filepath)

  hist_out_overall_df = pd.concat(hist_out_frames, axis=1) #.fillna(0).astype(int)
  hist_out_filepath = '%s_hist_out_%s_%s_%s.csv' % (output_path, interval, start_date, end_date)
  hist_out_overall_df.to_csv(hist_out_filepath)
  print 'Stored out degree histogram to %s' % (hist_out_filepath)

  hist_total_overall_df = pd.concat(hist_total_frames, axis=1) #.fillna(0).astype(int)
  hist_total_filepath = '%s_hist_total_%s_%s_%s.csv' % (output_path, interval, start_date, end_date)
  hist_total_overall_df.to_csv(hist_total_filepath)
  print 'Stored total degree histogram to %s' % (hist_total_filepath)


#
# Calculates some basic statistics for the given graph
# 
def get_graph_stats(graph):
  results = {}

  # number of vertices and edges:
  results['num_vertices'] = graph.num_vertices()
  results['num_edges'] = graph.num_edges()

  # average and std of vertex degrees:
  in_stats = graph_tool.stats.vertex_average(graph, "in")
  results['avg_deg_in'] = in_stats[0]
  results['std_deg_in'] = in_stats[1]

  out_stats = graph_tool.stats.vertex_average(graph, "out")
  results['avg_deg_out'] = out_stats[0]
  results['std_deg_out'] = out_stats[1]

  total_stats = graph_tool.stats.vertex_average(graph, "total")
  results['avg_deg_total'] = total_stats[0]
  results['std_deg_total'] = total_stats[1]

  return results


#
# Calculates histograms of degrees
#
def get_deg_hists(graph, direction):
  results = {}
  hist = graph_tool.stats.vertex_hist(graph, direction)
  for i in range(0, len(hist[0])):
    # print "%s packages have %s rank of %s" % (hist[0][i], direction, hist[1][i])
    results[hist[1][i]] = hist[0][i]
  return results


#
# Gets degree of graph
#
def get_deg(graph, direction):
  results = {}
  if direction == 'in':
    for v in graph.vertices():
      results[graph.vp.name[v]] = v.in_degree()
  elif direction == 'out':
    for v in graph.vertices():
      results[graph.vp.name[v]] = v.out_degree()
  return results


#
# Calculates histogram of distances
#
def get_dist_hist(graph):
  return


#
# Creates a list of dates from the start date to the end date
# with the given interval
#
def get_date_range(start_date, end_date, interval):
  # create dates:
  rule = rrule.DAILY
  if interval == 'daily':
    rule = rrule.DAILY
  elif interval == 'weekly':
    rule = rrule.WEEKLY
  elif interval == 'monthly':
    rule = rrule.MONTHLY
  else:
    print 'Could not identify interval %s. Try daily, weekly, or monthly' % (interval)

  dates = list(rrule.rrule(rule,
                         dtstart=parser.parse(start_date),
                         until=parser.parse(end_date)))
  return dates


#
# Calculates the pagerank for the given graph and returns top n results
#
def pagerank_top(graph, top=100):
  ranking = []

  pr = graph_tool.centrality.pagerank(graph)
  
  for v in graph.vertices():
    # print '%s (%s) has pagerank: %s' % (graph.vp.name[v], graph.vp.version[v], pr[v])
    ranking.append({
      'name': graph.vp.name[v],
      'pr_value': pr[v]
      })

  # sort results by rank:
  ranking = sorted(ranking, key=lambda k: k['pr_value'], reverse=True)

  # cut it:
  ranking = ranking[0:min(top, len(ranking))]

  # hold on to top n results:
  for i in range(0, len(ranking)):
    ranking[i]['rank'] = i + 1

  return ranking


#
# Saves ranking results to CSV file
#
def save_results_csv(results, date):
  # store results under the right date:
  output_file = '%s%s_pagerank.csv' % (output_path, str(date))
  
  keys = results[0].keys()
  with open(output_file, 'wb') as of:
    dict_writer = csv.DictWriter(of, keys)
    dict_writer.writeheader()
    dict_writer.writerows(results)
  print 'Written results to %s' % (output_file)


if __name__=='__main__':
  if len(sys.argv) < 7:
      print 'usage: %s [input_file] [start-date MM-DD-YYYY] [end-date MM-DD-YYYY] [daily / weekly / monthly] [aggregate csv: True/False] [top]' % (sys.argv[0])
      exit(-1)
  aggregate_csv = sys.argv[5] in ['True', 'true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
  create_pageranks(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], aggregate_csv, int(sys.argv[6]))

