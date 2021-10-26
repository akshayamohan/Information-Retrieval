'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import collections
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')


class Preprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.ps = PorterStemmer()

    def get_doc_id(self, doc):
        """ Splits each line of the document, into doc_id & text.
            Already implemented"""
        arr = doc.split("\t")
        return int(arr[0]), arr[1]

    def tokenizer(self, text):
        text = text.lower()
        text = re.sub('[^a-z0-9]+', ' ', text)
        text = re.sub(' +', ' ', text)
        text = text.strip()
        tokens = re.split("\s", text)

        processed_tokens = []

        for w in tokens:
            if w not in self.stop_words:
                ps_w = self.ps.stem(w)
                processed_tokens.append(ps_w)

        return processed_tokens
