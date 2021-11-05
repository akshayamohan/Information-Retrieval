import os
import pysolr
import requests
import json
import re

import urllib
import urllib.request

from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

CORE_NAME = "IRF21_BM25"
AWS_IP = "localhost"

core_names = ["IRF21_BM25", "IRF21_VSM"]

stop_words = set(stopwords.words('english'))
ps = PorterStemmer()


#TODO-remove after private access

with open('train.json') as json_file:
  collection = json.load(json_file)


def delete_core(core=CORE_NAME):
    print(os.system('sudo su - solr -c "/opt/solr/bin/solr delete -c {core}"'.format(core=core)))


def create_core(core=CORE_NAME):
    print(os.system(
        'sudo su - solr -c "/opt/solr/bin/solr create -c {core} -n data_driven_schema_configs"'.format(
            core=core)))

class Indexer:
    def __init__(self):
        self.solr_url = f'http://{AWS_IP}:8983/solr/'
        self.connection = pysolr.Solr(self.solr_url + CORE_NAME, always_commit=True, timeout=5000000)

    def do_initial_setup(self):
        delete_core()
        create_core()

    def create_documents(self, docs):
        print(self.connection.add(docs))

    def add_fields(self):
        print("adding fields")
        data = {
            "add-field": [
                {
                    "name": "lang",
                    "type": "text_general",
                    "multiValued": False
                },
                {
                    "name": "text_de",
                    "type": "text_de",
                    "multiValued": False
                },
                {
                    "name": "text_en",
                    "type": "text_en",
                    "multiValued": False
                },
                {
                    "name": "text_ru",
                    "type": "text_ru",
                    "multiValued": False
                },
                {
                    "name": "tweet_hashtags",
                    "type": "strings",
                    "multiValued": True
                }, 
                {
                    "name": "tweet_urls",
                    "type": "strings",
                    "multiValued": True
                },
            ]
        }

        print(requests.post(self.solr_url + CORE_NAME + "/schema", json=data).json())

    def replace_BM25(self, b=None, k1=None):
        data = {
            "replace-field-type": [
                {
                    'name': 'text_en',
                    'class': 'solr.TextField',
                    'positionIncrementGap': '100',
                    'indexAnalyzer': {
                        'tokenizer': {
                            'class': 'solr.StandardTokenizerFactory'
                        },
                        'filters': [{
                            'class': 'solr.StopFilterFactory',
                            'words': 'lang/stopwords_en.txt',
                            'ignoreCase': 'true'
                        }, {
                            'class': 'solr.LowerCaseFilterFactory'
                        }, {
                            'class': 'solr.EnglishPossessiveFilterFactory'
                        }, {
                            'class': 'solr.KeywordMarkerFilterFactory',
                            'protected': 'protwords.txt'
                        }, {
                            'class': 'solr.PorterStemFilterFactory'
                        }]
                    },
                    'similarity': {
                        'class': 'solr.BM25SimilarityFactory',
                        'b': str(b),
                        'k1': str(k1)
                    },
                    'queryAnalyzer': {
                        'tokenizer': {
                            'class': 'solr.StandardTokenizerFactory'
                        },
                        'filters': [{
                            'class': 'solr.SynonymGraphFilterFactory',
                            'expand': 'true',
                            'ignoreCase': 'true',
                            'synonyms': 'synonyms.txt'
                        }, {
                            'class': 'solr.StopFilterFactory',
                            'words': 'lang/stopwords_en.txt',
                            'ignoreCase': 'true'
                        }, {
                            'class': 'solr.LowerCaseFilterFactory'
                        }, {
                            'class': 'solr.EnglishPossessiveFilterFactory'
                        }, {
                            'class': 'solr.KeywordMarkerFilterFactory',
                            'protected': 'protwords.txt'
                        }, {
                            'class': 'solr.PorterStemFilterFactory'
                        }]
                    }
                }, {
                    'name': 'text_ru',
                    'class': 'solr.TextField',
                    'positionIncrementGap': '100',
                    'analyzer': {
                        'tokenizer': {
                            'class': 'solr.StandardTokenizerFactory'
                        },
                        'filters': [{
                            'class': 'solr.LowerCaseFilterFactory'
                        }, {
                            'class': 'solr.StopFilterFactory',
                            'format': 'snowball',
                            'words': 'lang/stopwords_ru.txt',
                            'ignoreCase': 'true'
                        }, {
                            'class': 'solr.SnowballPorterFilterFactory',
                            'language': 'Russian'
                        }]
                    },
                    'similarity': {
                        'class': 'solr.BM25SimilarityFactory',
                        'b': str(b),
                        'k1': str(k1)
                    },
                }, {
                    'name': 'text_de',
                    'class': 'solr.TextField',
                    'positionIncrementGap': '100',
                    'analyzer': {
                        'tokenizer': {
                            'class': 'solr.StandardTokenizerFactory'
                        },
                        'filters': [{
                            'class': 'solr.LowerCaseFilterFactory'
                        }, {
                            'class': 'solr.StopFilterFactory',
                            'format': 'snowball',
                            'words': 'lang/stopwords_de.txt',
                            'ignoreCase': 'true'
                        }, {
                            'class': 'solr.GermanNormalizationFilterFactory'
                        }, {
                            'class': 'solr.GermanLightStemFilterFactory'
                        }]
                    },
                    'similarity': {
                        'class': 'solr.BM25SimilarityFactory',
                        'b': str(b),
                        'k1': str(k1)
                    },
                }
            ]
        }

        print(requests.post(self.solr_url + CORE_NAME + "/schema", json=data).json())

    def query_solr(self):

        # with open('test-queries.txt') as fp:
        with open('queries.txt') as fp:

            for core in core_names:
                print('processing core: '+core)
                for line in fp:
                    query_id, query = line.split(' ', 1)
                    query = re.sub(r'[^\w\s]', ' ', query)
                    query = re.sub(' +', ' ', query)
                    query = query.strip()
                    
                    tokens = re.split("\s", text)

                    processed_tokens = []

                    for w in tokens:
                        if w not in stop_words:
                            ps_w = ps.stem(w)
                            processed_tokens.append(ps_w)

                    query = ' '.join(processed_tokens)
                    encoded_query = urllib.parse.quote(query)

                    print(encoded_query)

                    inurl = 'http://localhost:8983/solr/' + core + '/select?fl=id%2Cscore&q=text_en%3A(' + encoded_query + ')%20or%20text_de%3A(' + encoded_query + ')%20or%20text_ru%3A(' + encoded_query + ')' + '&rows=20&wt=json'
                    outfn = str(int(query_id)) + '_' + core + '.txt'


                    # change query id and IRModel name accordingly
                    if core == "IRF21_BM25":
                        IRModel = 'bm25'
                    else:
                        IRModel = 'vsm'

                    # IRModel='bm25' #either bm25 or vsm
                    outf = open(outfn, 'a+')
                    # data = urllib2.urlopen(inurl)
                    # if you're using python 3, you should use
                    data = urllib.request.urlopen(inurl)

                    docs = json.load(data)['response']['docs']
                    # the ranking should start from 1 and increase
                    rank = 1
                    for doc in docs:
                        outf.write(query_id + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + IRModel + '\n')
                        rank += 1
                    outf.close()


if __name__ == "__main__":
    i = Indexer()
    # !!!!!!!!!!!! Important!!!!!!<<<<<<<<<<<<<<<<<<<<<--------------UNCOMMENT FINALLY-------------------------->>>>>>>>>>>>>>>>>>>>
    i.do_initial_setup()

    i.replace_BM25(b=0.8, k1=0.4)
    
    i.add_fields()

    i.create_documents(collection)

    i.query_solr()
