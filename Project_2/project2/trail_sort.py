from linkedlist import LinkedList
from indexer import Indexer
from run_project import ProjectRunner



def _sort_with_tfidf(posting_list):

    sorted_output = []
    list_values = posting_list.dummy_traverse_list()
    list_values.sort(key = lambda x: x[1], reverse=True)
    for i in range(len(list_values)):
        sorted_output.append(list_values[i][0])
    return sorted_output

    # return sorted_list


def Sort_Tuple(tup): 

    tup.sort(key = lambda x: x[1], reverse=True) 
    return tup 
  
# Driver Code 
# tup = [('rishav', 10), ('akash', 5), ('ram', 20), ('gaurav', 15)] 
  
# printing the sorted list of tuples



linked_list = LinkedList()
linked_list.insert_at_end(20,1, 0.7)
linked_list.insert_at_end(21,1, 0.01)
linked_list.insert_at_end(18,1, 0.3)
linked_list.insert_at_end(23,1, 1.0)
linked_list.insert_at_end(3,1, 0.003)
linked_list.insert_at_end(9,1, 0.9)

# list_values = linked_list.dummy_traverse_list()
# print(Sort_Tuple(list_values))

print(_sort_with_tfidf(linked_list))


# list_values = linked_list.dummy_traverse_list()
# print(list_values)
# _sort_with_tfidf(linked_list)
# list_values = linked_list.dummy_traverse_list()
# print(list_values)
# print(_sort_with_tfidf(linked_list))


def traverse_skips(self):
    traversal = []
    if self.start_node is None:
        return
    else:
        n = self.start_node
        # Start traversal from head, and go on till you reach None
        while n.skip_link is not None:
            traversal.append(n.value)
            n = n.skip_link
        return traversal
