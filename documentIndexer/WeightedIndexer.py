"""
IR, October 2020
Assignment 1: Indexing documents
Autors: Alina Yanchuk, 89093
        Ana Sofia Fernandes, 88739
"""

from sys import getsizeof
import math
from collections import defaultdict


## Class that creates the Weighted Index from the InvertedIndex

class WeightedIndexer:

    def __init__(self,total_docs,inverted_index, document_len):
        self.total_docs=total_docs
        self.inverted_index=inverted_index
        self.document_len=document_len
        self.weighted_index={}
        
    ## inverted_index = { "term" : [ doc_freq, {"doc1":occurrences_of_term_in_doc1, "doc2": occurrences_of_term_in_doc2,...}],...  }
    ## weighted_index = { "term" : [ idf, {"doc1":weight_of_term_in_doc1,"doc2":weight_of_term_in_doc2,...}],...  }
    

    # lnc.ltc
    def weighted_index_lnc_ltc(self):       

        for term in self.inverted_index:
            docsWeigh={} # {"doc1":weight_of_term_in_doc1,"doc2":weight_of_term_in_doc2,...}  only with documents where the term occurs
            idf_docsWeight=[] # [idf,docWeights_with_lnc_ltc]  
                        # In python, the order of an array is mantained, so no problem!
            
            idf = math.log10(self.total_docs/self.inverted_index[term][0])
            idf_docsWeight.append(idf)         

            doc_pow_sum = defaultdict(int) #This will be used as the normalization factor.
                                        #This is a default dictionary so that if a certain value doesn't exist,
                                        # it will have a default value of 0

            
            for doc_id in self.inverted_index[term][1]: #self.inverted_index[term][1]) contains : {docID: tf}
                tf = self.inverted_index[term][1][doc_id] #term frequency (tf) - number of times each term appears in a doc
                weight = 1+math.log10(tf) #this calculates the weight of term-document
                #docsWeigh[doc_id] = weight
                doc_pow_sum[doc_id] += weight ** 2 # sum of all the weights of each document
                                                    #each weight to the pow of 2
                                                    #this will be used in the cossine normalization

            #normalization - cossine normalization
            #the cossine normalization is sqrt the inverse of the sum of all the weights of a document, 
            #each one to the pow of 2
            for doc_id in doc_pow_sum:
                docsWeigh[doc_id] = 1 / math.sqrt(doc_pow_sum[doc_id])
                        
            idf_docsWeight.append(docsWeigh)

            self.weighted_index[term]=idf_docsWeight
            

    # bm25
    def weighted_index_bm25(self, total_terms, k = 1.2 , b = 0.75): # k is a value between 1.2 and 2.0     

        for term in self.inverted_index:  
            docsWeigh=defaultdict(int) # {"doc1":weight_of_term_in_doc1,"doc2":weight_of_term_in_doc2,...}  only with documents where the term occurs
            idf_docsWeight=[] # [idf,docWeights_with_lnc_ltc]  
                                    # In python, the order of an array is mantained, so no problem!
            #final_score = defaultdict(int)          
            idf = math.log10(self.total_docs/self.inverted_index[term][0])
            idf_docsWeight.append(idf)

            for doc_id in self.inverted_index[term][1]: #self.inverted_index[term][1]) contains : {docID: tf}
                tf = self.inverted_index[term][1][doc_id] #term frequency (tf) - number of times each term appears in a doc
                len_of_doc = self.document_len[doc_id]
                avgdl = len_of_doc / total_terms
                docsWeigh[doc_id] += (idf * tf * k
                      / (tf + k * (1 - b + b * len_of_doc / avgdl)))
           
            idf_docsWeight.append(docsWeigh)

            self.weighted_index[term]=idf_docsWeight
        
  

            



    def get_weighted_index(self):

        """
        Returns the dictionary with the Inverted Index
        """

        return self.weighted_index             
                
                   

    def sort_weighted_index(self):    
        pass



    def show_weighted_index(self):

        """
        Prints the Inverted Index
        """

        print(self.weighted_index) 
   


    def get_size_in_mem(self):

        """
        Returns the size of the dictionary with the Weighted Index
        """

        return getsizeof(self.weighted_index)

