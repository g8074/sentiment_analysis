# -*- coding: utf-8 -*-
"""sentiment analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Db0Zoo3EmC6XY4TKVL5srBlNr16J38Pa
"""

!pip install vaderSentiment

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
vs=SentimentIntensityAnalyzer()

text='The product is really good'
vs.polarity_scores(text)

text2='Who all loves older size i.e., 4.7 inch should definitely go for this.Nothing is better than XR,XS or 11.Best for price and usage'
vs.polarity_scores(text)

text3='Everything is fine of the mobile except battery'
vs.polarity_scores(text)

#web scraping

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os

url='https://www.inshorts.com/en/read/sports'
news_data=[]
new_category=url.split('/')[-1]
data=requests.get(url)
soup=BeautifulSoup(data.content)
print(soup)

urls=['https://www.inshorts.com/en/read/sports',
      'https://www.inshorts.com/en/read/world',
      'https://www.inshorts.com/en/read/politics']

def build_dataset(urls):
  news_data=[]
  for u in urls:
    soup=BeautifulSoup(requests.get(u).content)
    category=u.split('/')[-1]                           
    news_article =[{'news_headline': headline.find('span', attrs={"itemprop":"headline"}).string,
                    'news_article': article.find('div', attrs={"itemprop":"articleBody"}).string,
                    'news_category': category}
                   for headline,article in zip(soup.find_all('div',class_=["news-card-title news-right-box"]),
                                               soup.find_all('div',class_=["news-card-content news-right-box"]))
                   ]
    news_article = news_article[0:20]
    news_data.extend(news_article)
  df=pd.DataFrame(news_data)
  df=df[['news_headline','news_article', 'news_category']]
  return df

df=build_dataset(urls)
df.head()

df=build_dataset(urls)
df.tail()

df.to_csv('news.csv',index=False)

import pandas as pd
df=pd.read_csv('https://raw.githubusercontent.com/krishna2824/krishna-shree/master/news.csv')
df

!pip install nltk

import nltk
nltk.download('stopwords')
stopword_list = nltk.corpus.stopwords.words('english')
stopword_list.remove('no')
stopword_list.remove('not')
len(stopword_list)

# function to remove HTML tag
def html_tag(text):
  soup=BeautifulSoup(text,"html.parser")
  new_text = soup.get_text()
  return new_text

# Expand Contraction
!pip install contractions
import contractions
def con(text):
  expand=contractions.fix(text)
  return expand
con("Y'all can't expand I'd think")

#removal of special charecters
import re
def remove_sp(text):
  pattern= r'[^A-Za-z0-9\s]'
  text= re.sub(pattern,'',text)
  return text

remove_sp("weel this was fun !! what do you think?. #123")

from nltk.tokenize.toktok import ToktokTokenizer
tokenizer=ToktokTokenizer

#removal of stopwords
tokenizer = ToktokTokenizer()
def remove_stopwords(text):
  tokens = tokenizer.tokenize(text)
  tokens = [token.strip() for token in tokens]
  filtered_tokens = [token for token in tokens if token not in stopword_list]
  filtered_text= ' '.join(filtered_tokens)
  return filtered_text

remove_stopwords("The, and , if are all stop words and even not")

#1. Lower case
#2. HTMP tags
#3. Contractions
#4. Stopwords
df.news_headline=df.news_headline.apply(lambda x:x.lower())
df.news_article=df.news_article.apply(lambda x:x.lower())


df.news_headline=df.news_headline.apply(html_tag)
df.news_article=df.news_article.apply(html_tag)

df.news_headline=df.news_headline.apply(con)
df.news_article=df.news_article.apply(con)


df.news_headline=df.news_headline.apply(remove_sp)
df.news_article=df.news_article.apply(remove_sp)

df.news_headline=df.news_headline.apply(remove_stopwords)
df.news_article=df.news_article.apply(remove_stopwords)

# dataset labeling and processing
df['compound'] = df['news_headline'].apply(lambda x: vs.polarity_scores(x)['compound'])
df.head()

# data finalization 
def predict(comp):
  comp=float(comp)
  if (comp>0):
    return 'positive'
  elif (comp==0):
    return 'neutral'
  else:
    return 'negative'
df['type_pred'] = df['compound'].apply(predict)
df.head()

