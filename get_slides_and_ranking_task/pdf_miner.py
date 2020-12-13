#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 12:50:06 2020

@author: hongfei7
"""
import importlib
import sys
import time
 
importlib.reload(sys)
time1 = time.time()
 
import os.path
from pdfminer.pdfparser import  PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

 
def parse(filename):
    '''Parse PDF documents'''
    
    try:
        print("Parsing " + filename)
        prefix = "slides/"
        fp = open(prefix + filename,'rb')
        # Create a PDF Parser
        parser = PDFParser(fp)
        doc = PDFDocument()
        parser.set_document(doc)
        doc.set_parser(parser)
        doc.initialize()
     
        # If doc is extractable, do it. If not, pass.
        if not doc.is_extractable:
            print("Not Allowed!")
            raise PDFTextExtractionNotAllowed
        else:
            rsrcmgr = PDFResourceManager()
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr,laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr,device)
            
            splits = filename.split(".")
            output_filename = "raw/" + splits[0] + ".txt"
            
            # clean the original file
            with open(output_filename,'w') as f:
                pass
     
            for page in doc.get_pages():
                interpreter.process_page(page)
                layout = device.get_result()

                for x in layout:
                    if(isinstance(x,LTTextBoxHorizontal)):
                        with open(output_filename,'a') as f:
                            results = x.get_text()
                            # print(results)
                            f.write(results  +"\n")
    except:
        print("Parse " + filename + " Error")

if __name__ == '__main__':
    path = "slides/" # slides dir
    
    target_path = "raw/"
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    
    files= os.listdir(path)
    for file in files:
         if not os.path.isdir(file):
             parse(file)
    time2 = time.time()
    print("Total consumed time: ",time2-time1)
