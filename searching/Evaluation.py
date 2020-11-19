"""
IR, November 2020
Assignment 2: Ranked Retrieval
Autors: Alina Yanchuk, 89093
        Ana Sofia Fernandes, 88739
"""

class Evaluation:
    def __init__(self, relevance_file):
        self.relevance_file = relevance_file #queries.relevance.txt -> query_id, cord_ui, relevance
        self.relevances = {} #{query_id : [{doc_1 : query_relevance}, {doc_2:query_relevance}]}

    def get_relevances(self):
        doc_relevance = {}
        #content = []
        with open (self.relevance_file, mode='r') as relevance_file:
            for row in relevance_file:
                query_id = row.split()[0]
                cord_ui = row.split()[1]
                relevance = row.split()[2]
                if query_id not in self.relevances.keys():
                    self.relevances[query_id] = [{cord_ui, relevance}]
                else:
                    self.relevances[query_id].append({cord_ui, relevance})


        return self.relevances #poderá ou não ser necessário




