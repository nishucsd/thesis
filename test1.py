__author__ = 'Nishant'
import numpy as np
import ujson
import time
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from clusters4 import topic4
import random
import locale

import matplotlib.pyplot as plt

locale.getdefaultlocale()

regex = re.compile('[%s]' % re.escape('!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~'))
stop_words =set(stopwords.words("english"))
stop_words|=set(["edu", "com", "also", "still", "anyone", "cc" , "ca", "us", "much", "even", "would", "see", "rt", 'is', 'of'])
st = PorterStemmer()
max_topics = 15
def load_data(filename):
    file = open(filename)
    f1 = open("F:\election data\election139\split1","a")


    for line in file:
        parsed_json = safe_parse(line)
        if(not parsed_json):
            continue
        # tweet = regex.sub('', parsed_json["text"].lower())
        hashtags = [x["text"].lower() for x in parsed_json['entities']['hashtags']]
        choice =0
        if "makedonalddrumpfagain" in hashtags:
            choice =4
        elif "alwaystrump" in hashtags or "makeamericagreatagain" in hashtags or "trump2016" in hashtags:
            choice =1
        elif "berniesanders" in hashtags or "feelthebern" in hashtags or "bernie2016" in hashtags or  "supermonday" in hashtags:
            choice =2
        elif "hillary" in hashtags or "imwithher" in hashtags or "hillaryclinton" in hashtags or "supertuesday" in hashtags:
            choice =3
        elif "cruzcrew" in hashtags or "choosecruz" in hashtags or "tedcruz" in hashtags:
            choice =0
        print("sfsf")
        # else :
        #     choice = int(random.random()*5)

        path = "C:\\291d\\t6\\" + str(choice)
        f2 = open(path,"a")
        f2.write(line)









def safe_parse(raw_json):
    if(is_json(raw_json)):
        return ujson.loads(raw_json)
    else:
        return {}

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


