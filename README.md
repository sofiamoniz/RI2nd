    IR, November 2020
    Assignment 2: Ranked Retrieval
    Authors: Alina Yanchuk, 89093; Ana Sofia Fernandes, 88739

#### The Ranking process is divided in two programs: the indexing and the searching

The indexing program produces a file with the Weighted Index, based on the Tokenizer and Ranking function chosen, and a file with the documents IDs mapping, that will be used in the searching process.
The searching program produces a file with the Ranking results and shows the Evaluation metrics calculated.

In order to everything work correctly, all the generated files by the indexing program must not have their defined names and Relative Paths changed!


## To run the scripts:

    1. Run the command pip install nltk
    2. Run the command pip install psutil
    3. Run the command pip install pystemmer
    
    4. Execute the two commands:    


    1st:    python3 Index.py <typeOfTokenizer> <fileToRead> <typeOfRanking>       ->  typeOfTokenizer: -s      or   -i   
                                                                                  ->  typeOfRanking:   -bm25   or   -lnc.ltc
            Example:
                python3 Index.py -s metadata_2020-03-27.csv -bm25
                python3 Index.py -i metadata_2020-03-27.csv -lnc.ltc


    2nd:    python3 Search.py <weightedIndexFile> <queryFile> <queryRelevancesFile> <numberOfDocsToReturn>

            Example: 
                python3 Search.py results/improvedTokenizer/weightedIndex_bm25.txt queries.txt queries.relevance.filtered.txt 50
                python3 Search.py results/improvedTokenizer/weightedIndex_lnc_ltc.txt queries.txt queries.relevance.filtered.txt 10

    
    NOTE: As said, the <weightedIndexFile> must be the Relative Path to that file, generated automatically by the indexing program!

##### All the results (Weighted Index, document IDs mapping and Ranking) are stored in the "results" folder             

##### The table with the Evaluation metrics can be found in the "results" folder, in the file table_evaluation.pdf
