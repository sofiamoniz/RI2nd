"""
IR, November 2020
Assignment 2: Ranked Retrieval
Autors: Alina Yanchuk, 89093
        Ana Sofia Fernandes, 88739
"""

class Evaluation:
    def __init__(self, relevance_file, score_file):
        self.relevance_file = relevance_file #queries.relevance.txt -> query_id, cord_ui, relevance
        self.score_file = score_file
        self.relevances = {} #{query_1 : [[doc_1 : query_relevance], [doc_2:query_relevance],...] , query_2 :[[doc_1 : query_relevance], [doc_2:query_relevance],...],... }
        self.scores = {}
        self.precision_dic = {}
        self.recall_dic = {}
        self.f1_score_dic = {}

    def get_relevances_or_scores(self, file_to_read):
        relevances_scores = {}
        with open (file_to_read, mode='r') as file_to_read:
            for row in file_to_read:
                query_id = row.split()[0]
                cord_ui = row.split()[1]
                content = row.split()[2]
                if query_id not in relevances_scores.keys():
                    relevances_scores[query_id] = [[cord_ui, content]]
                else:
                    relevances_scores[query_id].append([cord_ui, content])


        return relevances_scores
        

    def precision_recall(self):
        self.relevances = self.get_relevances_or_scores(self.relevance_file)
        self.scores = self.get_relevances_or_scores(self.score_file)
        total_rel_docs = 0
        found = 0
        for query_id in self.scores:
            doc_counter = 0
            found = 0
            total_precision = 0
            if not self.relevances.get(query_id):
                print ("No set for query ", query_id)
                self.precision_dic[query_id] = []
                self.recall_dic[query_id] = []
                continue
            #relevance_doc_list = self.relevances[query_id]
            #total_rel_docs = len (self.relevances[query_id]) 
            self.precision_dic[query_id] = []
            self.recall_dic[query_id] = []

            for scores_doc in self.scores[query_id]:
                doc_counter+=1
                for relevance_doc in self.relevances[query_id]:
                    if (scores_doc[0] == relevance_doc[0]):
                        found += 1
                    if (int(relevance_doc[1]) > 0):
                        total_rel_docs += 1
            self.precision_dic[query_id] = (found/doc_counter)*100
            self.recall_dic[query_id] = (found/total_rel_docs)*100

      
        print("Precision dic-> ", self.precision_dic) #Mais tarde escrevê-los num ficheiro
        print("Recall dic-> ", self.recall_dic)

    def f1_score(self):
        for query_id in self.precision_dic:
            for query_id in self.recall_dic:
                if self.precision_dic[query_id] != 0 and self.recall_dic != 0 :
                    self.f1_score_dic[query_id] = 2 * ((self.precision_dic[query_id]*self.recall_dic[query_id])
                                                        /(self.precision_dic[query_id]+self.recall_dic[query_id])) * 100
                else:
                    self.f1_score_dic[query_id] = 0
      
        print("F1 score -> ", self.f1_score_dic)


