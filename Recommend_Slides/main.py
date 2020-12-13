#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 03:21:18 2020

@author: hongfei7
"""

import gensim
from gensim.summarization import bm25
import os
import json
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

def simulate_query_by_topics(topic_file):
    ret = {}
    topics = []
    max_len = 100
    x = 0
    with open(topic_file, 'r', encoding='utf-8') as file2read:
        for line in file2read:
            obj = json.loads(line)
            res = ""
            for topic in obj:
                keywords = obj[topic]
                topics.append(topic)
                for word in keywords:
                    distribution = keywords[word]
                    num_of_word = int(max_len * distribution)
                    for i in range (num_of_word):
                        res = res + " " + word
                res = res[1:]
                ret[topic] = res
            x+=1
    return ret

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
        command_type = input("Please input your command type (query or latest): ")
        
        if command_type == "query":
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
            
            scores = bm25Model.get_scores(query)
            
            # get the top 10 indexes
            indexes = heapq.nlargest(10, range(len(scores)), scores.__getitem__)
             
            # get the top 10 values
            values = heapq.nlargest(10,scores)
            
            print("The top 10 relative slides are: \n")
            
            for i in indexes:
                print(filenames[i])
                
        elif command_type == "latest":
            topic_query = simulate_query_by_topics("../Identify_Topics/topics.json")
            output_filename = "result/bm25.txt"
            with open(output_filename,'w') as f:
                pass
            
            for topic in topic_query:
                query_str = topic_query[topic]
                # print("Query " + str(x) + " is : " + query_str)
                # x+=1
                query = []
                for word in query_str.strip().split():
                    query.append(word.lower())
                scores = bm25Model.get_scores(query)
                
                # get the top 10 indexes
                indexes = heapq.nlargest(10, range(len(scores)), scores.__getitem__)
                 
                # get the top 10 values
                values = heapq.nlargest(10,scores)
                
                with open(output_filename,'a') as f:
                    f.write("Topic name is: " + topic + "\n")
                    print("Topic name is: " + topic + "\n")
                    f.write("Top 10 slides filename:\n")
                    print("Top 10 slides filename:\n")
                    for i in indexes:
                        f.write(filenames[i] + "\n")
                        print(filenames[i])
                    f.write("------------------segmentation line-------------------\n")
                    print("------------------segmentation line-------------------")
        else:
            print("Invalid command!\n")
