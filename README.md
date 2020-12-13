# CourseProject

Final Project for CS410 of UIUC.

# Project Proposal
[Proposal.pdf](Proposal.pdf)

# Project Progress Report
[Progress_Report.pdf](CS410_Progress_Report.pdf)

# Project Presentation
[Video Presentation](https://youtu.be/PQwRULNWgfc)

# Documentation

## 1. Overview

This project consists of two major tasks. 
The first one is to identify emerging topics in Twitter within computer science field, 
and the second one is to recommend relevant slides of the given topics.

### 1.1 Identify Emerging Topics
In this task, we first crawled 680k tweets from Twitter with query "computer science", 
which limited our scale of topics.
Then, in order to mine topics from these tweets, we found the optimal number of topics w.r.t. 
coherence value and trained the LDA topic model with the optimal number of topics. 
Finally, we visualized topics with word cloud by analyzing hashtags.
Besides, we support identifying emerging topics by crawling the latest tweets 
and predicting their topics with pre-trained LDA model, 
while these newly crawled data is used to update our LDA model.

All related files are in `Identify_Topics/` directory.
- `Crawling/`: Keep crawling tweets and form training data.
- `data/`: Store raw data ([`sorted_tweets.json`](https://drive.google.com/file/d/1tGOrF_OCt_4XRY9G-8JoTAM_cQLGoeh_/view?usp=sharing)), processed data (`pre-processed.pkl`), stopwords (`stopwords.txt`), and pictures of topics (`topic_desc_fig/`).
- `model`: Store pre-trained LDA model files.
- `topic_discovery.py`: 
Extract topics from crawled tweets, 
evaluate models with different number of topics to find the optimal, 
get topics and draw pictures for them with word cloud,
and predict emerging topics based on pre-trained model.
- `topics.json`: Word distributions of topics, which will feed into next part.

### 1.2 Recommend Slides for Topics
In this task, we first crawled 100+ course slides in UIUC. 
Then, taking the above word distributions of different topics as input, we used BM25 to find relevant slides.

All related files are in `Recommend_Slides/` directory.
- `pdf_download.py`: Scrapes slides from four fixed UIUC course websites which are CS225, CS240, CS425 and CS447. It will download all the PDF documents to a local directory "slides".
- `pdf_miner.py`: Read the slides under the "slides" folder and use pdfminer tool to extract text from the slides. Then, write the raw text to a "txt" file under the folder "raw". For example, if it read a PDF file "slides/Lecture1.pdf", there will be a text file "raw/Lecture1.txt" which contains the text data of the original PDF file.
- `filter_raw.py`: Read the raw text files under the "raw" folder and filter these texts so that they can be used in the following ranking algorithm. It removes the stop words, meaningless numbers and some other useless words. Then, it lemmatizes and stems the words so that derivative words can be treated equally. The results are saved under the "corpus" folder. Each file under this folder represents the abstract of a PDF file from "slides" folder. For example, if it read a text file "raw/Lecture1.txt", there will be a filtered text file "corpus/Lecture1.txt" which contains the cleaned text data.
- `bm25.py`: Read the topic file "topics.json" and generate queries with the distributions of keywords in each topic. Each topic generates one query. Then, for each query, run the bm25 ranking algorithm to calculate the scores of this query to each documents in the "corpus" folder. Finally, get the top 10 documents and write the result to the target file "result/bm25.txt".
- `doc_sim.py`: Similar as "bm25.py". The only difference is the ranking algorithm. It calculates the cosine similarity with TF-IDF weights with each pair of query and document. Then, get the top 10 documents and write the result to the target file "result/sim.txt".

## 2. Implementation

### 2.1 Identify Emerging Topics

#### Tweets Crawling
This part serves to generate dataset containing recent tweets from Twitter. 
Due to the rate limit of Twitter, we can only crawl a small amount of tweets every 15 min.
Therefore, in `Crawling/` directory, we implemented a crawler which can crawl tweets automatically.

- `Twitter_crawler.py`: Crawl recent tweets that don't overlap with pre-crawled tweets.
- `utils.py`: Sort crawled tweets in terms of create time, which aims to optimize crawling and saving process.
- `Twitter_crawler.sh`: Auto-crawling bash file that runs `Twitter_crawler.py` and `utils.py` repeatedly every 15 min.

#### Topic Mining
This part is to generate topics with crawled tweets. Here we applied LDA algorithm for topic mining.
All related files are in `TopiccDiscovery/` directory. Implementation of `topic_discovery.py` is as follows: 

- **Preprocess**: For each tweet, we perform 1) lower; 2) remove username, 
hashtag, url, number, punctuation, special character, and short word; 3)
tokenization; 4) remove stopwords; 5) lemmatization; and 6) stemming. 
Then, we save processed data `data/pre-processed.pkl` for training.
- **Find optimal number of topics**: We applied LDA model with different 
numbers of topics from 2 to 14, and found that 10 is the optimal.
- **Training**: We set number of topics as 10, trained an LDA model on 
662k processed tweets, and saved model files in `model/` directory.
- **Saving Topics**: We loaded pre-trained files, saved word distributions for 
topics, and drew word cloud figures by analyzing hashtags for all topics.
- **Predict**: With pre-trained model, we can crawl latest tweets about computer 
science and make predictions to find out emerging topics among all topics. 
Meanwhile, we use these newly crawled tweets to update the LDA model.

### 2.2 Recommend Slides

#### `pdf_download.py`

This module does the following:

1. Given the course website page, use Soup to extract all the elements with tag "a".
2. Judge the elements whether it is a link which is end with ".txt". If yes, concatenate the prefix and the link to get the complete url.
3. Download the PDF file with its original name and put it into the "slides" folder.

Functions are:

- `getTagA(root_url)`: Obtain all the elements with tag "a" and return a list of string.
- `downPdf(root_url, prefix, list_a)`: Download all the PDF files in the root_url. The argument "prefix" is used to complete the pdf links. It varies with different course websites.
- `getFile(url)`: Get the url file to the "slides" folder.

#### `pdf_miner.py`

This module does the following:

1. Read each PDF file under the "slides" folder.
2. Create a PDF Parser for each PDF file. Then parse the pdf file and extract the text data from each page.
3. Write the raw text data to a target file under the folder "raw".

Functions are:

- `parse(filename)`: Extract text data from a PDF file and write it to a target text file (Different PDF files write into different text files).

#### `filter_raw.py`

This module does the following:

1. Read each raw text file under the "raw" folder.
2. Tokenlize the text data and remove short words, numbers and stop words from the text.
3. Lemmatize and stem words. Then, write it to a text file under the "corpus" folder (Different raw text files write into different target files).

Functions are:

- `get_raw_data(filepath)`: Read a raw text file and return a list of string. Each element in this list represents a line of data in the raw text file.
- `pre_process(data, filename)`: First, use "re" (regular expression) to remove unwanted words. Second, use "spacy" to lemmatize words and "nltk.stem" to stem words. Finally, write these stemmed words to the target file under the "corpus" folder.

#### `bm25.py`

This module does the following:

1. Read the topic file "topics.json" and generate a query based on the distributions of keywords in each topic. For example, if the topic is "{"topic1" : {kewords1 : 0.5, keyword2 : 0.5}}", it will generate a query like "keyword1 keyword1 keyword2 keyword2" which keeps to the distributions.
2. Treat this query as a document and compute the scores of this query to each document in our corpus with the BM25 model implemented by gensim library.
3. Get the top 10 score document names and write the result to the result file "result/bm25.txt".

Functions are:

- `tokenization(filename)`: Read the document under the "corpus" folder and return a list of words in this document.
- `read_corpus(dir_path)`: Read all the documents under the dir_path and return a 2-dimensional list of strings. The first dimension represents each document and the second one contains the words included in each document.
- `simulate_query_by_topics(topic_file)`: Generate queries with topics. In this implementation, it generates query with a word base 100. If we have keyword1 and keyword2 with distribution of 0.2 and 0.5. It will generate a query with 20 keyword1 and 50 keyword2. Node: each topic only reserves top several keywords. Their distributions may not add up to one, but it doesn't affect their relative size.

#### `doc_sim.py`:

This module does the following:

1. Read the topic file "topics.json" and generate a query based on the distributions of keywords in each topic. For example, if the topic is "{"topic1" : {kewords1 : 0.5, keyword2 : 0.5}}", it will generate a query like "keyword1 keyword1 keyword2 keyword2" which keeps to the distributions.
2. Treat this query as a document and compute the cosine similarity with TF-IDF weights with each documents under "corpus" folder.
3. Get the top 10 similarity document names and write the result to the result file "result/sim.txt".

Funcrions are the similar to those in "bm25.py".

## 3. Usage

### Installation

This software requires python 3.5+, 
and it also requires external libraries that can be installed by:

```
pip install -r requirements.txt
```

After you have installed `spacy` library, you also need to load `en` model in `spacy` through:

```
python -m spacy download en_core_web_sm
```

Now you have all the necessary packages! Before any later steps, clone this repository:

```
git clone https://github.com/liuyuxiang512/CourseProject
```

### Usage Example

```
cd CourseProject
```

#### Identify Emerging Topics

Directory `Identify_Topics/` serves to identify emerging topics in Twitter.

```
cd Identify_Topics
```

##### Crawling Tweets from Twitter

You could jump this step by downloading our crawled data [sorted_tweets.json](https://drive.google.com/file/d/1tGOrF_OCt_4XRY9G-8JoTAM_cQLGoeh_/view?usp=sharing), 
which contains 680k tweets, and save the file into `data/` directory.

In order to crawl tweets, 
you first need a Twitter developer account. Then: 

1. Create a Twitter application via [https://developer.twitter.com/](https://developer.twitter.com/).
2. Create a [Twitter app](https://apps.twitter.com/) to access Twitter's API.
3. Find the authentication info in the "Keys and Access Tokens" tab of the app's properties, 
including *consumer_key*, *consumer_secret*, *access_token*, and *access_token_secret*.
4. Fill the authentication into `authentication.txt` in four lines.

Then, you can keep crawling tweets by

```
cd Crawling
bash Twitter_crawler.sh
```

##### Find Optimal Number of Topics

In this step, you can try LDA model with different numbers of topics from 2 to 14, 
and get corresponding coherence values. 
A higher coherence value means a better model. 
If you don't want to use our processed data `Identify_Topics/data/pre-processed.pkl`, 
you may first remove it and continue, but it will take some time.

To find out the optimal number of topics, run

```
python topic_discovery.py --tune
```

Then you will get 

```
Tuning...
Number of Topics: 2 --- Coherence Value: 0.49589240555472486
Number of Topics: 3 --- Coherence Value: 0.4752864500035534
Number of Topics: 4 --- Coherence Value: 0.4844109302488787
Number of Topics: 5 --- Coherence Value: 0.5426149238108859
Number of Topics: 6 --- Coherence Value: 0.5708485237453553
Number of Topics: 7 --- Coherence Value: 0.5514423515877226
Number of Topics: 8 --- Coherence Value: 0.5778541035204716
Number of Topics: 9 --- Coherence Value: 0.566857492981066
Number of Topics: 10 --- Coherence Value: 0.5808911042666589
Number of Topics: 11 --- Coherence Value: 0.5561191556402437
Number of Topics: 12 --- Coherence Value: 0.5699566981479943
Number of Topics: 13 --- Coherence Value: 0.5522769193550581
Number of Topics: 14 --- Coherence Value: 0.5433632323040761
...
The optimal number of topics is: 10
```

Therefore, the optimal number of topics is 10, and we will use 10 for our LDA model in formal training.

##### Training

With 10 as number of topics, you can now train an LDA model by running

```
python topic_discovery.py --train
```

This step will take a long time, but you can go ahead and directly use our 
pre-trained model in `Identify_Topics/model/` directory for subsequent steps.

##### Displaying

This step is to use pre-trained model to get topics and draw word cloud for these topics.

```
python topic_discovery.py --display
```

Or you can see what we have got after this step: word distributions of topics 
`Identify_Topics/topics.json` and word cloud figures of topics in 
`Identify_Topics/data/topic_desc_fig/`.

##### Predict

After the previous steps, you have successfully obtained processed data 
(`Identify_Topics/data/pre-processed.pkl`), word distributions of topics 
(`Identify_Topics/topics.json`), and word cloud pictures of topics in
`Identify_Topics/data/topic_desc_fig/`.
This step is a further extension of our software.
You still need a Twitter developer account to crawl latest tweets.
Please refer to how to get authentication info in the above "Crawling Tweets from Twitter" section.
You can always find out emerging topics in Twitter by running

```
python topic_discovery.py --predict
```

It will crawl latest tweets, predict topics for then and figure out popular ones.
Meanwhile, it also uses these newly crawled data to update the LDA model.

We got the following results on Dec.13th:

```
Emerging Topics ID (Ordered): 8 1 7 6 5
```

To see what these topics are, you may go to 
`data/topic_desc_fig/` directory and find corresponding word cloud!


#### Recommend Slides
Directory `Recommend_Slides` is to recommend related slides based on topics.

```
cd Recommend_Slides
```

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
