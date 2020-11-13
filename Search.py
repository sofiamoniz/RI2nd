"""
IR, October 2020
Assignment 1: Indexing documents
Autors: Alina Yanchuk, 89093
        Ana Sofia Fernandes, 88739
"""


import sys, getopt
from searching.QuerySearch import QuerySearch

## Main class that
def main():

    if len(sys.argv) != 3: 
        print ("\nUsage:\n\n   Search.py <weightedIndexFile> <queryFile>\n\n Example: Search.py results/simpleTokenizer/weightedIndex_bm25.txt queries.txt")
        sys.exit()


    index_file=sys.argv[1]
    query_file=sys.argv[2]
    tokenizer=index_file[8:9] # 's' or 'i'
    if "bm25" in index_file: ranking="bm25"
    else: ranking="lnc.ltc"
 
    search = QuerySearch(tokenizer,ranking,index_file,query_file)
    search.query_search()



if __name__ == '__main__':
    main()