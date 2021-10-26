'''
@author: Sougata Saha
Institute: University at Buffalo
'''

from linkedlist import LinkedList
from collections import OrderedDict


class Indexer:
    def __init__(self):
        """ Add more attributes if needed"""
        self.inverted_index = OrderedDict({})
        self.total_docs = 0

    def get_index(self):
        """ Function to get the index.
            Already implemented."""
        return self.inverted_index

    def generate_inverted_index(self, doc_id, tokenized_document):
        """ This function adds each tokenized document to the index. This in turn uses the function add_to_index
            Already implemented."""
        self.total_docs += 1
        for t in tokenized_document:
            num_tokens_in_doc = len(tokenized_document)
            self.add_to_index(t, doc_id, num_tokens_in_doc)

    def add_to_index(self, term_, doc_id_, num_tokens_in_doc):
        """ This function adds each term & document id to the index.
            If a term is not present in the index, then add the term to the index & initialize a new postings list (linked list).
            If a term is present, then add the document to the appropriate position in the posstings list of the term.
            To be implemented."""
        
        if term_ in self.inverted_index:
            posting_list = self.inverted_index.get(term_)
            if(posting_list.is_not_duplicate(doc_id_, num_tokens_in_doc)):
                posting_list.insert_at_end(doc_id_, num_tokens_in_doc, 0)
        else:
            key = (term_)
            linked_list = LinkedList()
            linked_list.insert_at_end(doc_id_, num_tokens_in_doc, 0)
            value = linked_list
            self.inverted_index[key] = value

    def sort_terms(self):
        """ Sorting the index by terms.
            Already implemented."""
        sorted_index = OrderedDict({})
        for k in sorted(self.inverted_index.keys()):
            sorted_index[k] = self.inverted_index[k]
        self.inverted_index = sorted_index

    def add_skip_connections(self):
        """ For each postings list in the index, add skip pointers.
            To be implemented."""
        for key in self.inverted_index:
            posting_list = self.inverted_index.get(key)
            posting_list.add_skip_connections()

    def calculate_tf_idf(self):
        """ Calculate tf-idf score for each document in the postings lists of the index.
            To be implemented."""
        for key in self.inverted_index:
            posting_list = self.inverted_index.get(key)
            idf = self.total_docs/posting_list.length
            posting_list.add_tf_idf_score(idf)
