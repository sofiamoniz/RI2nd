##IR, November 2020
##Assignment 2: Ranked Retrieval
##Authors: Alina Yanchuk, 89093; Ana Sofia Fernandes, 88739


### To run the script:

    1. Run the command pip install nltk
    2. Run the command pip install psutil
    3. Execute the command: 

        Search.py <weightedIndexFile> <queryFile> <queryRelevancesFile> <numberOfDocsToReturn>

        Example: 
            python3 Search.py results/simpleTokenizer/weightedIndex_bm25.txt queries.txt queries.relevance.filtered.txt 50
            or
            python3 Search.py results/simpleTokenizer/weightedIndex_lnc_ltc.txt queries.txt queries.relevance.filtered.txt 10

### All the results (Inverted Index, ID's mapping files and scores for each method and tokenizer) are stored in the "results" folder             

### The table with the rankings can be found in the "results" folder, in the file table_rankings.pdf
