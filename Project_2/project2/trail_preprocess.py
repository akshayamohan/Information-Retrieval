from tqdm import tqdm

import collections
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
import nltk
# nltk.download('stopwords')

from linkedlist import LinkedList
from indexer import Indexer
from run_project import ProjectRunner


def tokenizer(text):
    """ Implement logic to pre-process & tokenize document text.
        Write the code in such a way that it can be re-used for processing the user's query.
        To be implemented."""


    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()

    text = text.lower()
    text = re.sub('[^a-z0-9]+', ' ', text)
    text = re.sub(' +', ' ', text)
    text = text.strip()
    tokens = re.split("\s", text)

    processed_tokens = []

    for w in tokens:
    	if w not in stop_words:
    		ps_w = ps.stem(w)
    		processed_tokens.append(ps_w)

    return processed_tokens


def _merge(posting_list_obj_term1, posting_list_obj_term2, num_comparisons):
    """ Implement the merge algorithm to merge 2 postings list at a time.
        Use appropriate parameters & return types.
        While merging 2 postings list, preserve the maximum tf-idf value of a document.
        To be implemented."""
    resultant_list = LinkedList()
    # posting_list_obj_term1 = index.get(term1)
    # posting_list_obj_term2 = index.get(term2)
    if (posting_list_obj_term1 is not None) and (posting_list_obj_term2 is not None):
        m = posting_list_obj_term1.start_node
        n = posting_list_obj_term2.start_node
        while (m is not None) and (n is not None):
            num_comparisons += 1
            if m.value == n.value:
                resultant_list.insert_at_end(m.value,1)
                m = m.next
                n = n.next
            else:
                if m.value < n.value:
                    m = m.next
                else:
                    n = n.next
    return resultant_list, num_comparisons

def _merge_with_skips(posting_list_obj_term1, posting_list_obj_term2, num_comparisons):
    
    resultant_list = LinkedList()
    if (posting_list_obj_term1 is not None) and (posting_list_obj_term2 is not None):
        m = posting_list_obj_term1.start_node
        n = posting_list_obj_term2.start_node
        while (m is not None) and (n is not None):
            num_comparisons += 1
            if m.value == n.value:
                resultant_list.insert_at_end(m.value,1)
                m = m.next
                n = n.next
            elif m.value < n.value:
                if(m.skip_link is not None) and (m.skip_link.value <= n.value):
                    m = m.skip_link
                else:
                    m = m.next
            else:
                if(n.skip_link is not None) and (n.skip_link.value <= m.value):
                    n = n.skip_link
                else:
                    n = n.next
    return resultant_list, num_comparisons

def _daat_and(tokenized_query):
        """ Implement the DAAT AND algorithm, which merges the postings list of N query terms.
            Use appropriate parameters & return types.
            To be implemented."""
        output_list = []
        num_comparisons = 0
        index = indexer.get_index()
        if len(tokenized_query) > 1:
            posting_list_obj_term1 = index.get(tokenized_query[0])
            posting_list_obj_term2 = index.get(tokenized_query[1])
            resultant_list, num_comparisons = _merge(posting_list_obj_term1, posting_list_obj_term2, num_comparisons)
            for i in range(len(tokenized_query)-2):
                posting_list_obj_term = index.get(tokenized_query[i+2])
                resultant_list, num_comparisons = _merge(resultant_list, posting_list_obj_term, num_comparisons)
            if resultant_list.start_node is not None:    
                output_list = resultant_list.traverse_list()
        elif len(tokenized_query) == 1:
            output_list = _get_postings(tokenized_query[0])
        return output_list, num_comparisons

def _daat_and_with_skips(tokenized_query):
    """ Implement the DAAT AND algorithm, which merges the postings list of N query terms.
        Use appropriate parameters & return types.
        To be implemented."""
    output_list = []
    num_comparisons = 0
    index = indexer.get_index()
    if len(tokenized_query) > 1:
        posting_list_obj_term1 = index.get(tokenized_query[0])
        posting_list_obj_term2 = index.get(tokenized_query[1])
        resultant_list, num_comparisons = _merge_with_skips(posting_list_obj_term1, posting_list_obj_term2, num_comparisons)
        for i in range(len(tokenized_query)-2):
            posting_list_obj_term = index.get(tokenized_query[i+2])
            resultant_list, num_comparisons = _merge_with_skips(resultant_list, posting_list_obj_term, num_comparisons)
        if resultant_list.start_node is not None:    
            output_list = resultant_list.traverse_list()
    elif len(tokenized_query) == 1:
        output_list = _get_postings(tokenized_query[0])
    return output_list, num_comparisons

def _get_postings(self, term):
        """ Function to get the postings list of a term from the index.
            Use appropriate parameters & return types.
            To be implemented."""
        postings = []
        index = self.indexer.get_index()
        posting_list_obj = index.get(term)
        if posting_list_obj is not None:
            postings = posting_list_obj.traverse_list()
            return postings
        else:
            return postings


text1 = '			Evaluation of SARS-CoV-2 RNA shedding in clinical       specimens of 10 patients Evaluation with evaluation COVID-19 in Macau    '
text2 = 'A Rational Use of Clozapine Based on Adverse Drug Reactions, Pharmacokinetics, and Clinical Pharmacopsychology'
processed_tokens1  = tokenizer(text1)
processed_tokens2 = tokenizer(text2)
# print(processed_tokens)

# linked_list = LinkedList()
# linked_list.insert_at_end(20)
# [linked_list.insert_at_end(i) for i in [42, 111, 13, 29, 7, -11]]
# linked_list.insert_at_end(25)
# list_values = linked_list.traverse_list()


indexer = Indexer()
tokenized_document1 = ['evalu']
tokenized_document2 = ['clinic']
tokenized_document3 = ['patient']

indexer.generate_inverted_index(1, tokenized_document1)
indexer.generate_inverted_index(2, tokenized_document1)
indexer.generate_inverted_index(5, tokenized_document1)
indexer.generate_inverted_index(9, tokenized_document1)
indexer.generate_inverted_index(10, tokenized_document1)
indexer.generate_inverted_index(7, tokenized_document2)
indexer.generate_inverted_index(8, tokenized_document2)
indexer.generate_inverted_index(9, tokenized_document2)
indexer.generate_inverted_index(10, tokenized_document2)
indexer.generate_inverted_index(9, tokenized_document3)
indexer.generate_inverted_index(10, tokenized_document3)


index = indexer.get_index()
posting_list1 = index.get('evalu')
posting_list2 = index.get('clinic')
posting_list3 = index.get('patient')

query = ['evalu', 'clinic', 'patient']

posting_list1.add_skip_connections()
posting_list2.add_skip_connections()

print(posting_list1.traverse_list())
print(posting_list2.traverse_list())
print(posting_list3.traverse_list())

resultant_list, num_comparisons = _merge(posting_list1,posting_list2,0)

print('----------------------------')
print(resultant_list.traverse_list())
print('comaprisons: '+str(num_comparisons))

resultant_list, num_comparisons = _merge_with_skips(posting_list1,posting_list2,0)

print('----------------------------')
print(resultant_list.traverse_list())
print('comaprisons: '+str(num_comparisons))

print('---------------------------')
resultant_list, num_comparisons = _daat_and(query)
print(resultant_list)
print('comaprisons: '+str(num_comparisons))

print('---------------------------')
resultant_list, num_comparisons = _daat_and_with_skips(query)
print(resultant_list)
print('comaprisons: '+str(num_comparisons))


# tokenized_document = ['evalu']

# indexer = Indexer()
# indexer.generate_inverted_index(21, processed_tokens)
# indexer.generate_inverted_index(20, tokenized_document)
# for i in range(9):
#     indexer.generate_inverted_index(i+1, tokenized_document)
# indexer.calculate_tf_idf()
# index = indexer.get_index()

# print('total num of docs: ' + str(indexer.total_docs))

# posting_list = index.get('evalu')

# projectRunner = ProjectRunner()
# postings = projectRunner._get_postings('evalu')
# print(postings)

# print(index)
# print(len(processed_tokens))
# print('-------------------')
# print(posting_list.traverse_list())
# print(posting_list.end_node.tf)
# print(posting_list.end_node.tf_idf)
# print(posting_list.length)
# print(posting_list.end_node.value)
# print(posting_list.add_skip_connections())
# print(posting_list.traverse_skips())

# print('-------------------')
# posting_list1 = index.get('2')
# print(posting_list1.traverse_list())
# print(posting_list1.length)
# print(posting_list1.end_node.tf)
# print(posting_list1.end_node.tf_idf)

# traversal = []
#         if self.start_node is None:
#             return
#         else:
#             while self.start_node.skip_link is not None:
#                 traversal = []
                
#                 n = self.start_node
#                 # Start traversal from head, and go on till you reach None
#                 while n is not None:
#                     traversal.append(n.value)
#                     n = n.skip_link
#                 return traversal



