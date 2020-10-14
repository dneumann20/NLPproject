# import numpy as np

import nltk
import numpy as np
from nltk.corpus import genesis
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk import jaccard_distance as jaccard
import socket
import sklearn
from googleapiclient.discovery import build
from sklearn.feature_extraction.text import TfidfVectorizer

#my_api_key = "AIzaSyA4mNsPZaC9DwLEdjPRPipPeaV4aSyjfjk"
#my_cse_id = "54c5d40125d58c1d1"

#p = "Taking my dog for a walk is fun"
#q = "Taking a shower is calming"
#ptok = nltk.word_tokenize(p)
#qtok = nltk.word_tokenize(q)

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res

#hp = google_search(atok, my_api_key, my_cse_id)
#hpq = google_search(btok, my_api_key, my_cse_id)

# find Jaccard Similarity between the two sets
#distance = nltk.jaccard_distance(hp, hpq)

a = "test"
b = "yest"
atok = nltk.word_tokenize(a)
btok = nltk.word_tokenize(b)

#aprep = preProcess(a)
#bprep = preProcess(b)

def jaccard_sim(S1, S2):
    return S1.jaccard(S2, genesis_ic)

distance = jaccard_sim(atok, btok)
print(distance)