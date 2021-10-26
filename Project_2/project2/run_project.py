'''
@author: Sougata Saha
Institute: University at Buffalo
'''

from tqdm import tqdm
from preprocessor import Preprocessor
from indexer import Indexer
from collections import OrderedDict
from linkedlist import LinkedList
import inspect as inspector
import sys
import argparse
import json
import time
import random
import flask
from flask import Flask
from flask import request
import hashlib

app = Flask(__name__)


class ProjectRunner:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.indexer = Indexer()

    def _merge(self, posting_list_obj_term1, posting_list_obj_term2, num_comparisons):
        """ Implement the merge algorithm to merge 2 postings list at a time.
            Use appropriate parameters & return types.
            While merging 2 postings list, preserve the maximum tf-idf value of a document.
            To be implemented."""
        resultant_list = LinkedList()
        if (posting_list_obj_term1 is not None) and (posting_list_obj_term2 is not None):
            m = posting_list_obj_term1.start_node
            n = posting_list_obj_term2.start_node
            while (m is not None) and (n is not None):
                num_comparisons += 1
                if m.value == n.value:
                    if m.tf_idf > n.tf_idf:
                        resultant_list.insert_at_end(m.value,1, m.tf_idf)
                    else:
                        resultant_list.insert_at_end(n.value,1, n.tf_idf)
                    m = m.next
                    n = n.next
                else:
                    if m.value < n.value:
                        m = m.next
                    else:
                        n = n.next
        return resultant_list, num_comparisons

    def _merge_with_skips(self, posting_list_obj_term1, posting_list_obj_term2, num_comparisons):
    
        resultant_list = LinkedList()
        if (posting_list_obj_term1 is not None) and (posting_list_obj_term2 is not None):
            m = posting_list_obj_term1.start_node
            n = posting_list_obj_term2.start_node
            while (m is not None) and (n is not None):
                num_comparisons += 1
                if m.value == n.value:
                    if m.tf_idf > n.tf_idf:
                        resultant_list.insert_at_end(m.value,1, m.tf_idf)
                    else:
                        resultant_list.insert_at_end(n.value,1, n.tf_idf)
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
        resultant_list.add_skip_connections()
        return resultant_list, num_comparisons

    def _sort_with_tfidf(self, posting_list):

        sorted_output = []
        list_values = posting_list.dummy_traverse_list()
        list_values.sort(key = lambda x: x[1], reverse=True)
        for i in range(len(list_values)):
            sorted_output.append(list_values[i][0])
        return sorted_output
        return sorted_list

    def _sort_queries(self, tokenized_query):
        sorted_output = []
        index = self.indexer.get_index()
        query_length_tuple_list = []
        for query in tokenized_query:
            query_posting_list = index.get(query)
            if query_posting_list is not None:
                query_length_tuple_list.append((query, query_posting_list.length))
        query_length_tuple_list.sort(key = lambda x: x[1])
        for i in range(len(query_length_tuple_list)):
            sorted_output.append(query_length_tuple_list[i][0])
        return sorted_output

    def _daat_and(self, tokenized_query):
        """ Implement the DAAT AND algorithm, which merges the postings list of N query terms.
            Use appropriate parameters & return types.
            To be implemented."""
        output_list = []
        num_comparisons = 0
        index = self.indexer.get_index()
        if len(tokenized_query) > 1:
            tokenized_query = self._sort_queries(tokenized_query)
            posting_list_obj_term1 = index.get(tokenized_query[0])
            posting_list_obj_term2 = index.get(tokenized_query[1])
            resultant_list, num_comparisons = self._merge(posting_list_obj_term1, posting_list_obj_term2, num_comparisons)
            for i in range(len(tokenized_query)-2):
                posting_list_obj_term = index.get(tokenized_query[i+2])
                resultant_list, num_comparisons = self._merge(resultant_list, posting_list_obj_term, num_comparisons)
            if resultant_list.start_node is not None:    
                output_list = resultant_list.traverse_list()
        elif len(tokenized_query) == 1:
            output_list = _get_postings(tokenized_query[0])
            resultant_list = index.get(tokenized_query[0])
        return output_list, num_comparisons, resultant_list

    def _daat_and_with_skips(self, tokenized_query):
        """ Implement the DAAT AND algorithm, which merges the postings list of N query terms.
            Use appropriate parameters & return types.
            To be implemented."""
        output_list = []
        num_comparisons = 0
        index = self.indexer.get_index()
        if len(tokenized_query) > 1:
            tokenized_query = self._sort_queries(tokenized_query)
            posting_list_obj_term1 = index.get(tokenized_query[0])
            posting_list_obj_term2 = index.get(tokenized_query[1])
            resultant_list, num_comparisons = self._merge_with_skips(posting_list_obj_term1, posting_list_obj_term2, num_comparisons)
            for i in range(len(tokenized_query)-2):
                posting_list_obj_term = index.get(tokenized_query[i+2])
                resultant_list, num_comparisons = self._merge_with_skips(resultant_list, posting_list_obj_term, num_comparisons)
            if resultant_list.start_node is not None:    
                output_list = resultant_list.traverse_list()
        elif len(tokenized_query) == 1:
            output_list = _get_postings(tokenized_query[0])
            resultant_list = index.get(tokenized_query[0])
        return output_list, num_comparisons, resultant_list

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

    def _get_skip_postings(self,term):
        skip_postings = []
        index = self.indexer.get_index()
        posting_list_obj = index.get(term)
        if posting_list_obj is not None:
            skip_postings = posting_list_obj.traverse_skips()
            return skip_postings
        else:
            return skip_postings

    def _output_formatter(self, op):
        """ This formats the result in the required format.
            Do NOT change."""
        if op is None or len(op) == 0:
            return [], 0
        op_no_score = [int(i) for i in op]
        results_cnt = len(op_no_score)
        return op_no_score, results_cnt

    def run_indexer(self, corpus):
        """ This function reads & indexes the corpus. After creating the inverted index,
            it sorts the index by the terms, add skip pointers, and calculates the tf-idf scores.
            Already implemented, but you can modify the orchestration, as you seem fit."""
        with open(corpus, 'r') as fp:
            for line in tqdm(fp.readlines()):
                doc_id, document = self.preprocessor.get_doc_id(line)
                tokenized_document = self.preprocessor.tokenizer(document)
                self.indexer.generate_inverted_index(doc_id, tokenized_document)
        self.indexer.sort_terms()
        self.indexer.add_skip_connections()
        self.indexer.calculate_tf_idf()

    def sanity_checker(self, command):
        """ DO NOT MODIFY THIS. THIS IS USED BY THE GRADER. """

        index = self.indexer.get_index()
        kw = random.choice(list(index.keys()))
        return {"index_type": str(type(index)),
                "indexer_type": str(type(self.indexer)),
                "post_mem": str(index[kw]),
                "post_type": str(type(index[kw])),
                "node_mem": str(index[kw].start_node),
                "node_type": str(type(index[kw].start_node)),
                "node_value": str(index[kw].start_node.value),
                "command_result": eval(command) if "." in command else ""}

    def run_queries(self, query_list, random_command):
        """ DO NOT CHANGE THE output_dict definition"""
        output_dict = {'postingsList': {},
                       'postingsListSkip': {},
                       'daatAnd': {},
                       'daatAndSkip': {},
                       'daatAndTfIdf': {},
                       'daatAndSkipTfIdf': {},
                       'sanity': self.sanity_checker(random_command)}

        for query in tqdm(query_list):
            """ Run each query against the index. You should do the following for each query:
                1. Pre-process & tokenize the query.
                2. For each query token, get the postings list & postings list with skip pointers.
                3. Get the DAAT AND query results & number of comparisons with & without skip pointers.
                4. Get the DAAT AND query results & number of comparisons with & without skip pointers, 
                    along with sorting by tf-idf scores."""

            input_term_arr = self.preprocessor.tokenizer(query)  # Tokenized query. To be implemented.

            for term in input_term_arr:
                
                postings = self._get_postings(term)

                skip_postings = self._get_skip_postings(term)

                """ Implement logic to populate initialize the above variables.
                    The below code formats your result to the required format.
                    To be implemented."""

                output_dict['postingsList'][term] = postings
                output_dict['postingsListSkip'][term] = skip_postings



            and_op_no_skip, and_op_skip, and_op_no_skip_sorted, and_op_skip_sorted = None, None, None, None
            and_comparisons_no_skip, and_comparisons_skip, \
                and_comparisons_no_skip_sorted, and_comparisons_skip_sorted = None, None, None, None
            """ Implement logic to populate initialize the above variables.
                The below code formats your result to the required format.
                To be implemented."""

            and_op_no_skip, and_comparisons_no_skip, result_posting_list = self._daat_and(input_term_arr)
            and_op_skip, and_comparisons_skip, result_posting_list_skips = self._daat_and_with_skips(input_term_arr)
            and_op_no_skip_sorted = self._sort_with_tfidf(result_posting_list)
            and_op_skip_sorted = self._sort_with_tfidf(result_posting_list_skips)
            and_comparisons_no_skip_sorted = and_comparisons_no_skip
            and_comparisons_skip_sorted = and_comparisons_skip

            and_op_no_score_no_skip, and_results_cnt_no_skip = self._output_formatter(and_op_no_skip)
            and_op_no_score_skip, and_results_cnt_skip = self._output_formatter(and_op_skip)
            and_op_no_score_no_skip_sorted, and_results_cnt_no_skip_sorted = self._output_formatter(and_op_no_skip_sorted)
            and_op_no_score_skip_sorted, and_results_cnt_skip_sorted = self._output_formatter(and_op_skip_sorted)

            output_dict['daatAnd'][query.strip()] = {}
            output_dict['daatAnd'][query.strip()]['results'] = and_op_no_score_no_skip
            output_dict['daatAnd'][query.strip()]['num_docs'] = and_results_cnt_no_skip
            output_dict['daatAnd'][query.strip()]['num_comparisons'] = and_comparisons_no_skip

            output_dict['daatAndSkip'][query.strip()] = {}
            output_dict['daatAndSkip'][query.strip()]['results'] = and_op_no_score_skip
            output_dict['daatAndSkip'][query.strip()]['num_docs'] = and_results_cnt_skip
            output_dict['daatAndSkip'][query.strip()]['num_comparisons'] = and_comparisons_skip

            output_dict['daatAndTfIdf'][query.strip()] = {}
            output_dict['daatAndTfIdf'][query.strip()]['results'] = and_op_no_score_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_docs'] = and_results_cnt_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_no_skip_sorted

            output_dict['daatAndSkipTfIdf'][query.strip()] = {}
            output_dict['daatAndSkipTfIdf'][query.strip()]['results'] = and_op_no_score_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_docs'] = and_results_cnt_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_skip_sorted

        return output_dict


@app.route("/execute_query", methods=['POST'])
def execute_query():
    """ This function handles the POST request to your endpoint.
        Do NOT change it."""
    start_time = time.time()

    queries = request.json["queries"]
    random_command = request.json["random_command"]

    """ Running the queries against the pre-loaded index. """
    output_dict = runner.run_queries(queries, random_command)

    """ Dumping the results to a JSON file. """
    with open(output_location, 'w') as fp:
        json.dump(output_dict, fp)

    response = {
        "Response": output_dict,
        "time_taken": str(time.time() - start_time),
        "username_hash": username_hash
    }
    return flask.jsonify(response)


if __name__ == "__main__":
    """ Driver code for the project, which defines the global variables.
        Do NOT change it."""

    output_location = "project2_output.json"
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--corpus", type=str, help="Corpus File name, with path.")
    parser.add_argument("--output_location", type=str, help="Output file name.", default=output_location)
    parser.add_argument("--username", type=str,
                        help="Your UB username. It's the part of your UB email id before the @buffalo.edu. "
                             "DO NOT pass incorrect value here")

    argv = parser.parse_args()

    corpus = argv.corpus
    output_location = argv.output_location
    username_hash = hashlib.md5(argv.username.encode()).hexdigest()

    """ Initialize the project runner"""
    runner = ProjectRunner()

    """ Index the documents from beforehand. When the API endpoint is hit, queries are run against 
        this pre-loaded in memory index. """
    runner.run_indexer(corpus)

    app.run(host="0.0.0.0", port=9999)
