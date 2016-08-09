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


    for line in file:
        # print(line)
        parsed_json = safe_parse(line)
        # if(not parsed_json):
        #     continue
        print(parsed_json["SrNo."])




def safe_parse(raw_json):
    if(is_json(raw_json)):
        return ujson.loads(raw_json)
    else:
        return {}

def is_json(myjson):
    try:
        json_object = ujson.loads(myjson)
        p1 = (json_object['SrNo.'])
    except ValueError as e:
        return False
    except KeyError as e2:
        return False
    return True

load_data(r"C:\Users\Nishant\PycharmProjects\thesis\topics.json")


