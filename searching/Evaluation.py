"""
IR, November 2020
Assignment 2: Ranked Retrieval
Authors: Alina Yanchuk, 89093
        Ana Sofia Fernandes, 88739
"""

import statistics
import collections
import math

## Class to calculates the metrics asked in the last exercice of the Assignment 2
class Evaluation:
    def __init__(self, relevances, scores):
        self.relevances = relevances  # { query1_id : { doc_1: relevance, doc_2: relevance,...},...} 
        self.scores = scores  # { query1_id : {doc_1 : score , doc_2: score,...},...} 

        self.returned_relevances = collections.defaultdict(dict)
        self.queries_precision = {}
        self.queries_recall = {}
        self.queries_average_precision = {}
        self.queries_dcg = collections.defaultdict(int)
        self.queries_ndcg = {}


    def mean_precision_recall(self):

        """
        Calculates the mean precision and mean recall 
        """

        for query_id in self.scores:
        
            tp_fn = 0
            tp_fp = 0
            tp = 0
            total_precision = 0

            for doc,relevance in self.relevances[query_id].items():
                if (doc in self.scores[query_id]) and relevance>0: #if the doc exists in our scores and has relevance
                    tp += 1 # We found a true positive
                if relevance > 0: # if the doc has relevance but doesn't exist in our scores
                    tp_fn += 1 # We found a true_positive-false_negative

            tp_fp = len(self.scores[query_id]) # All the relevant docs correspond to the len of our dictionary self.scores
                        
            self.queries_precision[query_id] = (tp/tp_fp) # Calculates the precision for each query
            if tp_fn!=0: # If true_positive-false_negative exist, we calculate the recall for each query
                self.queries_recall[query_id] = (tp/tp_fn)

        mean_precision = statistics.mean(list(self.queries_precision.values())) # he mean precision is the mean of all values
                                                                                # Of the precision dict
        mean_recall = statistics.mean(list(self.queries_recall.values())) # The mean recall is the mean of all values
                                                                                # Of the recall dict
      
        print("Mean Precision -> ", mean_precision)
        print("Mean Recall ->  ", mean_recall)



    def mean_f1(self):

        """
        Calculates the mean f-measure
        """

        queries_f1 = {}

        for query_id in self.queries_precision:
            if self.queries_precision[query_id] != 0 and self.queries_recall != 0 : # if both precision and recall have a value
                queries_f1[query_id] = 2 * ((self.queries_precision[query_id]*self.queries_recall[query_id])
                                                     /(self.queries_precision[query_id]+self.queries_recall[query_id])) # f1 calculation
            else: # If precision or recall is 0
                queries_f1[query_id] = 0

        mean_f1 = statistics.mean(list(queries_f1.values())) # The mean f1 is the mean of all values
                                                            # Of the f1 dict

        print("Mean F-Measure -> ", mean_f1)



    def average_precision(self):

        """
        Calculates the average precision
        """

        for query_id in self.scores:

            tp_fn = 0
            tp_fp = 0
            tp = 0
            precisions = []
            average_precision = 0

            for doc,relevance in self.relevances[query_id].items():
                if relevance > 0: #if the doc has relevance but doesn't exist in our scores
                    tp_fn += 1 #We found a true_positive-false_negative

            for doc,score in self.scores[query_id].items():
                relevant = False
                tp_fp += 1
                if doc in self.relevances[query_id] and self.relevances[query_id][doc]>0:
                    relevant = True #If the doc exists in our scores and in the relevances (having relevance>1), it means that
                                    #A relevant doc was found
                    tp += 1
                precision = tp/tp_fp #Calculates the precision for each query
                
                if relevant==True: precisions.append(precision) #Saves the precisions in order to calculate the average mean

            if len(precisions)!=0:
                average_precision = statistics.mean(precisions) #Calculates the mean of the precisions
            else:
                average_precision = 0

            self.queries_average_precision[query_id] = average_precision #Calculates the average mean for each query




    def mean_average_precision(self): 

        """
        Calculates the mean average precision (MAP)
        """

        self.average_precision()

        #The MAP value is the mean of all average precision values, calculated previously
        mean_average_precision = statistics.mean(list(self.queries_average_precision.values()))
        
        print("MAP -> "+str(mean_average_precision))



    def get_returned_relevances(self):

        """
        Saves the relevances of the documents returned by the Retrieval Engine and found on the relevances file, for each query
        """

        for query_id in self.relevances:
            for doc,relevance in self.relevances[query_id].items():
                if doc in self.scores[query_id]: # If the document exists in our scores (was retrieved), we will save its relevance
                    query_relevance=self.returned_relevances[query_id]
                    query_relevance[doc]=relevance
                    self.returned_relevances[query_id] = query_relevance




    def dcg(self):

        """
        Calculates the discounted cumulative gain (dcg)
        """

        self.get_returned_relevances()

        for query_id in self.returned_relevances:            
            count=0
            for doc,relevance in self.returned_relevances[query_id].items():       
                count+=1 # Count is used as the indice for each document
                self.queries_dcg[query_id] += relevance/math.log2(count+1) # dcg formula



    def mean_ndcg(self):

        """
        Calculates the mean normalized DCG (NDCG)
        """

        self.dcg()

        ideal_dcg = collections.defaultdict(int)
        relevances_ordered = {}
        for query_id in self.returned_relevances: 
            count=0
            # This time, we will order the relevant docs for each query, in decreasing order
            # Ex: query_1 : {doc1: 2, doc2:1, doc3:1 , doc4:0}
            # So that we can have the ideal elements.
            # Then, by normalizing the dcg with these values, we achive normalized DCG
            relevances_ordered[query_id] = {k: v for k, v in sorted(self.returned_relevances[query_id].items(), key=lambda item: item[1], reverse=True)}
            
            for doc,relevance in relevances_ordered[query_id].items():
                count+=1 #Count is used as the indice for each document
                ideal_dcg[query_id] += relevance/math.log2(count+1)

        for query_id in self.queries_dcg: 
            if ideal_dcg[query_id] != 0:
                self.queries_ndcg[query_id] = self.queries_dcg[query_id]/ideal_dcg[query_id] # The NDCG is found by dividing the
                                                                                             # DCG values by corresponding ideal values
            else:
                self.queries_ndcg[query_id] = 0
        
        #print(self.queries_ndcg)
        mean_ndgc = statistics.mean(list(self.queries_ndcg.values()))
        
        print("Mean NDGC -> "+str(mean_ndgc))



    def query_throughput(self,total_queries_processing,ranking_type):

        """
        Calculates the query throughput
        """

        if ranking_type=="bm25": total_number_of_queries = len(list(self.scores.keys()))
        else: total_number_of_queries = 2*len(list(self.scores.keys()))

        qt = total_number_of_queries / total_queries_processing
        
        print("Query throughput -> "+str(round(qt))+ " queries per second")



    def mean_latency(self,queries_latency):

        """
        Calculates the mean latency
        """

        #print(queries_latency)
        median_latency = statistics.median(list(queries_latency.values())) # Calculates the median of all query latency values,
                                                                           # Previously calculated at Ranking.py

        print("Median of Queries Latency -> "+str(median_latency)+ " seconds")