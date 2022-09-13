import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd

def basic_clean(string):
    string = string.lower()
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    string = re.sub(r"[^a-z0-9'\s]", '', string)
    return string

def tokenize(string):
    tokenizer = ToktokTokenizer()
    string = tokenizer.tokenize(string, return_str=True)

    return string

def stem(string):
    # Create the nltk stemmer object, then use it
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in string.split()]
    string = ' '.join(stems)

    return string

def lemmatize(string):
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    string = ' '.join(lemmas)
    
    return string

def remove_stopwords(string, extra_words = [], exclude_words = []):
    '''
    Takes in a string and optional lists of stopwords to add and remove from the string, and returns the string without stopwords
    '''
    stopword_list = stopwords.words('english')
    # Remove stopwords to remove
    for word in exclude_words:
        stopword_list.remove(word)
    # Adds additional stopwords
    for word in extra_words:
        stopword_list.append(word)
    words = string.split()
    filtered_words = [w for w in words if w not in stopword_list]
    print('Removed {} stopwords'.format(len(words) - len(filtered_words)))

    stopwordless_string = ' '.join(filtered_words)

    return stopwordless_string

def remove_smalls(string):
    words = string.split()
    return words


def full_clean(string, extra_words = [], exclude_words = [], stem_or_lemma = 'lemma'):
    '''
    Function combines all NLP cleaning steps:
    1. Basic clean makes it lower case, removes non-unicode and special characters
    2. Tokenize
    3. Stem or Lemmatized based on parameter input - default is lemmatize
    4. Remove stopwords
    5. Remove all 'words' less than two characters long
    '''
    string = basic_clean(string)
    string = tokenize(string)
    if stem_or_lemma == 'lemma':
        string = lemmatize(string)
    else:
        string = stem(string)
    cleaned_string = remove_stopwords(string, extra_words, exclude_words)

    return cleaned_string