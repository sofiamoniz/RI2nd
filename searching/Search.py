"""
IR, October 2020
Assignment 1: Indexing documents
Autors: Alina Yanchuk, 89093
        Ana Sofia Fernandes, 88739
"""


import time
import os
import psutil
import json
from searching.QueryProcessing import QueryProcessing

## Class that 
class Search:

    def __init__(self,tokenizer,index_file,query_file):
        self.tokenizer=tokenizer
        self.index_file=index_file
        self.query_file=query_file

        self.weighted_index={}
        self.weighted_queries={}

        self.queries=[]
        self.retrieved_documents=[]



    def query_search(self):

        self.weighted_index=self.read_index_file()

        queryProcessing = QueryProcessing(self.tokenizer,self.query_file,self.weighted_index)
        self.queries=queryProcessing.read_content()  # Array with queries from file
        self.weighted_queries=queryProcessing.queries_weights()   # Calculates the query weights 



        # Print results:
        for i in range(0,len(self.queries)):
            print("\n -> Query: "+self.queries[i]
                  +"\n    Retrieved ordered documents: "+self.retrieved_documents[i]+"\n")




    def read_index_file(self):
        with open(self.index_file) as file:
            self.weighted_index = json.load(file) 




     

"""
  
        


        # Print results:
        if(self.tokenizer_type=="s"):
            print("\n    Tokenizer used: Simple \n"
                    +"\n--- Number of documents:  %s documents." % (total_docs) 
                    +"\n--- Total number of terms (vocabulary size): %d terms." % (total_terms)
                    +"\n--- Indexation time:  %s seconds." % (round(indexing_time,3))
                    +"\n--- Size in memory used by the dictionary structure:  %s %s." % (round(memory_dic[0],3), memory_dic[1])
                    +"\n--- Memory required by the program:  %s %s." % (round(memory_used[0],3), memory_used[1])
                    + "\n--- Directory with the Inverted Index: results/simpleTokenizer"
                    + "\n--- Directory that contains the real document Id's and auto generated ones: results\n")
        else:
            print("\n    Tokenizer used: Improved \n"
                    +"\n--- Number of documents:  %s documents." % (total_docs) 
                    +"\n--- Total number of terms (vocabulary size): %d terms." % (total_terms)
                    +"\n--- Indexation time:  %s seconds." % (round(indexing_time,3))
                    +"\n--- Size in memory used by the dictionary structure:  %s %s." % (round(memory_dic[0],3), memory_dic[1])
                    +"\n--- Memory required by the program:  %s %s." % (round(memory_used[0],3), memory_used[1])
                    + "\n--- Directory with the Inverted Index: results/improvedTokenizer"
                    + "\n--- Directory that contains the real document Id's and auto generated ones: results\n")
        print("\nAnswers to 4. c) and d) :")
        print("\nTop 10 terms with frequency 1: "+str(results.terms_doc_frequency_1()))
        print("\nTop 10 terms with highest frequency: "+str(results.terms_highest_doc_frequency()))



"""