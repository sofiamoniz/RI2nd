"""
IR, October 2020
Assignment 1: Indexing documents
Autors: Alina Yanchuk, 89093
        Ana Sofia Fernandes, 88739
"""


import sys, getopt
from searching.Search import Search

## Main class that

def main():

    if len(sys.argv) != 4: 
        print('Invalid parameters! \nUsage: python3 bin/Fcm.py example/<file_name> <alpha> <k-context size>')
        sys.exit()
    elif sys.argv[1]!='-i' or sys.argv[1]!='-s':
        print('Invalid alpha! Must be between 0 and 1.')
        sys.exit()

    tokenizer=sys.argv[1] 
    index_file=sys.argv[2]
    query_file=sys.argv[3]

 
    Search(tokenizer,index_file,query_file)



if __name__ == '__main__':
    main()