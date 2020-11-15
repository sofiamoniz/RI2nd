"""
IR, October 2020
Assignment 1: Indexing documents
Autors: Alina Yanchuk, 89093
        Ana Sofia Fernandes, 88739
"""

from indexing.ImprovedTokenizer import ImprovedTokenizer
from indexing.SimpleTokenizer import SimpleTokenizer
import math
import collections

## Class that

class QueryProcessing:

    def __init__(self,tokenizer,ranking,queries,weighted_index):
        self.tokenizer=tokenizer
        self.ranking=ranking
        self.weighted_index=weighted_index
        self.queries=queries

        self.weighted_queries=[]
        self.scores=[]




    def weight_queries_lnc_ltc(self):

        for query in self.queries:

            temp=0
            query_length=0
            weighted_query={}

            if self.tokenizer=='s':
                simpleTokenizer=SimpleTokenizer()
                query_terms=simpleTokenizer.simple_tokenizer(query)
            else:
                improvedTokenizer=ImprovedTokenizer()
                query_terms=improvedTokenizer.improved_tokenizer(query)
            for term in query_terms:
                if term in weighted_query:
                    weighted_query[term]=weighted_query[term]+1
                else:
                    weighted_query[term]=1  
            for term in weighted_query:
                if term in self.weighted_index.keys():     
                    weighted_query[term]=(1+math.log10(weighted_query[term])) * self.weighted_index[term][0]        
                else:
                    weighted_query[term]=0
            for term,value in weighted_query.items():
                temp=temp+(math.pow(value,2))
                

            query_length=(math.sqrt(temp))

            for term,value in weighted_query.items():
                weighted_query[term]=value/query_length

            self.weighted_queries.append(weighted_query)
           
                
     

    def score_lnc_ltc(self):
        
        for i in range(0,len(self.queries)):
            query_score={}
            
            for term,query_weight in self.weighted_queries[i].items():  # each query
                if term in self.weighted_index:
                    for doc_id,doc_weight in self.weighted_index[term][1].items():
                        if doc_id in query_score:
                            query_score[doc_id]=query_score[doc_id]+(query_weight*doc_weight)
                        else:
                            query_score[doc_id]=query_weight*doc_weight

            query_score={k: v for k, v in sorted(query_score.items(), key=lambda item: item[1], reverse=True)}
            
            self.scores.append(query_score)
        




    def score_bm25(self):

        for query in self.queries:

            query_score = {}

            temp=0
            query_length=0
            weighted_query={}

            if self.tokenizer=='s':
                simpleTokenizer=SimpleTokenizer()
                query_terms=simpleTokenizer.simple_tokenizer(query)
            else:
                improvedTokenizer=ImprovedTokenizer()
                query_terms=improvedTokenizer.improved_tokenizer(query)

            for term in query_terms:
                if term in self.weighted_index:
                    for doc_id,doc_weight in self.weighted_index[term][1].items():
                        if doc_id in query_score:
                                query_score[doc_id]=query_score[doc_id]+doc_weight
                        else:
                            query_score[doc_id]=doc_weight
            query_score={k: v for k, v in sorted(query_score.items(), key=lambda item: item[1], reverse=True)}
            
            self.scores.append(query_score)
        
        
    