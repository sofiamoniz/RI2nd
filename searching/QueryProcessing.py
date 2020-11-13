"""
IR, October 2020
Assignment 1: Indexing documents
Autors: Alina Yanchuk, 89093
        Ana Sofia Fernandes, 88739
"""

from documentIndexer.ImprovedTokenizer import ImprovedTokenizer
from documentIndexer.SimpleTokenizer import SimpleTokenizer
import math

## Class that

class QueryProcessing:

    def __init__(self,tokenizer,file_name,weighted_index):
        self.file_name = file_name;
        self.weighted_index=weighted_index;

        self.queries=[];
        self.weighted_queries=[]



    def read_content(self):

        file = open(file_name, 'r') 

        for line in file: 
            self.queries.append(line)

        file.close()

        return self.queries



    def weighted_queries(self):

        weighted_query=defaultdict(int)


        for query in self.queries:

            if self.tokenizer=='-s':
                simpleTokenizer=SimpleTokenizer()
                query_terms=simpleTokenizer.simple_tokenizer(query)
            else:
                improvedTokenizer=ImprovedTokenizer()
                query_terms=improvedTokenizer.improved_tokenizer(query)

            for term in query_terms:
                weighted_query[term]=weighted_query[term]+1
            
            for term in weighted_query:
                if term in self.weighted_index.keys():
                    weighted_query[term]=(1+math.log10(weighted_query[term]) * self.weighted_index[term][0])
                else:
                    weighted_query[term]=0
            
            self.weighted_queries.append(weighted_query)
        
     


