# `npm` analysis over time

This repository contains code to analyze the `npm` ecosystem over time.


## Obtaining data

The npm data can be loaded using:

    node load-npm-data.js

This will produce two files:

1. `201X-XX-XX_npm_skim.json` contains a list of all repositories. This data is retrieved from <https://skimdb.npmjs.com/registry/_design/scratch/_view/byField>.

2. `201X-XX-XX_npm_repos.txt` contains per line a stringified JSON object denoting all npm metadata for one repository. This makes it easier for the subsequent Python scripts to deal with the data (Python's support for streaming JSON data is lacking).


## Creating graph snapshots

There are 2 ways to create graph snapshots.


### A) Create graph for one point in time

Create JSON snapshot of a graph for certain `date` in time (e.g., `2011-01-01`):

    node graph-snapshot.js <input-path> <date> <simple>

The `input-path` should point to a file where every line contains JSON encoded information on a single package as provided by npm (e.g., <https://registry.npmjs.org/express>). 
`simple` can be `true` or `false`. If `true`, the graph will only consider the latest version of every package at the specified date and dependencies will be resolved based on the name of packages only (no consideration of version numbers).

Next, turn the snapshot into a python-readable graph:

    python create-graph.py <input-path>

The graph will be stored in `.gt` format.


### B) Create graph for interval

Create multiple JSON snapshots for a period using:

    node graph-snapshots.js <input-path> <start-date> <end-date> <simple>

## Analyze graph

    python analyze-graph.py ./data/graph.gt



## Getting history of `package.json` files on GitHub:

1. Find `package.json` files via HTML (search for 'dependencies'): 
   
   <https://github.com/search?q=dependencies+filename:package.json+language:json+path:/&ref=searchresults&type=Code>
 
=> (only the first 1000 are available!!!)


1. Alternative: list all JavaScript repositories:

   <https://api.github.com/search/repositories?q=+language:javascript&sort=stars&order=desc>

   ...and check availability of package.json:

   <https://raw.githubusercontent.com/caolan/async/master/package.json>

  Store: {"owner": "caolan", "repository": "async"}

=> (only the first 1000 are available!!!)


1. Go through all repos in <http://ghtorrent.org/downloads/repos-dump.2015-03-29.tar.gz>.
   Look for "language=JavaScript".
   Check if package.json exists: <https://raw.githubusercontent.com/caolan/async/master/package.json>


2. Obtain commit history: 

   <https://api.github.com/repos/caolan/async/commits?path=package.json>. Includes commit SHA!


3. Download file at commit: 

   <https://raw.githubusercontent.com/request/request/cfa81645c9cb4011b23d1d1a445ad855762568e0/package.json>