"""
IR, November 2020
Assignment 2: Ranked Retrieval
Autors: Alina Yanchuk, 89093
        Ana Sofia Fernandes, 88739
"""

import sys, getopt
from searching.RetrievalEngine import RetrievalEngine

## Main class that runs the searching part of the program ( gets the arguments from command line and starts the program )
def main():

    """
    The program needs 2 arguments: file with the weighted index and file with the queries

    And PyStemmer instaled: pip install pystemmer
                            pip install psutil

    Examples of usage:

        python3 Search.py results/improvedTokenizer/weightedIndex_lnc_ltc.txt queries.txt
        python3 Search.py results/simpleTokenizer/weightedIndex_bm25.txt queries.txt
    """

    if len(sys.argv) != 3: 
        print ("\nUsage:\n\n   Search.py <weightedIndexFile> <queryFile>\n\n Example: Search.py results/simpleTokenizer/weightedIndex_bm25.txt queries.txt")
        sys.exit()


    index_file=sys.argv[1]
    query_file=sys.argv[2]
    tokenizer=index_file[8:9] # type of tokenizer in the weighted index ('s' or 'i')
    if "bm25" in index_file: ranking="bm25"   # type of ranking in the weighted index ('bm25' or 'lnc.ltc')
    else: ranking_type="lnc.ltc"
 
    search = RetrievalEngine(tokenizer,ranking_type,index_file,query_file)
    search.query_search()


if __name__ == '__main__':
    main()