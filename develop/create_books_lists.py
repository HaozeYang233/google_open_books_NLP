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
# load nltk's English stopwords as variable called 'stopwords'
stopwords = nltk.corpus.stopwords.words('english')
# load nltk's SnowballStemmer as variabled 'stemmer'
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")


#N.B. Stemming does not reduce the number of the words!!!! It just change and keep the significative part.
#EX.
############## stemmed
# ['latham', 'late', 'fellow', 'of', 'king', 'colleg', 'cambridg', 'georg', 'long', 'late', 'fellow', 'of', 'triniti', 'colleg', 'cambridg', 'william', 'ramsay', 'professor', 'of', 'human', 'in', 'the', 'univers', 'of', 'glasgow', 'ft', 'john', 'robson', 'of', 'the', 'univers', 'of', 'london', 'leonhahd', 'schmitz', 'ph', 'll', 'rector', 'of', 'the', 'high', 'school', 'of', 'edinburgh', 'ccs', 'charl', 'roach', 'smith', 'sl', 'philip']
############## tokens only
# ['latham', 'late', 'fellow', 'of', 'king', 'college', 'cambridge', 'george', 'long', 'late', 'fellow', 'of', 'trinity', 'college', 'cambridge', 'william', 'ramsay', 'professor', 'of', 'humanity', 'in', 'the', 'university', 'of', 'glasgow', 'ft', 'john', 'robson', 'of', 'the', 'university', 'of', 'london', 'leonhahd', 'schmitz', 'ph', 'll', 'rector', 'of', 'the', 'high', 'school', 'of', 'edinburgh', 'ccs', 'charles', 'roach', 'smith', 'sl', 'philip']
def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    stems = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            if token not in stopwords:
                if len(token) > 3:
                    filtered_tokens.append(token)
    for t in filtered_tokens:
        stemmer.stem(t).encode("ascii", errors="ignore")
        if len(t) > 3:
            stems.append(t)
    return stems


if __name__ == '__main__':

    # get paths to files
    baseFolder = '/Users/nicolavitale/Desktop/DataMining-COMP6237/Individual/Data/gap-txt'
    for rSDir, rDirs, rFiles in os.walk(baseFolder): 
        paths = []
        for txt in rFiles:
            paths.append(os.path.join(baseFolder, txt))
        #pprint(paths)

    # process each file and save it as a pickle object
    # list of just parsed books
    parsed_b_list = []
    for f in paths:  
        print '******************************\nProcessing...\t\t\t' + f + '\n******************************'
        with open(f, 'r') as myfile:
            myfile = myfile.read() # .replace('\n', '')
            # stemmed_file = tokenize_and_stem(myfile)
            # string_file = ' '.join(stemmed_file)
            parsed_b_list.append(myfile)

    print '******************************\nSAVING...\t...\t...\n******************************'
    with open('parsed_b_list.pickle', 'wb') as handle:
        pickle.dump(parsed_b_list, handle)


    # list of stemmed and cleaned books (passed to the function)
    stem_cl_b_list = []
    for f in paths:  
        print '******************************\nProcessing...\t\t\t' + f + '\n******************************'
        with open(f, 'r') as myfile:
            myfile = myfile.read() # .replace('\n', '')
            stemmed_file = tokenize_and_stem(myfile)
            string_file = ' '.join(stemmed_file)
            stem_cl_b_list.append(myfile)

    print '******************************\nSAVING...\t...\t...\n******************************'
    with open('stem_cl_b_list.pickle', 'wb') as handle:
        pickle.dump(stem_cl_b_list, handle)



 