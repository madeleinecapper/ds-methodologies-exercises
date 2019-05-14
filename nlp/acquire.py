import requests
from bs4 import BeautifulSoup as bsoup
import os
import json
import itertools as it
import pandas as pd
from typing import List, Dict

web_list_default = ['https://codeup.com/codeups-data-science-career-accelerator-is-here/',\
                    'https://codeup.com/data-science-myths/',\
                    'https://codeup.com/data-science-vs-data-analytics-whats-the-difference/',\
                    'https://codeup.com/10-tips-to-crush-it-at-the-sa-tech-job-fair/',\
                    'https://codeup.com/competitor-bootcamps-are-closing-is-the-model-in-danger/']


def get_article_titles(web_list = web_list_default):
    '''grabs article titles from websites on Codeup Blog, returns them as a list of strings'''
    headers = {'User-Agent': 'Codeup Ada Data Science'}
    article_titles = []
    for site in web_list:
        response = requests.get(site, headers=headers)
        soup = bsoup(response.text)
        if len(soup.find_all(class_='page-title')) > 0:
            article_titles.append(soup.find(class_='page-title').text)
        else:
            article = soup.find(class_='mk-single-content').text
            title = article.split('\n')[1]
            article_titles.append(title)
    return article_titles
    
def get_article_bodies(web_list=web_list_default):
    '''grabs article bodies from websites on Codeup Blog, returns list of strings'''
    headers = {'User-Agent': 'Codeup Ada Data Science'}
    article_bodies = []
    for site in web_list:
        response = requests.get(site, headers=headers)
        soup = bsoup(response.text)
        if len(soup.find_all(class_='page-title')) > 0:
            article_bodies.append(soup.find(class_='mk-single-content').text)
        else:
            article = soup.find(class_='mk-single-content').text
            body = article.split('\n')[2:]
            article_bodies.append(body)
    return article_bodies


def get_blog_articles(use_cache=True, web_list = web_list_default) -> List[Dict[str, str]]:
    '''
    Checks to see if cache has data already stored of blog data, if not, function creates a 
    list of dictionaries with a 'title' and 'content' key per entry
    '''
    if use_cache and os.path.exists('blog_articles.json'):
        article_list = json.load(open('blog_articles.json'))
        return article_list
    elif len(get_article_titles(web_list)) == len(get_article_bodies(web_list)):
        article_titles = get_article_titles(web_list)
        article_bodies = get_article_bodies(web_list)
        article_list = []
        if len(article_titles) == len(article_bodies):
            for i in range(0, len(article_titles)):
                article_list.append({'title': article_titles[i], 'content': article_bodies[i]})
            json.dump(article_list, open('blog_articles.json', 'w'))
            return article_list
    else:
        print('Something went wrong.  You have {} article titles and {} artilcle bodies'.format(len(article_titles), len(article_bodies)))

BASE_URL = 'https://inshorts.com/en/read'
SECTIONS = ['business', 'sports', 'technology', 'entertainment']

def handle_article(article) -> Dict[str, str]:
    '''
    Given a single article, extracts the title and content
    '''
    return {
        'title': article.find(class_='news-card-title').find('a').text.strip(),
        'content': (article.find(class_='news-card-content')
                    .find('div', attrs={'itemprop': 'articleBody'})
                    .text.strip())
    }

def fetch_section(section: str) -> List[Dict[str, str]]:
    '''
    Makes a request for the given section and processes all the articles in it
    '''
    url = f'{BASE_URL}/{section}'
    response = requests.get(url)
    soup = bsoup(response.text)
    articles = [handle_article(article) for article in soup.find_all(class_='news-card')]
    for article in articles:
        article['category'] = section
    return articles

def get_all_sections() -> List[Dict[str, str]]:
    '''
    Returns the processed article data for all of the sections we defined in
    SECTIONS
    '''
    sections = [fetch_section(section) for section in SECTIONS]
    # flatten out the nested lists with it.chain
    return list(it.chain(*sections))

def get_news_articles(use_cache=True) -> List[Dict[str, str]]:
    if use_cache and os.path.exists('news_articles.json'):
        articles = json.load(open('news_articles.json'))
    else:
        articles = get_all_sections()
        json.dump(articles, open('news_articles.json', 'w'))
    return articles

def get_news_data() -> pd.DataFrame:
    '''
    Returns all the articles from all the sections as a pandas DataFrame
    '''
    return pd.DataFrame(get_all_sections())