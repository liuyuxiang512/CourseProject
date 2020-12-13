#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 20:29:13 2020

@author: hongfei7
"""

import gensim
import os
import json
import heapq

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
            new_filename = f.replace(".txt", ".pdf")
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
    
    target_path = "result/"
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    
    output_filename = "result/sim.txt"

    texts = read_corpus(dir_path)
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(doc) for doc in texts]
    
    tf_idf = gensim.models.TfidfModel(corpus)
    # print(tf_idf)
    
    index = gensim.similarities.SparseMatrixSimilarity(tf_idf[corpus], num_features=len(dictionary))
    
    topic_query = simulate_query_by_topics("../Identify_Topics/topics.json")
    
    x = 0
    
    with open(output_filename,'w') as f:
        pass
    
    for topic in topic_query:
        query_str = topic_query[topic]
        print("Query " + str(x) + " is : " + query_str)
        x+=1
        query = []
        for word in query_str.strip().split():
            query.append(word.lower())
        query_doc_bow = dictionary.doc2bow(query)
        sims = index[tf_idf[query_doc_bow]]
        
        indexes = heapq.nlargest(10, range(len(sims)), sims.__getitem__)
         
        values = heapq.nlargest(10,sims)
        
        
        
        #print(indexes)
        print(values)
        
        for i in indexes:
            print(filenames[i])
        
        with open(output_filename,'a') as f:
            f.write("Topic name is: " + topic + "\n")
            f.write("Top 10 slides filename:\n")
            for i in indexes:
                f.write(filenames[i] + "\n")
            f.write("------------------segmentation line-------------------\n")