from __future__ import print_function
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

#load list with books
with open('parsed_b_list.pickle', 'rb') as handle:
  books_list = pickle.load(handle)

# load titles
with open('titles.pickle', 'rb') as handle:
  titles = pickle.load(handle)

# load vocabulary frame
with open('vocab_frame.pickle', 'rb') as handle:
  vocab_frame = pickle.load(handle)


# load documents distance matrix
with open('terms.pickle', 'rb') as handle:
  terms = pickle.load(handle)

# load tfidf_matrix
with open('-tf-idf_matrix.pickle', 'rb') as handle:
  tfidf_matrix = pickle.load(handle)


#k-means
for KMeans in range(1,10):
  print("******************************\nRunning KMeans...\t...\t...\n******************************")
  from sklearn.cluster import KMeans

  num_clusters = 5
  km = KMeans(n_clusters=num_clusters)
  km.fit(tfidf_matrix)
  clusters = km.labels_.tolist()
  print(clusters)
  print(len(clusters))

  print("******************************\nKMeans results and building data frame ...\t...\t...\n******************************")
  clusters = km.labels_.tolist()
  books = { 'title': titles, 'text': books_list, 'cluster': clusters}
  frame = pd.DataFrame(books, index = [clusters] , columns = ['title', 'cluster'])

  print(frame['cluster'].value_counts()) #number of films per cluster (clusters from 0 to 4)


  print("Top terms per cluster:")
  print()
  #sort cluster centers by proximity to centroid
  order_centroids = km.cluster_centers_.argsort()[:, ::-1] 

  for i in range(num_clusters):
      print("Cluster %d words:" % i, end='')
    
      for ind in order_centroids[i, :50]: #replace 6 with n words per cluster
          if not type(vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0]) is float:
            print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0], end=',')
      print() #add whitespace
      print() #add whitespace
    
      print("Cluster %d titles:" % i, end='')
      for title in frame.ix[i]['title'].values.tolist():
          print(' %s,' % title, end='')
      print() #add whitespace
      print() #add whitespace
  print() #add whitespace
  print() #add whitespace
