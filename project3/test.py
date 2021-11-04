import re
import urllib.request
import urllib

with open('test-queries.txt') as fp:
    for line in fp:
        query_id, query = line.split(' ', 1)
        query = re.sub(r'[^\w\s]', ' ', query)
        query = re.sub(' +', ' ', query)
        query = query.strip()
        encoded_query = urllib.parse.quote(query)
        print (encoded_query)

        query_url = 'http://localhost:8983/solr/' + core + '/select?fl=id%2Cscore&q=text_en%3A(' \
                            + encoded_query + ')%20or%20text_de%3A(' + encoded_query + ')%20or%20text_ru%3A(' \
                            + encoded_query + ')' + '&rows=20&wt=json'

print(str(int('002')))