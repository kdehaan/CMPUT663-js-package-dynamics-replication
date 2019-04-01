#!/usr/bin/env python

#
# Filters repositories identified via GHTorrent for ones that are not
# packages on npm.
#

import json
import re

npm_data = json.load(open('../../data/2015-09-22_npm_skim.json'))
gh_data = json.load(open('../../data/ghtorrent-js-repos.json'))

# print 'done reading data'

npm_git_repos = []
for repo in npm_data:
  if 'value' in repo:
    if 'repository' in repo['value'] and repo['value']['repository']:
      if 'url' in repo['value']['repository']:
        url = repo['value']['repository']['url']
        
        m = re.match(""".*github.com/([^/]*)/([^/]*)""", url)

        if m is not None:
          user_part = m.group(1)
          repo_part = m.group(2)

          if repo_part[-4:] == '.git':
            repo_part = repo_part[:-4]

        # print (user_part, repo_part)


        npm_git_repos.append(user_part + '/' + repo_part) 

# print 'found %s Git repos in npm data' % (len(npm_git_repos))
npm_git_set = set(npm_git_repos)


gh_set = set()
for gh in gh_data:
  gh_set.add(gh['full_name'])
# print 'found %s unique Git repos in GH data' % (len(gh_set))

diff = gh_set - npm_git_set
# print 'found %s repos in GH that are NOT in npm' % (len(diff))

print gh_set.intersection(npm_git_set)

# for e in diff:
#   print e