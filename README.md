# CourseProject

Please fork this repository and paste the github link of your fork on Microsoft CMT. Detailed instructions are on Coursera under Week 1: Course Project Overview.

# Project Proposal
[Proposal.pdf](Proposal.pdf)

# Project Progress Report
[CS410_Progress Report.pdf](CS410_Progress Report.pdf)

# Project Presentation
[Video Presentation](https://youtu.be/PQwRULNWgfc)

# Documentation

## 1. Overview

This project contains two main components. The first part is to identify hot topics in computer science with recent tweets from Twitter. The second one is to find relevant slides of each topic and show the top 10 slides.

### 1.2 Scrawl Slides And Rank Them With Each Topic

- `pdf_download.py`: Scrapes slides from four fixed UIUC course websites which are CS225, CS240, CS425 and CS447. It will download all the PDF documents to a local directory "slides".
- `pdf_miner.py`: Read the slides under the "slides" folder and use pdfminer tool to extract text from the slides. Then, write the raw text to a "txt" file under the folder "raw". For example, if it read a PDF file "slides/Lecture1.pdf", there will be a text file "raw/Lecture1.txt" which contains the text data of the original PDF file.
- `filter_raw.py`: Read the raw text files under the "raw" folder and filter these texts so that they can be used in the following ranking algorithm. It removes the stop words, meaningless numbers and some other useless words. Then, it lemmatizes and stems the words so that derivative words can be treated equally. The results are saved under the "corpus" folder. Each file under this folder represents the abstract of a PDF file from "slides" folder. For example, if it read a text file "raw/Lecture1.txt", there will be a filtered text file "corpus/Lecture1.txt" which contains the cleaned text data.
- `bm25.py`: Read the topic file "topics.json" and generate queries with the distributions of keywords in each topic. Each topic generates one query. Then, for each query, run the bm25 ranking algorithm to calculate the scores of this query to each documents in the "corpus" folder. Finally, get the top 10 documents and write the result to the target file "result/bm25.txt".
- `doc_sim.py`: Similar as "bm25.py". The only difference is the ranking algorithm. It calculates the cosine similarity with TF-IDF weights with each pair of query and document. Then, get the top 10 documents and write the result to the target file "result/sim.txt".

## 2. Implementation

### `pdf_download.py`

This module does the following:

1. Given the course website page, use Soup to extract all the elements with tag "a".
2. Judge the elements whether it is a link which is end with ".txt". If yes, concatenate the prefix and the link to get the complete url.
3. Download the PDF file with its original name and put it into the "slides" folder.

Functions are:

- `getTagA(root_url)`: Obtain all the elements with tag "a" and return a list of string.
- `downPdf(root_url, prefix, list_a)`: Download all the PDF files in the root_url. The argument "prefix" is used to complete the pdf links. It varies with different course websites.
- `getFile(url)`: Get the url file to the "slides" folder.

### `pdf_miner.py`

This module does the following:

1. Read each PDF file under the "slides" folder.
2. Create a PDF Parser for each PDF file. Then parse the pdf file and extract the text data from each page.
3. Write the raw text data to a target file under the folder "raw".

Functions are:

- `parse(filename)`: Extract text data from a PDF file and write it to a target text file (Different PDF files write into different text files).

### `filter_raw.py`

This module does the following:

1. Read each raw text file under the "raw" folder.
2. Tokenlize the text data and remove short words, numbers and stop words from the text.
3. Lemmatize and stem words. Then, write it to a text file under the "corpus" folder (Different raw text files write into different target files).

Functions are:

- `get_raw_data(filepath)`: Read a raw text file and return a list of string. Each element in this list represents a line of data in the raw text file.
- `pre_process(data, filename)`: First, use "re" (regular expression) to remove unwanted words. Second, use "spacy" to lemmatize words and "nltk.stem" to stem words. Finally, write these stemmed words to the target file under the "corpus" folder.

### `bm25.py`

This module does the following:

1. Read the topic file "topics.json" and generate a query based on the distributions of keywords in each topic. For example, if the topic is "{"topic1" : {kewords1 : 0.5, keyword2 : 0.5}}", it will generate a query like "keyword1 keyword1 keyword2 keyword2" which keeps to the distributions.
2. Treat this query as a document and compute the scores of this query to each document in our corpus with the BM25 model implemented by gensim library.
3. Get the top 10 score document names and write the result to the result file "result/bm25.txt".

Functions are:

- `tokenization(filename)`: Read the document under the "corpus" folder and return a list of words in this document.
- `read_corpus(dir_path)`: Read all the documents under the dir_path and return a 2-dimensional list of strings. The first dimension represents each document and the second one contains the words included in each document.
- `simulate_query_by_topics(topic_file)`: Generate queries with topics. In this implementation, it generates query with a word base 100. If we have keyword1 and keyword2 with distribution of 0.2 and 0.5. It will generate a query with 20 keyword1 and 50 keyword2. Node: each topic only reserves top several keywords. Their distributions may not add up to one, but it doesn't affect their relative size.

### `doc_sim.py`:

This module does the following:

1. Read the topic file "topics.json" and generate a query based on the distributions of keywords in each topic. For example, if the topic is "{"topic1" : {kewords1 : 0.5, keyword2 : 0.5}}", it will generate a query like "keyword1 keyword1 keyword2 keyword2" which keeps to the distributions.
2. Treat this query as a document and compute the cosine similarity with TF-IDF weights with each documents under "corpus" folder.
3. Get the top 10 similarity document names and write the result to the result file "result/sim.txt".

Funcrions are the similar to those in "bm25.py".

## 3. Usage

### Installation

This package requires Python 3.0+.
It also requires the following external libraries that can be obtained using:

```bash
pip install bs4
pip install spacy
pip install gensim
pip install pdfminer
pip install pytextrank
python -m spacy download en_core_web_sm
```

Clone the repository from github:

```bash
git clone https://github.com/liuyuxiang512/CourseProject
cd CourseProject
```

### Usage Example

============

补充你的部分

============

Download the slides using the `pdf_download.py`. But it may be slow. You can access the PDF slides with the link: [Download Slides](https://drive.google.com/file/d/1O0I2QJsoPQQTwgrtnuE_40PqFScTNRpv/view?usp=sharing). Then, unzip it to the "slides" folder.

```bash
python3 pdf_download.py
```

Then, we need to extract raw text from PDF files and filter these raw texts.

```bash
python3 pdf_miner.py
python3 filter_raw.py
```

Finally, using `bm25.py` or `doc_sim.py` to calculate the final results. After this step, you can see the result files under the "result" folder.

```bash
python3 bm25.py
python3 doc_sim.py
```

### Other Usage

`main.py`: Users can run this script with python3. It provides 2 kinds of command. (Note: This two commands are available after filtering the raw text).

```bash
python3 main.py
```

1. The first one is "latest". It will automatically run the results with existing topics in "topics.json".
2. The second one is "query". Then it will ask you to type in a query and output 10 files that are most relevant to your query. This ranking list is based on BM25 algorithm because after our mannual evaluation, BM25 ranking performs better than cosine similarity ranking.

`search.py`: Users can run this script with python3. It provides 2 kinds of command. (Note: This two commands are available after filtering the raw text).

```bash
python3 search.py
```

1. The first one is "bm25". It means that the following ranking is based on BM25 algorithm. Then it will ask you to type in a query and output 10 filenames that are most relevant to your query.
2. The second one is "sim". It means that the following ranking is based on document cosine similaritiy. Then it will ask you to type in a query and output 10 filenames that are most relevant to your query.
