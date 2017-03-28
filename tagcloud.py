#!/usr/bin/env python
"""
Minimal Example
===============
Generating a square wordcloud from the US constitution using default arguments.
"""

from os import path
from wordcloud import WordCloud
import math
d = path.dirname(__file__)

# Read the whole text.
# text = open(path.join(d, 'constitution.txt')).read()
# Generate a word cloud image

tokens = [('president', 10067), ('press', 9926), ('black', 9510), ('donald', 8248), ('reporter', 7494), ('news', 7470), ('media', 6968), ('conference', 6431), ('fake', 5507), ('russia', 4980), ('caucus', 4540)]
token_dict = dict(tokens)
div = sorted(token_dict.values())[0]
div=round(div/5, -1)
arr = [(i+' ')*int(token_dict[i]/div) for i in token_dict]
text = " ".join(arr)

wordcloud = WordCloud().generate(text)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud)
plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(max_font_size=40).generate(text)
plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.show()


def sigmoid(x):
    return 1 / (1 + math.exp(-x))

# The pil way (if you don't have matplotlib)
#image = wordcloud.to_image()
#image.show()