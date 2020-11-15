
from googleapiclient.discovery import build
#import nltk
#import numpy as np
import pandas as pd
import time
import re
from googlesearch import search

from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet

import flask
#import os
#import webbrowser
#from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import seaborn as sns
import Levenshtein as lev

#app=Flask(__name__)


#if not os.environ.get("WERKZEUG_RUN_MAIN"):
  #  webbrowser.open_new('index.html')

#Otherwise, continue as normal
 #   app.run(host="127.0.0.1", port=2000)


#@app.route('/')
#def index():
 #   return flask.render_template('index.html')


def google_snippets(query, num=10):
    
    query_service = build(serviceName="customsearch", version="v1", developerKey='AIzaSyAz3LheHf9jWsSEztGf5B1TAeiv0FbAsZo') 
    query_results = query_service.cse().list(q=query,cx='fd2dd246666e2965a', num=num
                                                ).execute()
    return query_results['items']



def google_search(query):
    return search(query, lang = 'en',  # The language
                num = 10, start = 0, stop = None, pause = 2.0)


def pre_processing(text):
    
    lemmatizer = WordNetLemmatizer()
    stop_words = stopwords.words('english')

    text = text.split(' ')
#     removing stopwords
    text = [word.strip().lower() for word in text if word.lower() not in stop_words]
#     removing these punctuations from tokens like it will convert the word mode? into mode
    rx = re.compile('([&#.:?!-()])*')
    text = [rx.sub('', word) for word in text]
    
# selecting only the alpha bets and words length greater than 1
    text = [word for word in text if len(word)>1 and word.isalpha()]
#     if some word appear more than 1, remove others
    unique = set(text)
    unique = [lemmatizer.lemmatize(word) for word in unique]
    
# storing after processing in third column
    return ' '.join(text)
    


def sim(P, Q, threshold, pre_process=False):
    
    if pre_process:
        P = pre_processing(P)
        Q = pre_processing(Q)
    
    print('Extracting P...')
    results_p = google_search(P)
    count_p = len(list(results_p))
    print(count_p)
    time.sleep(10)
    print('Extracting Q...')
    results_q = google_search(Q)
    count_q = len(list(results_q))
    print(count_q)
    time.sleep(150)
    
    print('Extracting P AND Q...')
    results_pq = google_search('{} AND {}'.format(P,Q))
    count_pq = len(list(results_pq))
    
    
    if count_pq <= threshold:
        return 0
    
    else:
        return (count_pq) /(count_p + count_q - count_pq) 
           



def wordnet_sim(P, Q):
    
    P=wordnet.synsets(P)
    Q=wordnet.synsets(Q)

    chod_sim = None
    wup, path = [], []
    for i in range(len(P)):
        for k in range(len(Q)):
            
            if (P[i].pos() == Q[k].pos()) and (chod_sim is None):
                chod_sim = P[i].lch_similarity(Q[k])

            wup.append(P[i].wup_similarity(Q[k]))
            path.append(P[i].path_similarity(Q[k]))
            
            
    wup = [score for score in wup if score]
    path=[score for score in path if score]
    
    if (not wup) and (not path):
        return 0, 0, 0
        
        
    return round(max(wup),4), round(max(path),4), round(chod_sim, 4)


def google_snippets(query, num=10):
    
        query_service = build(serviceName="customsearch", version="v1", developerKey='AIzaSyAz3LheHf9jWsSEztGf5B1TAeiv0FbAsZo') 
        query_results = query_service.cse().list(q=query,cx='fd2dd246666e2965a', num=num
                                                ).execute()
        return query_results['items']



def sim_snippets1(snipp_p, snipp_q):
    snippets_p, snippets_q = '', ''
    
    for i in range(5):
        if i < len(snipp_p):
            snippets_p += pre_processing(snipp_p[i]['snippet'])
            snippets_p +=' '
        
    if i < len(snipp_q):
        snippets_q += pre_processing(snipp_q[i]['snippet'])
        snippets_q += ' ' 
    
    common_words = len(set(snippets_p.strip().split(' ')) & set(snippets_q.strip().split(' '))) 
    combined_unique_words = len(set(snippets_p + snippets_q))
    
#     print(common_words/combined_unique_words)
    return common_words/combined_unique_words
    


def sim_snippets2(snippet_p, snippet_q):
    
    
    snippets_p, snippets_q='',''
    for i in range(10):
        if i < len(snippet_p):
            if 'snippet' in snippet_p[i].keys():
                snippets_p += pre_processing(snippet_p[i]['snippet'])
                snippets_p +=' '
        
        if i < len(snippet_q):
            if 'snippet' in snippet_q[i].keys():
                snippets_q += pre_processing(snippet_q[i]['snippet'])
                snippets_q += ' ' 

    return round(lev.ratio(snippets_p, snippets_q),4)


def concat():
    
    df_mc = pd.read_csv('mc.csv', sep=';', names=['Word 1', 'Word 2', 'Human Judgement Score'])
    df_rg = pd.read_csv('rg.csv', sep=';', names=['Word 1', 'Word 2', 'Human Judgement Score'])
    df_wordsim = pd.read_csv('wordsim.csv', sep=';', names=['Word 1', 'Word 2', 'Human Judgement Score'])

    data = pd.concat([df_mc, df_rg, df_wordsim])
    
    return data


def plotting_correlation(data, col1, col2):
    
    plt.figure(figsize=(10,8))
    plt.scatter(data[col1], data[col2])
    sns.despine()
    sns.set(font_scale=1)
    corr = round(data[[col1, col2]].corr().iloc[0,1], 3)

    plt.title('Correlation : {}\n\n'.format(corr))
    plt.xlabel(col1)
    plt.xlabel(col2)
    plt.show()

data = pd.read_csv('correlations.csv')

#@app.route('/', methods=("POST", "GET"))
#def pre_worked(data=data):
    #df = pd.read_csv('Compiled_results.csv')
    #data = pd.read_csv('correlations.csv')
#    return flask.render_template('about.html',tables=[data.to_html(classes='data')], titles=data.columns.values)


#if __name__ == '__main__':
 #app.run(debug=True)

#print(wordnet_sim('tiger', 'tiger'))









