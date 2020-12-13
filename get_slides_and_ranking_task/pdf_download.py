#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 15:25:19 2020

@author: maye
"""

from bs4 import BeautifulSoup as Soup
import requests
import urllib.request
import os

def getTagA(root_url):
    print("start to get " + root_url)
    res = requests.get(root_url)
    soup = Soup(res.text,'html.parser')
    temp = soup.find_all("a")
    return temp


def getFile(url):
    file_name = url.split('/')[-1]
    try:
        u = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        print(url, "url file not found")
        return
    block_sz = 8192
    with open(file_name, 'wb') as f:
        while True:
            buffer = u.read(block_sz)
            if buffer:
                f.write(buffer)
            else:
                break
   
    print ("Sucessful to download" + " " + file_name)

def downPdf(root_url, prefix, list_a):
    print("list a is :\n")
    print(list_a)
    number = 0

    if not root_url.endswith("/"):     
        index = root_url.rfind("/")
        root_url = root_url[:index+1]
    for name in list_a:
        name02 = name.get("href")
        if name02 == None:
            continue
        if name02.startswith("http"):
            continue
        if name02.startswith("."):
            name02 = name02[1:]
        ## get those pdf links
        if name02.lower().endswith(".pdf"):
            print("name02 is " + name02)
            splits = name02.split("/")
            pdf_name = splits[-1]
            print("pdf_name是：" + pdf_name)
            number += 1
            print("Download the %d pdf immdiately!!!"%number,end='  ')
            print(pdf_name+'downing.....') 
            
            pdf_url = prefix + name02
            response = requests.get(pdf_url,stream="TRUE")
            print("pdf url is: " + pdf_url)
            path = "slides/" + pdf_name
            with open(path,'wb') as file:
                for data in response.iter_content():
                    file.write(data)

if __name__ == "__main__":
    urls = ["https://courses.engr.illinois.edu/cs425/fa2020/lectures.html", "https://courses.grainger.illinois.edu/CS447/fa2020/", 
            "https://courses.grainger.illinois.edu/cs225/fa2020/pages/lectures.html", "https://courses.grainger.illinois.edu/cs240/fa2020/schedule/"]
    prefix = ["https://courses.engr.illinois.edu/cs425/fa2020/", "https://courses.grainger.illinois.edu/cs438/fa2020/slides/", 
              "https://courses.grainger.illinois.edu/CS447/fa2020/", "https://courses.grainger.illinois.edu"]
    
    target_path = "slides/"
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    
    for i in range(4):
        downPdf(urls[i], prefix[i], getTagA(urls[i]))

