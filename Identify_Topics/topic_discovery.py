import re
import csv
import json
import spacy
import tweepy
import argparse
import pandas as pd

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel
from gensim.utils import simple_preprocess
from gensim.models.ldamodel import LdaModel
from gensim.models.phrases import Phrases, Phraser

# NLTK
from nltk.stem import PorterStemmer

from wordcloud import WordCloud
# get stopwords


def crawl_tweets(field):
    # Twitter keys
    consumer_key = "Bi2HW8V30V9SebqwjW36mGwVv"
    consumer_secret = "POdkCtnk4bUv9bCNIJBx2sFcKz99I5OGYE1W3Q6RSRYBYQ8yRA"
    access_token = "1000446341196238848-QTvbjrKCX5w65AOnQQW7WqbhKUNNqX"
    access_token_secret = "8He7zKjmCm9KsX21Cc8LXrWpl3D4ppiUuVdzpL3NNhfFY"

    # Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    statuses = tweepy.Cursor(api.search, q=field, lang='en').items(2000)
    tweets = []
    for status in statuses:
        tweets.append(status.text)

    return tweets


def optimal_topic_model():
    processed_data = pd.read_pickle('data/pre-processed.pkl')
    texts = processed_data.iloc[:10000]["text"]
    texts = [text.split() for text in texts]

    # Create dictionary and corpus
    id2word = corpora.Dictionary(texts)
    corpus = [id2word.doc2bow(text) for text in texts]

    # optimal number of topics: 10
    coherence_values = []
    best_c_v = 0
    best_num_topics = 0
    for num_topics in range(2, 15):
        model = LdaModel(corpus=corpus,
                         id2word=id2word,
                         num_topics=num_topics,
                         random_state=100,
                         update_every=1,
                         chunksize=100,
                         passes=15,
                         alpha='auto',
                         per_word_topics=True)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=id2word, coherence='c_v')
        coherence = coherencemodel.get_coherence()
        coherence_values.append(coherence)
        if coherence > best_c_v:
            best_c_v = coherence
            best_num_topics = num_topics
        print("Number of Topics: " + str(num_topics) + " --- Coherence Value: " + str(coherence))

    print("...")
    print("The optimal number of topics is: " + str(best_num_topics))


def predict_topics(raw_data, field):
    lda_model = LdaModel.load("model/lda_model")
    data_predicted = pre_process(raw_data=raw_data, field=field, train=False)
    id2word = corpora.Dictionary(data_predicted)
    corpus = [id2word.doc2bow(text) for text in data_predicted]
    topics_list = []
    topic_distribution_list = lda_model[corpus]
    lda_model.update(corpus=corpus)
    lda_model.save("model/lda_model")
    for topic_distribution in topic_distribution_list:
        topic_distribution = topic_distribution[0]
        topic_distribution = sorted(topic_distribution, key=lambda x: x[1], reverse=True)
        topics_list.append(topic_distribution[0][0])

    return topics_list


def get_raw_data(input_file):
    data = []
    with open(input_file, "r") as file2read:
        for line in file2read.readlines():
            try:
                data.append(json.loads(line)["text"])
            except:
                pass

    return data  # 680419 -> 661676


def pre_process(raw_data, field, train=False):
    # prepare stopwords
    with open("data/stopwords.txt", "r") as file:
        stopwords = file.read().strip().split("\n")
    stopwords.extend(['from', 'twitter', 'pic'] + field.split())

    # Basic preprocess
    # 1) lower, remove username, hashtag, url
    # 2) remove number/punctuation/special character, short word
    # 3) tokenization, remove stopwords, remove short tweets
    clean_data = []
    for line in raw_data:
        text = line.lower()
        text = re.sub(r"@\S+", "", text)
        text = re.sub(r"#\S+", "", text)
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"[^a-zA-Z']", " ", text)
        tidy_tweet = " ".join([word for word in text.split() if len(word) > 3])
        tidy_tweet_tokens = simple_preprocess(tidy_tweet, deacc=True)
        tokens_no_stop = [word for word in tidy_tweet_tokens if word not in stopwords]
        no_stop_joined = " ".join(tokens_no_stop)
        if train:
            if len(tokens_no_stop) >= 3:
                clean_data.append(no_stop_joined)
        else:
            clean_data.append(no_stop_joined)

    # Advanced preprocess
    # 1) form bigrams 2) lemmatization 3) stemming

    # Build bigram model and form bigrams
    data_words = [simple_preprocess(doc, deacc=True) for doc in clean_data]
    bigram = Phrases(data_words, min_count=10, threshold=100)
    bigram_model = Phraser(bigram)
    data_words_bigrams = [bigram_model[doc] for doc in data_words]

    # LEMMATIZATION
    # python3 -m spacy download en
    nlp = spacy.load('en', disable=['parser', 'ner'])
    allowed_postags = ['NOUN', 'ADJ', 'VERB', 'ADV']
    lemmatized = []
    for sent in data_words_bigrams:
        doc = nlp(" ".join(sent))
        lemmatized.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])

    # STEMMING
    stemmer = PorterStemmer()
    stemmed = [[stemmer.stem(y) for y in x] for x in lemmatized]

    processed_data = pd.DataFrame({"text": [" ".join(text) for text in stemmed]})
    if train:
        processed_data.to_pickle('data/pre-processed.pkl')

    return stemmed


def train_topic_model(num_topics):
    processed_data = pd.read_pickle('data/pre-processed.pkl')
    texts = processed_data.iloc[:]["text"]
    texts = [text.split() for text in texts]

    # Create dictionary and corpus
    id2word = corpora.Dictionary(texts)
    corpus = [id2word.doc2bow(text) for text in texts]

    # Build LDA model
    lda_model = LdaModel(corpus=corpus,
                         id2word=id2word,
                         num_topics=num_topics,
                         random_state=100,
                         update_every=1,
                         chunksize=100,
                         passes=15,
                         alpha='auto',
                         per_word_topics=True)

    lda_model.save("model/lda_model")


def get_topics_distribution(output_file):
    lda_model = LdaModel.load("model/lda_model")

    topics = lda_model.show_topics(num_words=100)
    with open(output_file, "w") as file2write:
        for topic in topics:
            keyword_weight = {}
            for keyword in topic[1].split(" + "):
                keyword_weight[keyword.split("*")[1].strip('"')] = float(keyword.split("*")[0])
            topic_dict = {topic[0]: keyword_weight}
            file2write.write(json.dumps(topic_dict) + "\n")


def get_topic_description(input_file, field):
    data = []
    with open(input_file, "r") as file2read:
        for line in file2read.readlines():
            try:
                data.append(json.loads(line))
            except:
                pass

    # fetch tweets with hashtags
    texts_list = []
    hashtags_list = []
    for i in range(len(data)):
        hashtags = data[i]["entities"]["hashtags"]
        if len(hashtags) > 0:
            texts_list.append(data[i]["text"])
            hashtags_list.append([hashtag["text"] for hashtag in hashtags])

    # predict topics
    topics_list = predict_topics(raw_data=texts_list, field=field)

    # get hashtags for topics
    topic_hashtags = {}  # {topic: [hashtags]}
    for i in range(len(texts_list)):
        topic = topics_list[i]
        hashtags = hashtags_list[i]
        if topic not in topic_hashtags.keys():
            topic_hashtags[topic] = []
        for hashtag in hashtags:
            hashtag = hashtag.lower()
            topic_hashtags[topic].append(hashtag)

    # draw wordcloud
    wc = WordCloud()
    for topic in topic_hashtags.keys():
        text = " ".join(topic_hashtags[topic])
        wc.generate(text)
        wc.to_file("data/topic_desc_fig/topic_" + str(topic) + ".png")


def find_emerging_topics(topics_list):
    topic_count = {}
    for topic in topics_list:
        if topic not in topic_count.keys():
            topic_count[topic] = 0
        topic_count[topic] += 1

    topic_count = sorted(topic_count.items(), key=lambda x: x[1], reverse=True)

    emerging_topics = []
    threshold = 0
    for i in range(len(topic_count)):
        if i <= int(len(topic_count) / 2):
            emerging_topics.append(topic_count[i][0])
            threshold = topic_count[i][1]
        else:
            if topic_count[i][1] < threshold:
                break
            emerging_topics.append(topic_count[i][0])

    # display
    print("Emerging Topics ID (Ordered): " + " ".join([str(topic) for topic in emerging_topics]))
    print("Go to 'data/topic_desc_fig/' directory and find corresponding word cloud!")

    return emerging_topics


def parse_args():
    # parse input
    parser = argparse.ArgumentParser(description='Identify In-demanding Skills')
    parser.add_argument('-i', '--input_file', type=str, default='data/sorted_tweets.json',
                        help='input file contains tweets crawled from Twitter')
    parser.add_argument('-n', '--num_topics', type=int, default=10,
                        help='number of topics.')
    parser.add_argument('-f', '--field', type=str, default='computer science',
                        help='field of subject to mine (computer science)')
    parser.add_argument('-o', '--output_file', type=str, default='topics.json',
                        help='output file contains term distribution of \'num_topics\'.')
    parser.add_argument('--train', default=False, action="store_true",
                        help='preprocess and train')
    parser.add_argument('--display', default=False, action="store_true",
                        help='save topics and draw pictures')
    parser.add_argument('--tune', default=False, action="store_true",
                        help='find the optimal number of topics')
    parser.add_argument('--predict', default=False, action="store_true",
                        help='predict emerging topics with trained model')
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()
    input_file = args.input_file
    num_topics = args.num_topics
    field = args.field
    output_file = args.output_file

    tune = args.tune
    train = args.train
    display = args.display
    predict = args.predict

    if tune:
        try:
            processed_data = pd.read_pickle('data/pre-processed.pkl')
        except:
            raw_data = get_raw_data(input_file=input_file)
            print("Preprocessing...")
            processed_data = pre_process(raw_data=raw_data, field=field, train=train)
        print("Tuning...")
        optimal_topic_model()

    if train:
        try:
            processed_data = pd.read_pickle('data/pre-processed.pkl')
        except:
            raw_data = get_raw_data(input_file=input_file)
            print(len(raw_data))
            print("Preprocessing...")
            processed_data = pre_process(raw_data=raw_data, field=field, train=train)
            print(len(processed_data))
        print("Training...")
        train_topic_model(num_topics=num_topics)
        print("Finished!")

    if test:
        print("Saving Topics...")
        get_topics_distribution(output_file=output_file)
        print("Saving Figures")
        get_topic_description(input_file=input_file, field=field)
        print("Finished!")

    if predict:
        raw_data = crawl_tweets(field=field)
        topics_list = predict_topics(raw_data=raw_data, field=field)
        emerging_topics = find_emerging_topics(topics_list=topics_list)
