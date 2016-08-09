__author__ = 'Nishant'
from lru import LRU
import numpy as np
class topic:
    def __init__(self, c_hash, c_user, c_words):
        self.topic_count =1
        self.l1 = LRU(c_hash)
        self.l2 = LRU(c_user)
        self.l3 = LRU(c_words)

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

    def set_cluster(self, hashtags, users, words):
        for k in hashtags:
            v = self.l1.get(k,0)
            self.l1[k]=v+1
        for k in users:
            v = self.l2.get(k,0)
            self.l2[k]=v+1
        for k in words:
            v = self.l3.get(k,0)
            self.l3[k]=v+1
        self.topic_count+=1

    def get_similarity(self,hashtags,users,words):
        h_sum = 0
        u_sum = 0
        w_sum = 0

        for h in hashtags:
            h_sum+= self.l1.get(h,0)
        for u in users:
            u_sum+= self.l2.get(u,0)
        for w in words:
            w_sum+= self.l3.get(w,0)

        similarity = 0.5*h_sum + 0.2*u_sum + 0.3*w_sum
        return similarity