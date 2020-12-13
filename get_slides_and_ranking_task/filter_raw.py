#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 18:56:53 2020

@author: hongfei7
"""

import re
import os

import spacy

# NLTK
from nltk.stem import PorterStemmer

# Gensim
from gensim.utils import simple_preprocess

def get_raw_data(filepath):
    data = []
    with open(filepath, 'r', encoding='utf-8') as file2read:
        for line in file2read:
            data.append(line)
    return data

nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
allowed_postags = ['NOUN', 'ADJ', 'VERB', 'ADV']

def pre_process(data, filename):
    # prepare stopwords file
    with open("stopwords.txt", "r") as file:
        stopwords = file.read().strip().split("\n")
    #print(stopwords)
    
    output_filename = "corpus/" + filename
    all_words = []
    for text in data:
        text = text.lower()
        #print("Before :" + text)
        text = re.sub(r"@\S+", "", text)
        text = re.sub(r"#\S+", "", text)
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"[^a-zA-Z']", " ", text)
        tidy_text = " ".join([word for word in text.split() if len(word) >= 3])
        tidy_text_tokens = [(simple_preprocess(str(word), deacc=True) + [word])[0] for word in tidy_text.split()]
        tokens_no_stop = [word for word in tidy_text_tokens if word not in stopwords]
        
        all_words.extend(tokens_no_stop)
    lemmatized = []
    res = nlp(" ".join(all_words))
    for token in res:
        lemmatized.append(token.lemma_)
    #print(lemmatized)
    # STEMMING
    stemmer = PorterStemmer()
    stemmed = [stemmer.stem(x) for x in lemmatized]
    
    # clean the old file
    with open(output_filename,'w') as f:
        pass
    
    with open(output_filename,'a') as f:
        for token in stemmed:
            f.write(token  +"\t")
        
if __name__ == "__main__":
    path = "raw/"
    
    target_path = "corpus/"
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    
    files= os.listdir(path)
    for file in files:
        if not os.path.isdir(file):
            print("Start to deal with file:"+file)
            try:
                data = get_raw_data(path + file)
                pre_process(data, file)
            except:
                print("Parse："+file + "Error")
    
    
        
