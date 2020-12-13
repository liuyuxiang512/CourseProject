#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 23:55:57 2020

@author: hongfei7
"""

import gensim
from gensim.summarization import bm25
import os
import heapq
import spacy

# NLTK
from nltk.stem import PorterStemmer

filenames = []

def tokenization(filename):
    result = []
    filepath = "corpus/" + filename
    with open(filepath, 'r') as f:
        text = f.read()
        words = text.split('\t')
        for word in words:
            if word != "":
                result.append(word)
    return result

def read_corpus(dir_path):
    corpus = [];
    for root,dirs,files in os.walk(dir_path):
        for f in files:
            if f == ".DS_Store":
                continue
            corpus.append(tokenization(f))
            #print("file is :" + f)
            new_filename = f.split(".")[0] + ".pdf"
            filenames.append(new_filename)
    print("Corpus size is :" + str(len(corpus)))
    return corpus
    # dictionary = corpora.Dictionary(corpus)
    # print len(dictionary)

if __name__ == "__main__":
    dir_path = 'corpus/'
    
    # BM25 Model
    texts = read_corpus(dir_path)
    bm25Model = bm25.BM25(texts)
    
    # Doc Cosine Similarity
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(doc) for doc in texts]
    
    tf_idf = gensim.models.TfidfModel(corpus)
    index = gensim.similarities.SparseMatrixSimilarity(tf_idf[corpus], num_features=len(dictionary))
    
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    allowed_postags = ['NOUN', 'ADJ', 'VERB', 'ADV']
    
    while True:
        search_type = input("Please input your search type (bm25 or sim): ")
        query_str = input("Please input your query: ")
        
        
        query = []
        for word in query_str.strip().split():
            query.append(word.lower())
        lemmatized = []
        res = nlp(" ".join(query))
        for token in res:
            lemmatized.append(token.lemma_)
        #print(lemmatized)
        # STEMMING
        stemmer = PorterStemmer()
        stemmed = [stemmer.stem(x) for x in lemmatized]
        query = stemmed
        
        if search_type == "bm25":
            scores = bm25Model.get_scores(query)
            
            # get the top 10 indexes
            indexes = heapq.nlargest(10, range(len(scores)), scores.__getitem__)
             
            # get the top 10 values
            values = heapq.nlargest(10,scores)
            
            # print(indexes)
            print(values)
            
            for i in indexes:
                print(filenames[i])

        elif search_type == "sim":
            query_doc_bow = dictionary.doc2bow(query)
            sims = index[tf_idf[query_doc_bow]]
            
            indexes = heapq.nlargest(10, range(len(sims)), sims.__getitem__)
            
            values = heapq.nlargest(10,sims)
            
            # print(indexes)
            print(values)
        
            for i in indexes:
                print(filenames[i])
        else:
            print("Invalid type!\n")
