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
from searching.Evaluation import Evaluation

## Class that acts as a pipeline for the all searching and retrieval process ( calls all the other classes and methods  )
class RetrievalEngine:

    def __init__(self,tokenizer,ranking_type,index_file,query_file,relevances_file,number_of_docs_to_return):
        self.tokenizer=tokenizer
        self.ranking_type=ranking_type
        self.index_file=index_file
        self.query_file=query_file
        self.relevances_file=relevances_file
        self.top=number_of_docs_to_return # for each query

        self.weighted_index=self.read_index_file()
        self.queries=self.read_queries_file()
        self.real_doc_ids=self.read_doc_ids_file()
        self.relevances=self.read_relevances_file()


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

        ranking = Ranking(self.tokenizer,self.queries,self.weighted_index)
        
        start_queries_processing = time.time()
        if self.ranking_type=="lnc.ltc":
            ranking.weight_queries_lnc_ltc() # this step is only for lnc.ltc
            ranking.score_lnc_ltc()
        
        else:
            ranking.score_bm25() # no need to weight the queries

        queries_processing = time.time() - start_queries_processing
        queries_latency = ranking.get_queries_latency()

        # Write TOP N results to file and create dic with N scores for evaluation:
        scores_for_evaluation = {}
        with open("results/ranking_"+self.ranking_type+".txt", 'w') as file_ranking:
            file_ranking.write("***  TOP "+self.top+" RETURNED DOCUMENTS *** ")
            file_ranking.write("\n\nRanking: "+self.ranking_type)
            file_ranking.write("\nIndex file: "+self.index_file)
            file_ranking.write("\nTokenizer: "+"Improved\n" if self.tokenizer=='i' else "Simple\n")
            for i in range(0,len(self.queries)):
                file_ranking.write("\n\n -> Query: "+self.queries[i]+"\n")
                file_ranking.write("\nQuery latency: " + str(queries_latency[i+1])+" seconds\n")
                number_of_docs_returned=0 # TOP self.top
                docs_scores={}
                for doc,score in ranking.scores[i].items():
                    if number_of_docs_returned==int(self.top): break
                    else:
                        docs_scores[self.real_doc_ids[doc]]=score 
                        file_ranking.write("\nDocument: "+self.real_doc_ids[doc]+"                  Score: "+str(score))
                        number_of_docs_returned=number_of_docs_returned+1
                scores_for_evaluation[str(i+1)]=docs_scores

        
        print("\nResults of Ranking in: "+"results/ranking_"+self.ranking_type+".txt\n")



        ## EVALUATION of results:

        print("Evaluation TOP "+self.top+" :\n")

        evaluation = Evaluation(self.relevances,scores_for_evaluation)
        
        evaluation.mean_precision_recall()
        evaluation.mean_f1()
        evaluation.mean_average_precision()
        evaluation.mean_ndcg()
        evaluation.query_throughput(queries_processing)
        evaluation.mean_latency(queries_latency)
        print("\n")

 ## AUXILIAR FUNCTIONS:


    def read_index_file(self):

        """
        Reads the file with the Weighted Index to dictionary
        """
        weighted_index={}
        file = open(self.index_file, 'r') 
        for line in file:
            tokens=line.rstrip().split(';') 
            term=tokens[0]
            idf=float(tokens[1])
            tokens[2]=tokens[2].replace('\'','\"')
            docsWeights=json.loads(tokens[2])

            weighted_index[term]=[idf,docsWeights]  # weighted_index = { "term" : [ idf, {"doc1":weight_of_term_in_doc1,"doc2":weight_of_term_in_doc2,...}],...  }
        file.close()

        return weighted_index
    


    def read_queries_file(self):

        """
        Reads the file with the Queries to array
        """

        queries=[]
        file = open(self.query_file, 'r') 
        for line in file: 
            queries.append(line.rstrip())   # queries = [ query1, query2, query3,...]
        file.close()

        return queries



    def read_doc_ids_file(self):

        """
        Reads the file with the document id's mapping to dictionary
        """
        real_doc_ids={}
        with open('results/documentIDs.txt') as file_ids:
            real_doc_ids = json.load(file_ids)   # real_doc_ids = { doc1_generated Id_ : doc1_real_Id, ... }
        
        return real_doc_ids


    def read_relevances_file(self):

        relevances={}
        with open (self.relevances_file, mode='r') as file_to_read:
            for row in file_to_read:
                query_id = row.split()[0]
                cord_ui = row.split()[1]
                content = float(row.split()[2])
                if query_id not in relevances.keys():
                    doc_scores = {}
                    doc_scores[cord_ui]=content
                    relevances[query_id] = doc_scores
                else:
                    doc_scores=relevances[query_id]
                    doc_scores[cord_ui]=content
                    relevances[query_id] = doc_scores
        
        return relevances

