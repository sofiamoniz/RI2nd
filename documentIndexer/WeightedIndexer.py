"""
IR, October 2020
Assignment 1: Indexing documents
Autors: Alina Yanchuk, 89093
        Ana Sofia Fernandes, 88739
"""

from sys import getsizeof
import math

## Class that creates the Weighted Index from the InvertedIndex

class WeightedIndexer:

    def __init__(self,total_docs,inverted_index):
        self.total_docs=total_docs
        self.inverted_index=inverted_index
        self.weighted_index=dict()
        
    ## inverted_index = { "term" : [ doc_freq, {"doc1":occurrences_of_term_in_doc1, "doc2": occurrences_of_term_in_doc2,...}],...  }
    ## weighted_index = { "term" : [ idf, {"doc1":weight_of_term_in_doc1,"doc2":weight_of_term_in_doc2,...}],...  }
    
    # lnc.ltc
    def weighted_index_lnc_ltc(self):

        for term in self.inverted_index:
            idf_docsWeight=[] # [idf,docWeights_with_lnc_ltc]  
                              # In python, the order of an array is mantained, so no problem!
            docsWeigh={} # {"doc1":weight_of_term_in_doc1,"doc2":weight_of_term_in_doc2,...}  only with documents where the term occurs
            
            idf = math.log10(self.total_docs/self.inverted_index[term][0])
            idf_docsWeight.append(idf)

            # TO DO: calcular as weights

            self.weighted_index[term]=idf_docsWeight
            

    # bm25
    def weighted_index_bm25(self):
       
        for term in self.inverted_index:
            idf_docsWeight=[] # [idf,docWeights_with_bm25]  
                              # In python, the order of an array is mantained, so no problem!
            docsWeigh={} # {"doc1":weight_of_term_in_doc1,"doc2":weight_of_term_in_doc2,...}  only with documents where the term occurs
            
            idf = math.log10(self.total_docs/self.inverted_index[term][0])
            idf_docsWeight.append(idf)

            idf_docsWeight.append("weight")
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

