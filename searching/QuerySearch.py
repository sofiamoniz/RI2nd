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
class QuerySearch:

    def __init__(self,tokenizer,ranking,index_file,query_file):
        self.tokenizer=tokenizer
        self.ranking=ranking
        self.index_file=index_file
        self.query_file=query_file

        self.weighted_index={}
        self.weighted_queries={}

        self.queries=[]

        self.real_doc_ids={}




    def query_search(self):

        self.read_index_file()
        self.read_queries_file()
        self.read_doc_ids_file()

        queryProcessing = QueryProcessing(self.tokenizer,self.ranking,self.queries,self.weighted_index)
        
        if self.ranking=="lnc.ltc":
            queryProcessing.weight_queries_lnc_ltc()
            queryProcessing.score_lnc_ltc()
        
        else:
            queryProcessing.score_bm25()


            # Results:

        for i in range(0,len(self.queries)):
            print("\n -> Query: "+self.queries[i]+"\n")
            print("10 Top Ranked Documents: \n")
            j=0 # Só para retornar apenas 10 docs
            for doc,score in queryProcessing.scores[i].items():
                if j==10: break
                else: 
                    print("Document: "+self.real_doc_ids[doc]+"                  Score: "+str(score))
                    j=j+1

        
        
        



    def read_index_file(self):
        file = open(self.index_file, 'r') 
        for line in file:
            tokens=line.rstrip().split(';') 
            term=tokens[0]
            idf=float(tokens[1])
            tokens[2]=tokens[2].replace('\'','\"')
            docsWeights=json.loads(tokens[2])
            self.weighted_index[term]=[idf,docsWeights]
        file.close()
    
    def read_queries_file(self):
        file = open(self.query_file, 'r') 
        for line in file: 
            self.queries.append(line.rstrip())
        file.close()

    def read_doc_ids_file(self):
        with open('results/documentIDs.txt') as file_ids:
            self.real_doc_ids = json.load(file_ids)



     

"""
  
        

        # Print results:
        for i in range(0,len(self.queries)):
            print("\n -> Query: "+self.queries[i]
                  +"\n    Retrieved ordered documents: "+self.retrieved_documents[i]+"\n")



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