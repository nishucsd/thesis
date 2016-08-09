__author__ = 'Nishant'
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import numpy as np
import json
import matplotlib.pyplot as plt
import ujson
import time
import codecs
import re
import sqlite3
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
# from clusters2 import topic2
from clusters4 import topic4
import random
import csv
#Variables that contains the user credentials to access Twitter API
consumer_key = "SYL3iiFXt7whpdhZIQWE1ngRd"
consumer_secret = "hmJFd3zelTXh2NnXprtzLY2LDEscOtRxuOT9l5hgMk8vYzy3yx"
access_token = "4715398634-mddzJIPAj8nPHXNGExcbJvrdBGH9muMeIxz7f6K"
access_token_secret = "TzrvcQmxAHsLSXr9GcFnZGDv3ywSbQaiuNtsMR168CdhZ"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    sr_no=1
    def __init__(self):
        self.regex = re.compile('[%s]' % re.escape('!"$%&\'()*+,-./:;<=>?[\\]^_`{|}‘’~'))
        self.stop_words =set(stopwords.words("english"))
        self.stop_words|=set(["edu","go", "also", "still",'say','says', "anyone", "that" , "thats", "us", "much", "even", "would", "see", "rt", 'is', 'of', "vote","this", "support",'hey','ji'])
        self.lemmatizer = WordNetLemmatizer()
        self.st = PorterStemmer()
        self.count =0
        self.max_topics=15
        self.start_time = time.time()
        self.topics = np.array([topic4(600,400,15000)])
        self.similarity = np.zeros(self.max_topics)
        self.c_old = [0]*self.max_topics
        self.v_old = [0]*self.max_topics
        self.sr_no=1
        # plt.ion()
        # self.fig = plt.figure()
        # self.ax1 = self.fig.add_subplot(1,1,1)
        # plt.get_current_fig_manager().window.wm_geometry("+0+0")

    def on_data(self, data):
        self.analyse(data)
        return True

    def on_error(self, status):
        print(status)

    def analyse(self,line):
        file1 = open("acceleration.txt","a")
        file2 =  codecs.open("topics.json",'a',encoding='utf8')
        # file2 = open("json.txt","a")
        f_writer = csv.writer(file1)

        parsed_json = self.safe_parse(line)
        if(not parsed_json):
            return
        tweet = self.regex.sub('', parsed_json["text"].lower())

        hashtags = [x["text"].lower() for x in parsed_json['entities']['hashtags']]
        usernames = [x["screen_name"].lower() for x in parsed_json['entities']['user_mentions']]
        words = self.getwords(tweet.split())

        if(len(words) < 2):
            return
        self.count+=1
        for i in range(self.topics.size):
            self.similarity[i] = self.topics[i].get_similarity(hashtags, usernames, words)
        if(np.max(self.similarity) == 0):
            if(self.topics.size < self.max_topics):
                self.topics = np.append(self.topics, topic4(600,400,15000))
                max_ind = self.topics.size -1
            else:
                max_ind = random.randrange(0,self.topics.size)
        else:
            max_ind = np.argmax(self.similarity)

        self.topics[max_ind].set_cluster(hashtags, usernames, words)
        if(self.count%1500 ==0):
            current = time.time()
            print("--- %s seconds ---" % (current - self.start_time))
            self.start_time=current
            self.count=0
            counts_vector = [i.topic_count for i in self.topics]
            counts_vector += [0]*(self.max_topics-len(counts_vector))
            delta = np.subtract(counts_vector,self.c_old)
            acc = np.subtract(delta,self.v_old)
            # f_writer.writerow(acc)
            # print(counts_vector)
            # self.ax1.plot(acc)
            self.c_old = counts_vector
            self.v_old = delta
            # plt.grid()
            # self.fig.canvas.draw()
            # self.ax1.clear()
            # self.json_counts(  self.sr_no,file2, counts_vector, self.topics)
            self.sr_no+=1
            self.print_counts( counts_vector, self.topics)
            print("\n")

    # print("---\n\n\nfinal time: %s seconds ---" % (time.time() - self.s1))


    def getwords(self, tweet):
        # return np.array([x for x in tweet if not (x.startswith('#') or x.startswith('@') or x.startswith('https') or x in self.stop_words )])
        return np.array([x for x in tweet if not (x.startswith('#') or x.startswith('@') or x.startswith('htt') or x in self.stop_words or len(x)<2)])


    def safe_parse(self,raw_json):
        if(self.is_json(raw_json)):
            return ujson.loads(raw_json)
        else:
            return {}

    def print_counts(self,c_vector, topics):
        annotate = np.arange(self.max_topics)
        temp = sorted(zip(c_vector,topics, annotate), key = lambda x:-x[0])
        for i in temp[:10] :
            print( "Topic: ", i[2])
            print(sorted(i[1].l1.items(), key = lambda x : -x[1])[:20])
            print(sorted(i[1].l2.items(), key = lambda x : -x[1])[:20])
            print(sorted(i[1].l3.items(), key = lambda x : -x[1])[:20])
            print()

    def write_counts(self,writer, c_vector, topics):
        annotate = np.arange(self.max_topics)
        writer.write("Time stamp is- "+str(time.time())+"\n")
        temp = sorted(zip(c_vector,topics, annotate), key = lambda x:-x[0])
        for i in temp[:10] :
            writer.write( "Topic: "+ str(i[2])+"\n")
            writer.write(str(sorted(i[1].l1.items(), key = lambda x : -x[1])[:20]) +"\n")
            writer.write(str(sorted(i[1].l2.items(), key = lambda x : -x[1])[:20]) +"\n")
            writer.write(str(sorted(i[1].l3.items(), key = lambda x : -x[1])[:20]) +"\n")
            writer.write("\n")

    def json_counts(self,sr_no, writer, c_vector, topics):
        out={}
        out["SrNo."]=sr_no
        out["created_at"] = time.asctime( time.localtime(time.time()) )
        out["Top_Topics"]={}
        annotate = np.arange(self.max_topics)
        temp = sorted(zip(c_vector,topics, annotate), key = lambda x:-x[0])
        for i in temp[:7] :
            out["Top_Topics"]["Topic_"+ str(i[2])]={}
            out["Top_Topics"]["Topic_"+ str(i[2])]["hashtags"]= [a[0] for a in sorted(i[1].l1.items(), key = lambda x : -x[1])[:15]]
            out["Top_Topics"]["Topic_"+ str(i[2])]["user_mentions"]= [a[0] for a in sorted(i[1].l2.items(), key = lambda x : -x[1])[:15]]
            out["Top_Topics"]["Topic_"+ str(i[2])]["tokens"]= [a[0] for a in sorted(i[1].l3.items(), key = lambda x : -x[1])[:15]]
        # print(out)
        json.dump([out], writer)
        writer.write('\n')



    def is_json(self, myjson):
        try:
            json_object = ujson.loads(myjson)
            p1 = (json_object['user']['id_str'],json_object['text'], json_object['entities']['hashtags'] )
        except ValueError as e:
            return False
        except KeyError as e1:
            return False
        return True





if __name__ == '__main__':
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    # stream.filter(track=['nvdemconvention','democratic convention'])
    stream.filter(track=['trump','hillary','bernie','eu referendum', 'uk','giants'])
    # stream.filter(locations=[-75,39,-73,41])
