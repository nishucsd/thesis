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
    v_sum =np.zeros(max_topics)
    start_time = time.time()
    s1 = start_time
    time_slice = 3000
    evac_arg =0
    flag =0
    reset_val = time_slice*10
    topics = np.array([topic4(600,400,15000)])
    c_old = np.zeros(max_topics)
    v_old = np.zeros(max_topics)
    hash_old = [[('',0)]*600]*max_topics
    hashkeys_old = [['']*600]*max_topics
    similarity = np.zeros(max_topics)
    # plt.ion()
    # fig = plt.figure()
    # ax1 = fig.add_subplot(1,1,1)
    test=0
    test_set=[]
    plt.get_current_fig_manager().window.wm_geometry("+0+0")
    for line in file:
        parsed_json = safe_parse(line)
        if(not parsed_json):
            continue
        hashtags, usernames, words = get_entities(parsed_json)
        if(len(words) < 2):
            continue
        count+=1
        if(count<60000):
            for i in range(topics.size):
                similarity[i] = topics[i].get_similarity(hashtags, usernames, words)
            if(np.max(similarity) == 0):
                if(topics.size < max_topics):
                    topics = np.append(topics, topic4(600,400,15000))
                    max_ind = topics.size -1
                else:
                    if(flag ==1):
                        max_ind = evac_arg
                        flag =0
                    else:
                        max_ind = random.randrange(0,topics.size)
            else:
                max_ind = np.argmax(similarity)

            topics[max_ind].set_cluster(hashtags, usernames, words)

            if(count%time_slice ==0):
                current = time.time()
                print("--- %s seconds ---" % (current - start_time))
                start_time=current
                counts_vector = [i.topic_count for i in topics]
                counts_vector += [0]*(max_topics-len(counts_vector))
                delta = np.subtract(counts_vector,c_old)
                acc = np.subtract(delta,v_old)
                # print(counts_vector)
                c_old = counts_vector
                v_old = delta
                v_sum+=v_old

                # ax1.plot(acc)
                # plt.grid()
                # fig.canvas.draw()
                # ax1.clear()



                annotate = np.arange(max_topics)
                temp = sorted(zip(counts_vector,topics, annotate), key = lambda x:-x[0])
                # print_counts(temp)
                # print_emerging_hash(temp,hash_old,hashkeys_old)
                # hash_old = [i[1].l1.items() for i in temp]
                # hashkeys_old = [i[1].l1.keys() for i in temp]
                # print("\n")
            if(count % reset_val == 0):
                flag =1
                # print("velocity sum is",v_sum)
                evac_arg = np.argmin(v_sum)
                v_sum= np.zeros(max_topics)
                topics[evac_arg] = topic4(600,400,15000)
                c_old[evac_arg]=0
                v_old[evac_arg]=0
        # print(count)
        if(count>60000):
            if(len(hashtags)==0):
                continue
            if(test>6000):
                break
            test+=1
            test_set.append((hashtags,usernames,words))
    result=[]
    for tweets in test_set:
        for i in range(topics.size):
                similarity[i] = topics[i].get_similarity([], tweets[1], tweets[2])
        if(np.max(similarity) == 0):
            result.append([])
        else:
            max_i=np.argmax(similarity)
            result.append(dict(sorted(topics[max_i].l1.items(), key = lambda x : -x[1])[:10]).keys())
    prec=0
    i=0
    for tweets in test_set:
        if(bool(set(tweets[0]).intersection(set(result[i])))):
            prec+=1
    print("precision is",prec)




    print("---\n\n\nfinal time: %s seconds ---" % (time.time() - s1))

def get_entities(parsed_json):
    tweet = regex.sub('', parsed_json["text"].lower())
    hashtags = [x["text"].lower() for x in parsed_json['entities']['hashtags']]
    usernames = [x["screen_name"].lower() for x in parsed_json['entities']['user_mentions']]
    words = getwords(tweet.split())
    return hashtags, usernames, words

def getwords(tweet):
    return np.array([x for x in tweet if not (x.startswith('#') or x.startswith('@') or x.startswith('http') or x in stop_words )])


def safe_parse(raw_json):
    if(is_json(raw_json)):
        return ujson.loads(raw_json)
    else:
        return {}

def print_counts(temp):
    for i in temp[:8] :
        print( "Topic: ", i[2])
        print(sorted(i[1].l1.items(), key = lambda x : -x[1])[:50])
        print(sorted(i[1].l2.items(), key = lambda x : -x[1])[:50])
        print(sorted(i[1].l3.items(), key = lambda x : -x[1])[:50])
        print()

def print_emerging_hash(temp, hash_old, hashkey_old):
    for i in range(8):
        print( "Topic: ", temp[i][2])
        common_k = np.intersect1d(temp[i][1].l1.keys(), hashkey_old[i])
        new = dict(temp[i][1].l1.items())
        old = dict(hash_old[i])
        for j in common_k:
            new[j]-=old[j]
        # print((new))
        print(sorted(new.items(), key = lambda x : -x[1])[:50])


def is_json(myjson):
    try:
        json_object = ujson.loads(myjson)
        p1 = (json_object['user']['id_str'],json_object['text'], json_object['entities']['hashtags'] )
    except ValueError as e:
        return False
    except KeyError as e2:
        return False
    return True

load_data(r"F:\election data\election139\election248")


