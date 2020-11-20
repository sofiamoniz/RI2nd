from Evaluation import Evaluation

def test():
    evaluation = Evaluation("searching/queries.relevance.filtered.txt","searching/ranking_for_evaluation_bm25.txt")
    evaluation.mean_precision_recall()
    evaluation.mean_f1()
    evaluation.map()

test()