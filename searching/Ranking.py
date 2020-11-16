"""
IR, November 2020
Assignment 2: Ranked Retrieval
Autors: Alina Yanchuk, 89093
        Ana Sofia Fernandes, 88739
"""

from indexing.ImprovedTokenizer import ImprovedTokenizer
from indexing.SimpleTokenizer import SimpleTokenizer
import math
from collections import defaultdict

## Class that
class Ranking:

    def __init__(self,tokenizer,queries,weighted_index):
        self.tokenizer=tokenizer
        self.weighted_index=weighted_index
        self.queries=queries

        self.weighted_queries=[] # only for lnc.ltc

        self.scores=[]


    # lnc.ltc:

    def weight_queries_lnc_ltc(self):

        """
        Computes the weights for each term of the query, for all the queries
        """

        for query in self.queries: # one query at a time

            temp=0
            query_length=0
            weighted_query=defaultdict(int)    # weighted_query = { "term1": weight_of_term1_in_query, ...}   for all terms in the query

            # Tokenize the query with the same tokenizer used on the documents:
            if self.tokenizer=='s':
                simpleTokenizer=SimpleTokenizer()
                query_terms = simpleTokenizer.simple_tokenizer(query)
            else:
                improvedTokenizer=ImprovedTokenizer()
                query_terms = improvedTokenizer.improved_tokenizer(query)

            for term in query_terms: # query terms already tokenized and processed
                weighted_query[term] = weighted_query[term]+1 # tf on query

            for term in weighted_query:
                if term in self.weighted_index.keys(): # if the term exists on any document      
                    weighted_query[term] = (1 + math.log10(weighted_query[term])) * self.weighted_index[term][0] # self.weighted_index[term][0] -> idf of the term 
 

            # Normalization:
            for term,value in weighted_query.items():
                temp = temp + (math.pow(value,2))
            query_length = math.sqrt(temp)
            for term,value in weighted_query.items():
                weighted_query[term] = value / query_length

            self.weighted_queries.append(weighted_query) # self.weighted_queries = [ weighted_query1, weighted_query2, ...]
           
                
     
    def score_lnc_ltc(self):

        """
        Computes the scores for all documents that answers the query
        """

        for i in range(0,len(self.queries)): # one query at a time

            docs_scores=defaultdict(int) # docs_score = { doc1: score1, doc2: score2, ...} for all docs that answers the query

            for term,term_query_weight in self.weighted_queries[i].items():  
                if term in self.weighted_index: # if term exists in any document
                    for doc_id,term_doc_weight in self.weighted_index[term][1].items(): # all docs ( their ids and weights for this term ) that have the term 
                        docs_scores[doc_id] = docs_scores[doc_id] + (term_query_weight * term_doc_weight)

            docs_scores={k: v for k, v in sorted(docs_scores.items(), key=lambda item: item[1], reverse=True)} # order by score ( decreasing order )
            
            self.scores.append(docs_scores) # self.scores = [ scores_for_query1, scores_for_query2, ...]
        




    # bm25:

    def score_bm25(self):

        for query in self.queries: # one query at a time

            docs_scores=defaultdict(int) # docs_score = { doc1: score1, doc2: score2, ...} for all docs that answers the query
            temp=0
            query_length=0

            # Tokenize the query with the same tokenizer used on the documents:
            if self.tokenizer=='s':
                simpleTokenizer=SimpleTokenizer()
                query_terms=simpleTokenizer.simple_tokenizer(query)
            else:
                improvedTokenizer=ImprovedTokenizer()
                query_terms=improvedTokenizer.improved_tokenizer(query)


            for term in query_terms: # query terms already tokenized and processed
                if term in self.weighted_index:  # if term exists in any document
                    for doc_id,doc_weight in self.weighted_index[term][1].items(): # all docs ( their ids and weights for this term ) that have the term 
                        docs_scores[doc_id]=docs_scores[doc_id]+doc_weight
         
            docs_scores={k: v for k, v in sorted(docs_scores.items(), key=lambda item: item[1], reverse=True)} # order by score ( decreasing order )
            
            self.scores.append(docs_scores) # self.scores = [ scores_for_query1, scores_for_query2, ...]
        
        
    