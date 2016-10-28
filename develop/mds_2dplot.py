import pickle
import numpy as np
import pandas as pd
import os  
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.manifold import MDS

#load list with books
with open('parsed_b_list.pickle', 'rb') as handle:
  books_list = pickle.load(handle)

# load titles
with open('titles.pickle', 'rb') as handle:
  titles = pickle.load(handle)

# load tfidf_matrix
with open('-tf-idf_matrix.pickle', 'rb') as handle:
  tfidf_matrix = pickle.load(handle)

# load documents distance matrix
with open('-dist.pickle', 'rb') as handle:
  dist = pickle.load(handle)

print("******************************\nRunning KMeans...\t...\t...\n******************************")
from sklearn.cluster import KMeans

num_clusters = 5
km = KMeans(n_clusters=num_clusters)
km.fit(tfidf_matrix)
clusters = km.labels_.tolist()
print(clusters)
print(len(clusters))

print("******************************\nSaving KMeans results...\t...\t...\n******************************")
from sklearn.externals import joblib

joblib.dump(km, 'doc_cluster.pkl')

print("******************************\nLoading KMeans results and building data frame ...\t...\t...\n******************************")
km = joblib.load('doc_cluster.pkl')
clusters = km.labels_.tolist()
books = { 'title': titles, 'text': books_list, 'cluster': clusters}
frame = pd.DataFrame(books, index = [clusters] , columns = ['title', 'cluster'])

print(frame['cluster'].value_counts()) #number of films per cluster (clusters from 0 to 4)

# convert two components as we're plotting points in a two-dimensional plane
# "precomputed" because we provide a distance matrix
# we will also specify `random_state` so the plot is reproducible.
mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)

pos = mds.fit_transform(dist)  # shape (n_components, n_samples)

xs, ys = pos[:, 0], pos[:, 1]
print()
print()


#set up colors per clusters using a dict
cluster_colors = {0: 'g', 1: 'b', 2: 'r', 3: 'm', 4: 'y'}

#set up cluster names using a dict
cluster_names = {0: 'Family, home, war', 
                 1: 'Police, killed, murders', 
                 2: 'Father, New York, brothers', 
                 3: 'Dance, singing, love', 
                 4: 'Killed, soldiers, captain'}


#create data frame that has the result of the MDS plus the cluster numbers and titles
df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=titles)) 

#group by cluster
groups = df.groupby('label')


# set up plot
fig, ax = plt.subplots(figsize=(17, 9)) # set size
ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling

#iterate through groups to layer the plot
#note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
for name, group in groups:
    ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, 
            label=cluster_names[name], color=cluster_colors[name], 
            mec='none')
    ax.set_aspect('auto')
    ax.tick_params(\
        axis= 'x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off')
    ax.tick_params(\
        axis= 'y',         # changes apply to the y-axis
        which='both',      # both major and minor ticks are affected
        left='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelleft='off')
    
#ax.legend(numpoints=1)  #show legend with only 1 point

#add label in x,y position with the label as the film title
for i in range(len(df)):
    ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['title'], size=8)  

    
    
plt.show() #show the plot

#uncomment the below to save the plot if need be
plt.savefig('clusters_small_noaxes.png')







