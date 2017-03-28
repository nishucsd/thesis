#!/usr/bin/env python
"""
Minimal Example
===============
Generating a square wordcloud from the US constitution using default arguments.
"""

from os import path
from wordcloud import WordCloud
import math
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

# tokens = [('trump', 17979), ('black', 2633), ('reporter', 1921), ('press', 1863), ('president', 1687), ('donald', 1553), ('news', 1410), ('conference', 1402), ('caucus', 1290), ('congressional', 1284), ('set', 1246), ('meeting', 1153), ('fake', 1094), ('media', 1093)]
tokens = [('trump', 92441), ('president', 10067), ('press', 9926), ('black', 9510), ('donald', 8248), ('reporter', 7494), ('news', 7470), ('media', 6968), ('conference', 6431), ('fake', 5507), ('russia', 4980), ('caucus', 4540)]
token_dict = dict(tokens)
div = sorted(token_dict.values())[0]
div=round(div/5, -1)
arr = [(i+' ')*int(token_dict[i]/div) for i in token_dict]
print(" ".join(arr))




# The pil way (if you don't have matplotlib)
#image = wordcloud.to_image()
#image.show()