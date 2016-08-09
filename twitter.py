__author__ = 'Nishant'
import numpy as np
import ujson
import time
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from clusters4 import topic4
import random
import matplotlib.pyplot as plt


regex = re.compile('[%s]' % re.escape('!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~'))
stop_words =set(stopwords.words("english"))
stop_words|=set(["edu", "com", "also", "still", "anyone", "cc" , "ca", "us", "much", "even", "would", "see", "rt", 'is', 'of'])
st = PorterStemmer()
max_topics = 15
def load_data(filename):
    file = open(filename)
    count =0
    start_time = time.time()
    s1 = start_time
    time_slice = 5000
    topics = np.array([topic4(600,400,15000)])
    c_old = [0]*max_topics
    v_old = [0]*max_topics
    similarity = np.zeros(max_topics)
    plt.ion()
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    plt.get_current_fig_manager().window.wm_geometry("+0+0")
    for line in file:
        parsed_json = safe_parse(line)
        if(not parsed_json):
            continue
        tweet = regex.sub('', parsed_json["text"].lower())
        hashtags = [x["text"].lower() for x in parsed_json['entities']['hashtags']]
        usernames = [x["screen_name"].lower() for x in parsed_json['entities']['user_mentions']]

        words = getwords(tweet.split())
        count+=1
        if(len(words) < 2):
            continue
        for i in range(topics.size):
            similarity[i] = topics[i].get_similarity(hashtags, usernames, words)
        if(np.max(similarity) == 0):
            if(topics.size < max_topics):
                topics = np.append(topics, topic4(600,400,15000))
                max_ind = topics.size -1
            else:
                max_ind = random.randrange(0,topics.size)
        else:
            max_ind = np.argmax(similarity)

        topics[max_ind].set_cluster(hashtags, usernames, words)

        if(count%time_slice ==0):
            current = time.time()
            print("--- %s seconds ---" % (current - start_time))
            start_time=current
            count=0
            counts_vector = [i.topic_count for i in topics]
            counts_vector += [0]*(max_topics-len(counts_vector))
            delta = np.subtract(counts_vector,c_old)
            acc = np.subtract(delta,v_old)
            print(counts_vector)
            # print(similarity)
            ax1.plot(acc)
            c_old = counts_vector
            v_old = delta
            plt.grid()
            fig.canvas.draw()
            ax1.clear()
            # print_counts( counts_vector, topics)
            print("\n")
    print("---\n\n\nfinal time: %s seconds ---" % (time.time() - s1))

def getwords(tweet):
    return np.array([st.stem(x) for x in tweet if not (x.startswith('#') or x.startswith('@') or x.startswith('http') or x in stop_words )])


def safe_parse(raw_json):
    if(is_json(raw_json)):
        return ujson.loads(raw_json)
    else:
        return {}

def print_counts(c_vector, topics):
    annotate = np.arange(max_topics)
    temp = sorted(zip(c_vector,topics, annotate), key = lambda x:-x[0])
    c=0
    # print([i[0] for i in temp])
    for i in temp :
        print( "Topic: ", i[2])
        print(sorted(i[1].l1.items(), key = lambda x : -x[1])[:50])
        print(sorted(i[1].l2.items(), key = lambda x : -x[1])[:50])
        print(sorted(i[1].l3.items(), key = lambda x : -x[1])[:50])
        print()

        c+=1
        if(c>8):
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

load_data(r"F:\election data\election139\election245")


