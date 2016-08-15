# thesis
This is my thesis project on twitter 

The project aims to find events in realtime from twitter feeds. It takes twitter stream as input, and it lists out the top topics that are being discussed.
Key Features include:

1. It gives top keywords, hashtags and usermentions for every topic

2. It gives the rate of change of popularity of each topic with respect to time as a graph.

3. The topics evolve with time.

4. Old topics that are no longer being discussed die out and new ones are incorporated.

live-twitter.py gives the topics and accelerations as jsons and csv files respectively. Need to install these libraries to access it.

pip install tweepy

pip install numpy

pip install matplotlib.pyplot

pip install ujson

pip install random

pip install csv
