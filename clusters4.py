__author__ = 'Nishant'
from lru import LRU
import numpy as np
class topic4:
    def __init__(self, c_hash, c_user, c_words):
        self.topic_count =1
        # self.time = (self.first,self.last)
        self.l1 = LRU(c_hash)
        self.first =""
        self.last=""
        self.lats=[]
        self.longs=[]
        self.l2 = LRU(c_user)
        self.l3 = LRU(c_words)
        self.l4 = LRU(400)
    def set_hashLRU(self,l):
        self.set(self.l1, l)

    def set_userLRU(self,l):
        self.set(self.l2, l)

    def set_wordLRU(self,l):
        self.set(self.l3, l)

    def set(self, lru, l):
        for k in l:
            v = lru.get(k,0)
            lru[k]=v+1

    def set_cluster(self, hashtags, users, words,links, cords):
        for k in hashtags:
            self.l1[k]=self.l1.get(k,0)+1
        for k in users:
            self.l2[k]=self.l2.get(k,0)+1
        for k in words:
            self.l3[k]=self.l3.get(k,0)+1
        for k in links:
            self.l4[k]=self.l4.get(k,0)+1
        if(cords is not None):
            self.lats.append(cords["coordinates"][1])
            self.longs.append(cords["coordinates"][0])
        self.topic_count+=1

    def get_similarity(self,hashtags,users,words):
        h_sum = 1
        u_sum = 1
        w_sum = 1
        h_match =0
        h_ind =0
        u_ind =0
        w_ind =0
        c=0
        h1 = self.l1.get_size()
        u1 = self.l2.get_size()
        w1 = self.l3.get_size()
        for h in hashtags:
            # l1_items=zip(*self.l1.items())
            h_sum+= self.l1.get(h,0)
            if(self.l1.has_key(h)):
                ind = self.l1.keys().index(h)
                h_ind+= h1 - ind
                h_match+= 1 if ind<250 else 0
        for u in users:
            u_sum+= self.l2.get(u,0)
            if(self.l2.has_key(u)):
                u_ind+= u1 - self.l2.keys().index(u)
        for w in words:
            w_sum+= self.l3.get(w,0)
            if(self.l3.has_key(w)):
                w_ind+= w1 - self.l3.keys().index(w)
        if(h_match !=0):
            c = h_match -1
        # print(h_ind,h1,u_ind,u1,w_ind,w1, h_sum,w_sum,)
        similarity = (h_ind/(h1+1))*(h_sum/sum(self.l1.values() +[1])) + (u_ind/(u1+1))*(u_sum/sum(self.l2.values()+[1])) + (w_ind/(w1+1))*(w_sum/sum(self.l3.values()+[1])) +c
        return similarity
    def flush1(self, cache, size):
        if(len(cache.keys())>5):
            tokens = reversed(cache.keys()[5])
            cache.clear()
            for i in tokens:
                cache[i]=1


    def flush(self):
        self.flush1(self.l1,500)
        self.flush1(self.l2, 500)
        self.flush1(self.l3,3500)
        self.topic_count=1



