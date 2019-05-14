import unicodedata
import re
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

def basic_clean(unclean):
    '''Takes in a string and removes extraneous whitesplace in addition to normalizing it to ascii characters
    returns a version of the text that is only ascii and more specifically nothing that is a letter, number, underscore, or space.'''
    unclean = str(unclean)
    # unclean = unclean.strip()
    unclean = unclean.lower()
    unclean = re.sub('-', ' ',unclean)
    normalized = unicodedata.normalize('NFKD', unclean)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')
    normalized = ' '.join(re.sub(r'[^\w\s]', '', normalized).split())
    return normalized

def tokenize(some_text):
    '''takes in a string and tokenizes all the words in the string using ToktokTokenizer from nltk'''
    tokenizer = nltk.tokenize.ToktokTokenizer()
    some_text = tokenizer.tokenize(some_text, return_str=True)
    return some_text

def stem(some_text):
    '''accepts some text and returns the text after applying stemming to words'''
    ps = nltk.stem.PorterStemmer()
    stems = [ps.stem(word) for word in some_text.split()]
    article_stemmed = ' '.join(stems)
    return article_stemmed

def lemmatize(some_text):
    '''accepts some text and returns the text after applying lemmatization to ea word'''
    wn = nltk.stem.WordNetLemmatizer()
    lemmas = [wn.lemmatize(word.lower()) for word in some_text.split()]
    article_lemmatized = ' '.join(lemmas)
    return article_lemmatized

def remove_stopwords(some_text, extra_words = [], exclude_words = []):
    '''accepts some text and returns it after removing stopwords'''
    stopword_list = stopwords.words('english')
    [stopword_list.append(word) for word in extra_words if word not in stopword_list]
    [stopword_list.remove(word) for word in exclude_words if word in stopword_list]
    word_list = some_text.split()
    filtered_words = [w for w in word_list if w not in stopword_list]
    return ' '.join(filtered_words)

def prep_article(d_content, extra_words = [], exclude_words = []):
    if 'title' and 'content' and 'category' in list(d_content.keys()):
        cleaned = basic_clean(d_content['content'])
        tokened = tokenize(cleaned)
        prepped_content = {
            'title': d_content['title'],
            'category': d_content['category'],
            'original': d_content['content'],
            'stemmed': stem(tokened),
            'lemmatized': lemmatize(tokened),
            'clean': remove_stopwords(tokened, extra_words, exclude_words)
        }
        return prepped_content
    elif 'title' and 'content' in list(d_content.keys()):
        cleaned = basic_clean(d_content['content'])
        tokened = tokenize(cleaned)
        prepped_content = {
            'title': d_content['title'],
            'original': d_content['content'],
            'stemmed': stem(tokened),
            'lemmatized': lemmatize(tokened),
            'clean': remove_stopwords(tokened, extra_words, exclude_words)
        }
        return prepped_content
    else:
        print('~~~Function requires a dictionary with a \'title\' and \'content\' key.~~~')

def prepare_article_data(list_o_dicts, extra_words = [], exclude_words = []):
    return [prep_article(art, extra_words, exclude_words) for art in list_o_dicts]