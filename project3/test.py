import os
import pysolr
import requests
import json
import re

import urllib
import urllib.request 

CORE_NAME = "IRF21_BM25"
AWS_IP = "localhost"

core_names = ["IRF21_BM25", "IRF21_VSM"]

# with open('test-queries.txt') as fp:
#     for line in fp:
#         query_id, query = line.split(' ', 1)
#         query = re.sub(r'[^\w\s]', ' ', query)
#         query = re.sub(' +', ' ', query)
#         query = query.strip()
#         encoded_query = urllib.parse.quote(query)
#         print (encoded_query)

#         query_url = 'http://localhost:8983/solr/' + core + '/select?fl=id%2Cscore&q=text_en%3A(' \
#                             + encoded_query + ')%20or%20text_de%3A(' + encoded_query + ')%20or%20text_ru%3A(' \
#                             + encoded_query + ')' + '&rows=20&wt=json'

# print(str(int('002')))

def query_solr():

    print("inside new code")
    with open('test-queries.txt') as fp:
    # with open('queries.txt') as fp:

        for core in core_names:
            print('working on core: '+core)
            for line in fp:
                query_id, query = line.split(' ', 1)
                query = re.sub(r'[^\w\s]', ' ', query)
                query = re.sub(' +', ' ', query)
                query = query.strip()
                encoded_query = urllib.parse.quote(query)

                inurl = 'http://localhost:8983/solr/' + core + '/select?fl=id%2Cscore&q=text_en%3A(' + encoded_query + ')%20or%20text_de%3A(' + encoded_query + ')%20or%20text_ru%3A(' + encoded_query + ')' + '&rows=20&wt=json'
                outfn = 'test'+str(int(query_id)) + '_' + core + '.txt'


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

                print('reponse received: '+ data)

                docs = json.load(data)['response']['docs']
                # the ranking should start from 1 and increase
                rank = 1
                for doc in docs:
                    outf.write(query_id + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + IRModel + '\n')
                    rank += 1
                outf.close()


query_solr()