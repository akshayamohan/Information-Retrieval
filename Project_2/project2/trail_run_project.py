from tqdm import tqdm

import collections
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
import nltk
import random
# nltk.download('stopwords')

from linkedlist import LinkedList
from indexer import Indexer
from run_project import ProjectRunner


projectRunner = ProjectRunner()

text = '			Evaluation of SARS-CoV-2 RNA shedding in clinical       specimens of 10 patients Evaluation with evaluation COVID-19 in Macau    '

corpus = 'data/input_corpus.txt'
projectRunner.run_indexer(corpus)
print(len(projectRunner._get_postings('patient')))
print(len(projectRunner._get_skip_postings('patient')))
# index = projectRunner.indexer.get_index()
# kw = random.choice(list(index.keys()))
# print(index[kw].start_node.value)