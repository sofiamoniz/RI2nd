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
        Search the query terms and returns the retrieved ordered documents, based on the ranking type choosen. Writes results to files.

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
        query_latency = ranking.get_query_latency()
        
        if self.ranking_type=="lnc.ltc":
            ranking.weight_queries_lnc_ltc() # this step is only for lnc.ltc
            ranking.score_lnc_ltc()
        
        else:
            ranking.score_bm25() # no need to weight the queries

    
        # Write results to file:
        with open("results/ranking_"+self.ranking_type+".txt", 'w') as file_ranking:
            file_ranking.write("***  TOP 10 RETURNED DOCUMENTS *** ")
            file_ranking.write("\n\nRanking: "+self.ranking_type)
            file_ranking.write("\nIndex file: "+self.index_file)
            file_ranking.write("\nQuery latency: "+self.query_file)
            file_ranking.write("\nTokenizer: "+"Improved\n" if self.tokenizer=='i' else "Simple\n")
            for i in range(0,len(self.queries)):
                file_ranking.write("\n\n -> Query: "+self.queries[i]+"\n")
                file_ranking.write("\nQuery latency: " + str(query_latency[self.queries[i]])+"\n")
                number_of_docs_returned=0 # TOP 10
                for doc,score in ranking.scores[i].items():
                    if number_of_docs_returned==10: break
                    else: 
                        file_ranking.write("\nDocument: "+self.real_doc_ids[doc]+"                  Score: "+str(score))
                        number_of_docs_returned=number_of_docs_returned+1

        
        print("Results of Ranking in: "+"results/ranking_"+self.ranking_type+".txt")



        # Write results to file to use in evaluation:
        with open("searching/ranking_for_evaluation_"+self.ranking_type+".txt", 'w') as file_ranking:
            query_id = 0
            for i in range(0,len(self.queries)):
                number_of_docs_returned=0 
                query_id+=1
                for doc,score in ranking.scores[i].items():
                    if number_of_docs_returned==10: break
                    else: 
                        file_ranking.write(str(query_id)+"    "+self.real_doc_ids[doc]+"    "+str(score)+"\n")  # query - doc - score
                        number_of_docs_returned=number_of_docs_returned+1
                        
           

        

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

