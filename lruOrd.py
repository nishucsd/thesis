import collections

__author__ = 'Nishant'
class lru1:
    def __init__(self, capacity):
        self.dic = collections.OrderedDict()
        self.remain = capacity

    def get(self, key):
        if key not in self.dic:
            return -1
        v = self.dic.pop(key)
        self.dic[key] = v   # set key as the newest one
        return v

    def set(self, key):
        if key in self.dic:
            v = self.get(key)
            self.dic.pop(key)
            self.dic[key] = v+1
        else:
            if self.remain > 0:
                self.remain -= 1
            else:  # self.dic is full
                self.dic.popitem(last=False)
            self.dic[key] = 1