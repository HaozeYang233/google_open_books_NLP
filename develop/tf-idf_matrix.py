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

# check the list of books
with open('parsed_b_list.pickle', 'rb') as handle:
  b_list = pickle.load(handle)

print "Number of books..."
print len(b_list)

print "Number of words in each book..."
for b in b_list:
	print len(b.split())


# tokenizer
# load nltk's English stopwords as variable called 'stopwords'
stopwords = nltk.corpus.stopwords.words('english')
# load nltk's SnowballStemmer as variabled 'stemmer'
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")

def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    stems = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            if token not in stopwords:
                filtered_tokens.append(token)
    for t in filtered_tokens:
        stemmer.stem(t).encode("ascii", errors="ignore")
        stems.append(t)
    return stems


# compute tf - idf matrix
print "building TF-IDF matrix..."
from sklearn.feature_extraction.text import TfidfVectorizer
#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2, stop_words='english',
                                 use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(b_list) #fit the vectorizer to book list

pprint(tfidf_matrix)

print tfidf_matrix

terms = tfidf_vectorizer.get_feature_names()

pprint(terms[:25])

# save tfidf
print '******************************\nSAVING...\t...\t...\n******************************'
with open('00tf-idf_matrix.pickle', 'wb') as handle:
    pickle.dump(tfidf_matrix, handle)

# save terms: list of features used in the tf-idf matrix
with open('00terms.pickle', 'wb') as handle:
    pickle.dump(terms, handle)

# compute similarity
print "building SIMILARITY MATRIX..."
# compute cosine similarity and distance (1-cos_sim) for the documents: DIT, number included in (0, 1) the bigger is the more similar
from sklearn.metrics.pairwise import cosine_similarity
dist = 1 - cosine_similarity(tfidf_matrix)

# save similarity matrix
print '******************************\nSAVING...\t...\t...\n******************************'
with open('00dist.pickle', 'wb') as handle:
    pickle.dump(dist, handle)









