'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import math


class Node:

    def __init__(self, value=None, next=None):
        """ Class to define the structure of each node in a linked list (postings list).
            Value: document id, Next: Pointer to the next node
            Add more parameters if needed.
            Hint: You may want to define skip pointers & appropriate score calculation here"""
        self.value = value
        self.next = next
        self.skip_link = None
        self.tf = 0
        self.tf_idf = 0


class LinkedList:
    """ Class to define a linked list (postings list). Each element in the linked list is of the type 'Node'
        Each term in the inverted index has an associated linked list object.
        Feel free to add additional functions to this class."""
    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.length, self.n_skips, self.idf = 0, 0, 0.0
        self.skip_length = None

    def traverse_list(self):
        traversal = []
        if self.start_node is None:
            return
        else:
            n = self.start_node
            # Start traversal from head, and go on till you reach None
            while n is not None:
                traversal.append(n.value)
                n = n.next
            return traversal
            

    def traverse_skips(self):
        traversal = []
        if self.start_node is None:
            return
        else:
            n = self.start_node
            # Start traversal from head, and go on till you reach None
            while n is not None:
                traversal.append(n.value)
                n = n.skip_link
            return traversal

    def add_skip_connections(self):
        """ Write logic to add skip pointers to the linked list. 
            This function does not return anything.
            To be implemented."""
        n_skips = math.floor(math.sqrt(self.length))
        if n_skips * n_skips == self.length:
            n_skips = n_skips - 1
        self.n_skips = n_skips
        self.skip_length = round(math.sqrt(self.length),0)
        
        if self.skip_length > 1:
            n = self.start_node
            m = self.start_node
            counter = 0
            while n is not None:

                if((counter % self.skip_length) == 0):
                    m = n
                    for i in range(int(self.skip_length)):
                        if(m is not None):
                            m = m.next
                        else:
                            return
                    n.skip_link = m
                else:
                    n.skip_link = None
                counter += 1
                n = n.next
                

    def insert_at_end(self, value, num_tokens_in_doc, idf):
        new_node = Node(value=value)
        new_node.tf = (1/num_tokens_in_doc)
        new_node.tf_idf = idf
        n = self.start_node

        if self.start_node is None:
            self.start_node = new_node
            self.end_node = new_node
            self.length += 1
            return

        elif self.start_node.value >= value:
            self.start_node = new_node
            self.start_node.next = n
            self.length += 1
            return

        elif self.end_node.value <= value:
            self.end_node.next = new_node
            self.end_node = new_node
            self.length += 1
            return

        else:
            while n.value < value < self.end_node.value and n.next is not None:
                n = n.next

            m = self.start_node
            while m.next != n and m.next is not None:
                m = m.next
            m.next = new_node
            new_node.next = n
            self.length += 1
            return

    def add_tf_idf_score(self, idf):
        if self.start_node is None:
            return
        else:
            n = self.start_node
            # Start traversal from head, and go on till you reach None
            while n is not None:
                n.tf_idf = n.tf * idf
                n = n.next
            return

    def is_not_duplicate(self, docId, num_tokens_in_doc):
        if self.start_node is None:
            return True
        else:
            n = self.start_node
            # Start traversal from head, and go on till you reach None
            while n is not None:
                if(n.value != docId):
                    n = n.next
                else :
                    n.tf = n.tf + (1/num_tokens_in_doc)
                    return False
        return True


    def dummy_traverse_list(self):
        traversal = []
        if self.start_node is None:
            return
        else:
            n = self.start_node
            # Start traversal from head, and go on till you reach None
            while n is not None:
                traversal.append((n.value, n.tf_idf))
                n = n.next
            return traversal