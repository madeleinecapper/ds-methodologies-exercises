import os
import re
import requests
import json
from bs4 import BeautifulSoup as bsoup

from requests import get
from os import path
import csv
import pprint 
import itertools as it
import pandas as pd


def get_repo_list():
    url_p1 = 'https://github.com/search?p='
    url_p2 = [str(i) for i in range(0,40)]
    url_p3 = '&q=stars%3A%3E0&s=stars&type=Repositories'
    repo_urls = []
    for num in url_p2:
        url = url_p1 + num + url_p3
        response = requests.get(url)
        soup = bsoup(response.text, features="lxml")
        
        middles = soup.find_all(class_='v-align-middle')
        urls = middles[-10:]
        urls = [urls[i].text for i in range(0, len(urls))]
        repo_urls = repo_urls + urls
        
    print('status:', response.status_code)
    
    return repo_urls


def get_all_readme_files_and_languages(urls = get_repo_list(), use_cache=True):
    '''checks for a local cache to use if possible or requested in kwargs and proceeds to hit a list of 
    urls for repositories and collects the primary coding language associated with each, in addition to 
    the body of the readme.md in each repository page as displayed inline by github'''
    if use_cache and os.path.exists('repositories.json'):
        repositories_list = json.load(open('repositories.json'))
        return repositories_list
    else:
        BASE_URL = 'https://github.com'
        SECTIONS = urls
        repositories = []

        for section in SECTIONS:
            print('github name: ', section)
            url = f'{BASE_URL}/{section}'
            print('url:', url)
            response = requests.get(url)
            soup = bsoup(response.text, features="lxml")
        
         # CREATE A LIST OF DICTIONARIES:
         # Iterating through all of the relevant repositories, extract the title and content
         # Also add the category to the dictionary.
            for repo in soup.find_all(class_="repository-content"):
                if len(repo.find_all(class_='lang')) > 1:
                    if repo.find_all(class_='lang')[0] == 'Jupyter NoteBook':
                        primary_language = repo.find_all(class_='lang')[1].text
                    else:
                        primary_language = repo.find_all(class_='lang')[0].text
                this_entry = {
                            'title': section,
                            'language': primary_language,
                            'content': (repo.find(class_='markdown-body entry-content p-5').text.strip())
                         }
                print(this_entry.keys())
                print(this_entry['title'])
                print(this_entry['language'])
                repositories.append(this_entry)
        json.dump(repositories, open('repositories.json', 'w'))
        return repositories


# The below code was done to read data files because github blocked the Codeup server 
# from making too many requests.  

def temp_get_all_readme_files_and_languages():
    BASE_URL = 'https://github.com'
    SECTIONS = ['1','2','3']
    articles = []

    for section in SECTIONS:   
        with open("page"+ section + ".html") as file: # Use file to refer to the file object
            data = file.read()

        soup = bsoup(data, features="lxml")
        
        # CREATE A LIST OF DICTIONARIES:
        # Iterating through all of the relevant articles, extract the title and content
        # Also add the category to the dictionary.

        for repo in soup.find_all(class_="repository-content"):
            if len(repo.find_all(class_='lang')) > 1:
                if repo.find_all(class_='lang')[0] == 'Jupyter NoteBook':
                    primary_language = repo.find_all(class_='lang')[1].text
                else:
                    primary_language = repo.find_all(class_='lang')[0].text
            this_entry = {
                        'title': section,
                        'language': primary_language,
                        'content': (repo.find(class_='markdown-body entry-content p-5').text.strip())
                        }
            print(this_entry.keys())
            print('this is printing the page number only for now:',this_entry['title'])
            print('primary language', this_entry['language'])
            articles.append(this_entry)

    return articles

# Now we have the web pages in a list of dictionaries