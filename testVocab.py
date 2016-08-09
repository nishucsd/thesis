__author__ = 'Nishant'
import numpy as np
import ujson
from lruOrd import lru1
import time
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from clusters import topic
from clusters2 import topic2
import random
# import pandas as pd

# import sys
# import codecs
# from sklearn.cluster import KMeans
# from matplotlib import pyplot as plt
# from scipy.cluster.hierarchy import dendrogram, linkage
# from sklearn.decomposition import PCA
# from pylab import rcParams

regex = re.compile('[%s]' % re.escape('!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~'))
stop_words =set(stopwords.words("english"))
stop_words|=set(["edu", "com", "also", "still", "anyone", "cc" , "ca", "us", "much", "even", "would", "see", "rt", 'is', 'of'])
lemmatizer = WordNetLemmatizer()
st = PorterStemmer()
def load_data(filename):
    file = open(filename)
    count =0
    start_time = time.time()
    s1 = start_time

    topics = np.array([topic2(600,400,20000),topic2(600,400,20000),topic2(600,400,20000),topic2(600,400,20000),topic2(600,400,20000),topic2(600,400,20000),topic2(600,400,20000),topic2(600,400,20000),topic2(600,400,20000),topic2(600,400,20000),topic2(600,400,20000),topic2(600,400,20000),topic2(600,400,20000),topic2(600,400,20000)])

    # topics = np.array([topic(400,400,20000),topic(400,400,20000),topic(400,400,20000),topic(400,400,20000),topic(400,400,20000),topic(400,400,20000),topic(400,400,20000),topic(400,400,20000),topic(400,400,20000),topic(400,400,20000),topic(400,400,20000)])
    similarity = np.array(np.zeros(topics.size))
    for line in file:
        # print(line)
        parsed_json = safe_parse(line)
        if(not parsed_json):
            continue
        # # print(df["text"])
        tweet = regex.sub('', parsed_json["text"].lower())
        # print(getwords(tweet.split()))

        hashtags = list(map(lambda x : x["text"], parsed_json['entities']['hashtags']))
        usernames = list(map(lambda x : x["screen_name"], parsed_json['entities']['user_mentions']))
        words = getwords(tweet.split())
        count+=1
        if(len(words) < 3):
            continue
        for i in range(similarity.size):
            similarity[i] = topics[i].get_similarity(hashtags, usernames, words)
        if(np.max(similarity) == 0):
            max_ind = random.randrange(0,similarity.size)
        else:
            max_ind = np.argmax(similarity)

        topics[max_ind].set_cluster(hashtags, usernames, words)
        if(count%5000 ==0):
            current = time.time()
            print("--- %s seconds ---" % (current - start_time))
            start_time=current
            count=0
            # print(similarity)
            counts_vector = np.array([i.topic_count for i in topics])
            # print_counts( counts_vector, topics)
            print("\n")
    print("---\n\n\nfinal time: %s seconds ---" % (time.time() - s1))

def getwords(tweet):
    return np.array([st.stem(x) for x in tweet if not (x.startswith('#') or x.startswith('@') or x.startswith('https') or x in stop_words )])
    # return np.array([st.stem(x) for x in tweet if not (x.startswith('#') or x.startswith('@') or x.startswith('https') or x in stop_words )])


def safe_parse(raw_json):
    if(is_json(raw_json)):
        return ujson.loads(raw_json)
    else:
        return {}

def print_counts(c_vector, topics):
    temp = sorted(zip(c_vector,topics), key = lambda x:-x[0])
    c=0
    for i in temp :
        print(sorted(i[1].l1.items(), key = lambda x : -x[1])[:50])
        print(sorted(i[1].l2.items(), key = lambda x : -x[1])[:50])
        print(sorted(i[1].l3.items(), key = lambda x : -x[1])[:50])
        print()

        c+=1
        if(c>4):
            break


def is_json(myjson):
    try:
        json_object = ujson.loads(myjson)
        p1 = (json_object['user']['id_str'],json_object['text'], json_object['entities']['hashtags'] )
    except ValueError as e:
        return False
    except KeyError as e2:
        return False
    return True


load_data(r"F:\election data\election141\election141")


