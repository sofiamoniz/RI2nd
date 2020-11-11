"""
IR, October 2020
Assignment 1: Indexing documents
Autors: Alina Yanchuk, 89093
        Ana Sofia Fernandes, 88739
"""


import sys, getopt
from documentIndexer.DocumentIndexer import DocumentIndexer

## Main class that runs the project ( gets the arguments from command line and starts the program )

def main(argv):

    """
    The program needs 2 arguments: type of tokenizer and file to read.

    And PyStemmer instaled: pip install pystemmer
                            pip install psutil

    Examples of usage:

        python3 Main.py -s "all_sources_metadata_2020-03-13.csv"
        python3 Main.py -i "all_sources_metadata_2020-03-13.csv"

    After running, the results files are stored in the "results" folder.
    """

    input_file = ''

    try:
        opts,args = getopt.getopt(argv,"hs:i:",["sfile=","ifile="])
    except getopt.GetoptError: # If there's an argument error, the instructions are shown
        print ('\nUsage:\nMain.py -s <fileToRead>\nor Main.py -i <fileToRead>')
        sys.exit(2)
    if opts==[]: # If the user didn't pass any arguments
        print ('\nUsage:\nMain.py -s <fileToRead>\nor Main.py -i <fileToRead>')
        sys.exit()
    for opt, arg in opts:
        if opt == '-h': # If the user looks for help, the instructions are shown
            print ('\nUsage:\nMain.py -s <fileToRead>\nor Main.py -i <fileToRead>')
            sys.exit()            
        elif opt in ("-s", "--sfile"): # The user choses to use the simple tokenizer
            input_file = arg
            doc_indexer= DocumentIndexer(input_file,'s')
            doc_indexer.document_indexer()
        elif opt in ("-i", "--ifile"): # The user choses to use the improved tokenizer
            input_file = arg
            doc_indexer=DocumentIndexer(input_file,'i')
            doc_indexer.document_indexer()



if __name__ == '__main__':
    main(sys.argv[1:])