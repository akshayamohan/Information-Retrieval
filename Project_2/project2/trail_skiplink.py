from linkedlist import LinkedList
from indexer import Indexer

tokenized_document1 = ['evalu']

indexer = Indexer()


arr = [1114, 3179, 5243, 18078, 21142, 22937, 25980, 27939, 31534, 33542, 37975, 40820, 51642, 
70142, 74801, 76667, 76945, 87341, 93031, 96926, 101255, 103373, 104256, 107254, 114225, 116827, 120813, 132286, 141156, 145184, 145213, 
146416, 149990, 152124, 153319]

[1114, 3179, 5243, 18078, 21142, 22937, 25980, 27939, 31534, 33542, 37975, 40820, 51642, 
70142, 74801, 76667, 76945, 87341, 93031, 96926, 101255, 103373, 104256, 107254, 114225, 116827, 120813, 132286, 141156, 145184, 145213, 
146416, 149990, 152124, 153319]

for i in range(len(arr)):
	indexer.generate_inverted_index(arr[i], tokenized_document1)

index = indexer.get_index()
posting_list = index.get('evalu')
print(posting_list.add_skip_connections())
print(posting_list.length)
print(posting_list.traverse_list())
print(posting_list.traverse_skips())