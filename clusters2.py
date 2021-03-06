__author__ = 'Nishant'
from lru import LRU
import numpy as np
class topic4:
    def __init__(self, c_hash, c_user, c_words):
        self.topic_count =1
        self.l1 = LRU(c_hash)
        self.l2 = LRU(c_user)

    def set_hashLRU(self,l):
        self.set(self.l1, l)

    def set_userLRU(self,l):
        self.set(self.l2, l)



    def set(self, lru, l):
        for k in l:
            v = lru.get(k,0)
            lru[k]=v+1

    def set_cluster(self, hashtags, users, words):
        for k in hashtags:
            self.l1[k]=self.l1.get(k,0)+1
        for k in users:
            self.l2[k]=self.l2.get(k,0)+1

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

        if(h_match !=0):
            c = h_match -1
        # print(h_ind,h1,u_ind,u1,w_ind,w1, h_sum,w_sum,)
        similarity = (h_ind/(h1+1))*(h_sum/sum(self.l1.values() +[1])) + (u_ind/(u1+1))*(u_sum/sum(self.l2.values()+[1]))  +c
        return similarity