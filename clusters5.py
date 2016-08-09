__author__ = 'Nishant'
from lru import LRU
import numpy as np
class topic4:
    def __init__(self, c_hash, c_user, c_words):
        self.topic_count =1
        self.l1_cap =c_hash
        self.l2_cap =c_user
        self.l3_cap =c_words
        self.l1 = LRU(c_hash)
        self.l2 = LRU(c_user)
        self.l3 = LRU(c_words)
        self.l1_sum =0
        self.l2_sum =0
        self.l3_sum =0
        self.l1_len =0
        self.l2_len =0
        self.l3_len =0



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
            if(not self.l1.has_key(k)):
                self.l1_sum -=self.l1.values()[-1] if self.l1_len>=self.l1_cap else 0
                self.l1_len +=1
            self.l1_sum +=1

            self.l1[k]=self.l1.get(k,0)+1


        for k in users:
            if(not self.l2.has_key(k)):
                self.l2_len +=1

            self.l2[k]=self.l2.get(k,0)+1


        for k in words:
            if(not self.l3.has_key(k)):
                self.l3_len +=1

            self.l3[k]=self.l3.get(k,0)+1


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
        h1 = min(self.l1_len,self.l1_cap)
        u1 = min(self.l2_len,self.l2_cap)
        w1 = min(self.l3_len,self.l3_cap)
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


        similarity = (h_ind/(h1+1))*(h_sum/sum(self.l1.values() +[1])) + (u_ind/(u1+1))*(u_sum/sum(self.l2.values()+[1])) + (w_ind/(w1+1))*(w_sum/sum(self.l3.values()+[1])) +c
        return similarity