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

    def __init__(self,total_docs,inverted_index):
        self.total_docs=total_docs
        self.inverted_index=inverted_index
        self.weighted_index={}
        self.idf_docsWeight = [] # [idf,docWeights_with_lnc_ltc]  
                              # In python, the order of an array is mantained, so no problem!
        
    ## inverted_index = { "term" : [ doc_freq, {"doc1":occurrences_of_term_in_doc1, "doc2": occurrences_of_term_in_doc2,...}],...  }
    ## weighted_index = { "term" : [ idf, {"doc1":weight_of_term_in_doc1,"doc2":weight_of_term_in_doc2,...}],...  }
    
    def idf_calculation(self, term):
        idf = math.log10(self.total_docs/self.inverted_index[term][0]) #self.inverted_index[term][0] = term_info["document_frequency"]
        self.idf_docsWeight.append(idf)

    # lnc.ltc
    def weighted_index_lnc_ltc(self):
        for term in self.inverted_index:
            idf_docsWeight=[] 
            docsWeigh={} # {"doc1":weight_of_term_in_doc1,"doc2":weight_of_term_in_doc2,...}  only with documents where the term occurs
            
            self.idf_calculation(term)           

            doc_length = defaultdict(int) #This will be used as the normalization factor.
                                        #This is a default dictionary so that if a certain value doesn't exist,
                                        # it will have a default value of 0

            
            for doc_id in self.inverted_index[term][1]: #self.inverted_index[term][1]) contains : {docID: tf}
                tf = self.inverted_index[term][1][doc_id] #term frequency (tf) - number of times each term appears in a doc
                weight = 1+math.log10(tf) #this calculates the weight of term-document
                docsWeigh[doc_id] = weight
                doc_length[doc_id] += weight ** 2
                print("weight ", weight)

            
            idf_docsWeight.append(docsWeigh) #sem normalizar já fica feito aqui


            #normalization
            '''
            for doc_id in doc_length:
                    doc_length[doc_id] = math.sqrt(doc_length[doc_id])

            for doc_id in docsWeigh:
                docsWeigh[doc_id] /= doc_length[doc_id]
             #   for doc_id in 
            '''
            #idf_docsWeight.append(docsWeigh)

            self.weighted_index[term]=idf_docsWeight
            

    # bm25
    def weighted_index_bm25(self):
       
        for term in self.inverted_index:
            docsWeigh={} # {"doc1":weight_of_term_in_doc1,"doc2":weight_of_term_in_doc2,...}  only with documents where the term occurs
            
            self.idf_calculation(term)         

            
            # TO DO: calcular as weights

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

