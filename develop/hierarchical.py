import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
from pprint import pprint as pprint
import mpld3
import pickle
import matplotlib.pyplot as plt
import matplotlib as mpl

# load documents distance matrix
with open('-dist.pickle', 'rb') as handle:
  dist = pickle.load(handle)

# load titles
with open('titles.pickle', 'rb') as handle:
  titles = pickle.load(handle)


# hierarchical clustering
from scipy.cluster.hierarchy import ward, dendrogram

linkage_matrix = ward(dist) #define the linkage_matrix using ward clustering pre-computed distances

fig, ax = plt.subplots(figsize=(15, 20)) # set size
ax = dendrogram(linkage_matrix, orientation="right", labels=titles);

plt.tick_params(\
    axis= 'x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')

plt.tight_layout() #show plot with tight layout

#uncomment below to save figure
plt.savefig('-ward_clusters.png', dpi=200) #save figure as ward_clusters



