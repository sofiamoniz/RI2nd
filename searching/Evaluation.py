"""
IR, November 2020
Assignment 2: Ranked Retrieval
Autors: Alina Yanchuk, 89093
        Ana Sofia Fernandes, 88739
"""

import statistics
import math

class Evaluation:
    def __init__(self, relevances, scores):
        self.relevances = relevances  # {query_1 : {doc_1 : relevance, doc_2: relevance,...},...} 
        self.scores = scores  # {query_1 : {doc_1 : score , doc_2: score,...},...} 

        self.queries_precision = {}
        self.queries_recall = {}
        self.queries_average_precision = {}
        self.dcg_dic = self.dcg()
        self.ndcg_dic = {}


    def mean_precision_recall(self):

        for query_id in self.scores:
        
            tp_fn = 0
            tp_fp = 0
            tp = 0
            total_precision = 0

            for doc,relevance in self.relevances[query_id].items():
                if (doc in self.scores[query_id]) and relevance>0:
                    tp += 1
                if relevance > 0:
                    tp_fn += 1

            tp_fp = len(self.scores[query_id])
                        
            self.queries_precision[query_id] = (tp/tp_fp)
            if tp_fn!=0:
                self.queries_recall[query_id] = (tp/tp_fn)
            
        #print(self.queries_precision)
        #print(self.queries_recall)
        mean_precision = statistics.mean(list(self.queries_precision.values()))
        mean_recall = statistics.mean(list(self.queries_recall.values()))
      
        print("Mean Precision -> ", mean_precision) #Mais tarde escrevê-los num ficheiro e fazer só a média
        print("Mean Recall ->  ", mean_recall)



    def mean_f1(self):

        queries_f1 = {}

        for query_id in self.queries_precision:
            if self.queries_precision[query_id] != 0 and self.queries_recall != 0 :
                queries_f1[query_id] = 2 * ((self.queries_precision[query_id]*self.queries_recall[query_id])
                                                     /(self.queries_precision[query_id]+self.queries_recall[query_id])) 
            else:
                queries_f1[query_id] = 0

        #print(queries_f1)
        mean_f1 = statistics.mean(list(queries_f1.values()))

        print("Mean F-Measure -> ", mean_f1)



    def average_precision(self):

        for query_id in self.scores:

            tp_fn = 0
            tp_fp = 0
            tp = 0
            precisions = []
            average_precision = 0

            for doc,relevance in self.relevances[query_id].items():
                if relevance > 0:
                    tp_fn += 1

            for doc,score in self.scores[query_id].items():
                relevant = False
                tp_fp += 1
                if doc in self.relevances[query_id] and self.relevances[query_id][doc]>0:
                    relevant = True
                    tp += 1
                precision = tp/tp_fp
                if tp_fn!=0:
                    recall = tp/tp_fn
                
                if relevant==True: precisions.append(precision)

            if len(precisions)!=0:
                average_precision = statistics.mean(precisions)
            else:
                average_precision = 0

            self.queries_average_precision[query_id] = average_precision

        #print(self.queries_average_precision)



    def mean_average_precision(self): #MAP

        self.average_precision()

        mean_average_precision = statistics.mean(list(self.queries_average_precision.values()))
        
        print("MAP -> "+str(mean_average_precision))



    def dcg(self):
        query_dcg = {}
        for query_id in self.relevances:            
            count=0
            for doc,relevance in self.relevances[query_id].items():       
                count+=1
                if query_id not in query_dcg.keys():
                    query_dcg[query_id] = relevance/math.log2(count+1)
                else:
                    query_dcg[query_id] += relevance/math.log2(count+1)
        return query_dcg


    def mean_ndcg(self):
        query_ndcg = {}
        relevances_ordered = {}
        for query_id in self.relevances: 
            count=0
            for doc,relevance in self.relevances[query_id].items():
                relevances_ordered[query_id] = {k: v for k, v in sorted(self.relevances[query_id].items(), key=lambda item: item[1], reverse=True)}
            
            for doc,relevance in relevances_ordered[query_id].items():
                count+=1
                if query_id not in query_ndcg.keys():
                    query_ndcg[query_id] = relevance/math.log2(count+1)
                else:
                    query_ndcg[query_id] += relevance/math.log2(count+1)

        for query_id in self.dcg_dic:
            for query_id in query_ndcg:
                if query_ndcg[query_id] != 0:
                    self.ndcg_dic[query_id] = self.dcg_dic[query_id]/query_ndcg[query_id]
                else:
                    self.ndcg_dic[query_id] = 0
        
        mean_ndgc = statistics.mean(list(self.ndcg_dic.values()))
        
        print("Mean NDGC -> "+str(mean_ndgc))



    def query_throughput(self):
        pass



    def mean_latency(self,queries_latency):

        #print(queries_latency)
        median_latency = statistics.median(list(queries_latency.values()))

        print("Median of Queries Latency -> "+str(median_latency)+ " seconds")




