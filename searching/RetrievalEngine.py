"""
IR, November 2020
Assignment 2: Ranked Retrieval
Autors: Alina Yanchuk, 89093
        Ana Sofia Fernandes, 88739
"""

import time
import os
import psutil
import json
from searching.Ranking import Ranking

## Class that acts as a pipeline for the all searching and retrieval process ( calls all the other classes and methods  )
class RetrievalEngine:

    def __init__(self,tokenizer,ranking_type,index_file,query_file):
        self.tokenizer=tokenizer
        self.ranking_type=ranking_type
        self.index_file=index_file
        self.query_file=query_file

        self.weighted_index={}
        self.queries=[]
        self.real_doc_ids={}


    def query_search(self):


        """
        Search the query terms and prints the retrieved ordered documents, based on the ranking type choosen 

        Follows this pipeline:

                Loads the queries, weighted index and document id's, from the files provided    
                    |
                Weights the queries   ( only if using lnc.ltc ! )
                    |         
                Computes the scores   ( for each document that answers the query ) 
                    |             
                Retrieve the ranked documents
        """

        self.read_index_file() 
        self.read_queries_file()
        self.read_doc_ids_file()

        ranking = Ranking(self.tokenizer,self.queries,self.weighted_index)
        
        if self.ranking_type=="lnc.ltc":
            ranking.weight_queries_lnc_ltc() # this step is only for lnc.ltc
            ranking.score_lnc_ltc()
        
        else:
            ranking.score_bm25() # no need to weight the queries

    
        # Print results:
        for i in range(0,len(self.queries)):
            print("\n -> Query: "+self.queries[i]+"\n")
            print("Ranked Documents Retrieved: \n")
            j=0 # Só para retornar apenas 10 docs
            for doc,score in ranking.scores[i].items():
                if j==10: break
                else: 
                    print("Document: "+self.real_doc_ids[doc]+"                  Score: "+str(score))
                    j=j+1
           



 ## AUXILIAR FUNCTIONS:


    def read_index_file(self):

        """
        Reads the file with the Weighted Index to self.weighted_index
        """

        file = open(self.index_file, 'r') 
        for line in file:
            tokens=line.rstrip().split(';') 
            term=tokens[0]
            idf=float(tokens[1])
            tokens[2]=tokens[2].replace('\'','\"')
            docsWeights=json.loads(tokens[2])

            self.weighted_index[term]=[idf,docsWeights]  # self.weighted_index = { "term" : [ idf, {"doc1":weight_of_term_in_doc1,"doc2":weight_of_term_in_doc2,...}],...  }
        file.close()
    


    def read_queries_file(self):

        """
        Reads the file with the Queries to self.queries
        """

        file = open(self.query_file, 'r') 
        for line in file: 
            self.queries.append(line.rstrip())   # self.queries = [ query1, query2, query3,...]
        file.close()



    def read_doc_ids_file(self):

        """
        Reads the file with the document id's mapping to self.real_doc_ids
        """

        with open('results/documentIDs.txt') as file_ids:
            self.real_doc_ids = json.load(file_ids)   # self.real_doc_ids = { doc1_generated Id_ : doc1_real_Id, ... }

