__author__ = 'Nishant'
from lru import LRU
import numpy as np
import ujson
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import functools as f
def tester():
    # l = LRU(5)
    # l["sff"]=1
    # l["abc"]=56
    # l["ty"]=4545
    # l["ty"]=454555
    # l["uuuf"]=565
    # l["nhnh"]=787
    # a=zip(*l.items())

    # print(l.values())
    # print(l.keys().reverse())
    # print(np.sum([1,7,88,88,8,8,8]))
    # print(f.reduce(lambda x,y: x[1] + y[1], l.items()))
    # lemmatizer = WordNetLemmatizer()
    # # print(lemmatizer.lemmatize("trump2016"))
    file = open(r"C:\Users\Nishant\Documents\Data\users-partition.pickle")
    # lemmatizer = WordNetLemmatizer()
    # ps = PorterStemmer()
    # print(ps.stem("sanders"))
    # # print(lemmatizer.lemmatize("saying"))
    # a = [3,2,52,6,5]
    # b=[888,8,8888,88,888888]
    # a = np.array([99])
    # a = np.append(a,899)
    # print(a)
    # print(np.append(a, [4]))
    # # print(sorted(zip(a,b), key = lambda x:-x[0]))

    file = open(r"F:\election data\election139\election150")
    for line in file:
        # print(line)
        parsed_json = safe_parse(line)
        if(not parsed_json):
            continue
        print(parsed_json["text"].lower())
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


tester()
