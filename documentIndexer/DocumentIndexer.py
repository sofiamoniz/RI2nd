"""
IR, October 2020
Assignment 1: Indexing documents
Autors: Alina Yanchuk, 89093
        Ana Sofia Fernandes, 88739
"""


from documentIndexer.CorpusReader import CorpusReader
from documentIndexer.Indexer import Indexer
from documentIndexer.Results import Results
from documentIndexer.WeightedIndexer import WeightedIndexer
import time
import os
import psutil

## Class that acts as a pipeline for the all indexing process ( calls all the other classes and methods  )

class DocumentIndexer:

    def __init__(self,input_file,tokenizer_type):
        self.input_file=input_file
        self.tokenizer_type=tokenizer_type

    def document_indexer(self):

        """
        Index the documents and prints the results and relevant information
        
        Follows this pipeline:

                Read Corpus     
                    |
                Tokenize
                    |             -----> Here, we already have all documents tokenized.
                Index   ( one document at a time )
                    |             -----> Here, we already have all documents indexed ( or the ordered Inverted Index created )
                Store and print results
    
        """

        doc_ids={}
        total_docs=0
        total_terms=0
        indexing_time=0

        start_time = time.time()
        corpusReader = CorpusReader(self.input_file,self.tokenizer_type) ## Corpus Reader with Tokenization
        corpus,real_doc_ids=corpusReader.read_content() # corpus: [[doc1_terms_after_tokenization],[doc2_terms_after_tokenization]...]
                                                        # real_doc_ids: [real_doc1_id,real_doc2_id,...]
        total_docs=len(corpus)
        
        for j in range(total_docs):    
            total_terms=total_terms+len(corpus[j])  # vocabulary size or number of terms
 



        indexer = Indexer(total_docs) ## Indexer
        for i in range(total_docs):   # Index one document at a time. The id's are auto generated by incrementation, starting at id=1 
            generated_id=i+1 
            indexer.index_document(corpus[i],generated_id)
            doc_ids[generated_id]=real_doc_ids[i]
        indexer.sort_inverted_index() ## All documents have been indexed and the final Inverted Indexer created!
        indexing_time=time.time()-start_time
        inverted_index=indexer.get_inverted_index()
        

        weighted_index = WeightedIndexer(total_docs, inverted_index)
        weighted_index.weighted_index_lnc_ltc()
        #weighted_index.weighted_index_bm25()
        weighted_index.show_weighted_index()

"""
        results = Results(inverted_index,doc_ids,self.tokenizer_type,self.input_file) ## Results ( writes informations to files )
        results.write_document_ids_to_file()
        results.write_index_to_file()
        #results.print_table_for_inverted_index() # This line can be descommented if we wish to print the table in the terminal
        


        process = psutil.Process(os.getpid())
        
        memory_used= self.format_bytes(process.memory_info().rss) # Memory used by the Python program
        memory_dic = self.format_bytes(indexer.get_size_in_mem()) # Memory occupied by the structure used

        


        # Print results:
        if(self.tokenizer_type=="s"):
            print("\n    Tokenizer used: Simple \n"
                    +"\n--- Number of documents:  %s documents." % (total_docs) 
                    +"\n--- Total number of terms (vocabulary size): %d terms." % (total_terms)
                    +"\n--- Indexation time:  %s seconds." % (round(indexing_time,3))
                    +"\n--- Size in memory used by the dictionary structure:  %s %s." % (round(memory_dic[0],3), memory_dic[1])
                    +"\n--- Memory required by the program:  %s %s." % (round(memory_used[0],3), memory_used[1])
                    + "\n--- Directory with the Inverted Index: results/simpleTokenizer"
                    + "\n--- Directory that contains the real document Id's and auto generated ones: results\n")
        else:
            print("\n    Tokenizer used: Improved \n"
                    +"\n--- Number of documents:  %s documents." % (total_docs) 
                    +"\n--- Total number of terms (vocabulary size): %d terms." % (total_terms)
                    +"\n--- Indexation time:  %s seconds." % (round(indexing_time,3))
                    +"\n--- Size in memory used by the dictionary structure:  %s %s." % (round(memory_dic[0],3), memory_dic[1])
                    +"\n--- Memory required by the program:  %s %s." % (round(memory_used[0],3), memory_used[1])
                    + "\n--- Directory with the Inverted Index: results/improvedTokenizer"
                    + "\n--- Directory that contains the real document Id's and auto generated ones: results\n")
        print("\nAnswers to 4. c) and d) :")
        print("\nTop 10 terms with frequency 1: "+str(results.terms_doc_frequency_1()))
        print("\nTop 10 terms with highest frequency: "+str(results.terms_highest_doc_frequency()))



    def format_bytes(self,size): 

        
        power = 2**10 # 2**10 = 1024
        n = 0
        power_labels = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
        while size > power:
            size /= power
            n += 1
        return size, power_labels[n]+'bytes'

"""