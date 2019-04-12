#!/usr/bin/env python
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

df = pd.read_csv('../../data/all_pageranks_simple.csv', index_col=0, parse_dates=0)

print df['underscore']


#repos = ['express', 'connect', 'async']
# repos = ['backbone', 'ember', 'backbone.marionette', 'knockout', 'dojo', 'angular', 'polymer']
repos = ['lodash', 'underscore', 'sugar']
# repos = ['request', 'superagent', 'restler']


ax = df[repos[0]].plot(title='Utility lib wars', logy=True)

for i in range(1, len(repos)):
  df[repos[i]].plot()

ax.legend(repos, loc='lower center')
# reverse y-axis:
plt.gca().invert_yaxis()
plt.gca().set_ybound(lower=0, upper=None)

plt.show()