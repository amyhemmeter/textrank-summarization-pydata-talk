from newsapi import NewsApiClient
from bs4 import BeautifulSoup
import requests
import json
import re
from nltk import sent_tokenize

api_key = 'faf93487cd524c7abdfb28b0ce86c201'
newsapi = NewsApiClient(api_key=api_key)

def get_urls(keyword, news_source, newsapi, date_from, date_to):
  articles = newsapi.get_everything(q=keyword,
                                    sources=news_source,
                                    from_param=date_from,
                                    to=date_to,
                                    language='en',
                                    sort_by='relevancy')
  return articles

def format_stories(news_articles, source_name):
  stories = {}
  for x in news_articles['articles']:
    stories[x['title']] = x['url']

  article_number = 1

  name = source_name
  print('Finding ' + source_name + ' stories')
  for k,v in stories.items():
    req = requests.get(v)
    soup = BeautifulSoup(req.text, 'html.parser')
    story = soup.findAll('p')
    story_strings = [str(x).replace('</p>','').split('>')[1] for x in story]
    story_sents = sent_tokenize(' '.join(story_strings))
    file_string = 'data/' + source_name + '-story-' + str(article_number) + '.json'
    story_sents = story_sents[:-1]
    if name=='CBC':
      story_sents = story_sents[:-5]
    with open(file_string, 'w') as outfile:
      #story_sents = [sent.encode('utf8') for sent in story_sents]
      json.dump(story_sents, outfile)
    article_number += 1


ap_articles = get_urls('science', 'associated-press', newsapi, '2020-01-01', '2020-01-19')
format_stories(ap_articles,'AP')
aj_articles = get_urls('science', 'cbc-news', newsapi, '2020-01-01', '2020-01-19')
format_stories(aj_articles, 'CBC')
r_articles = get_urls('science', 'reuters', newsapi, '2020-01-01', '2020-01-19')
format_stories(r_articles, 'Reuters')