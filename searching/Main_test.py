from Evaluation import Evaluation

def test():
    evaluation = Evaluation("queries.relevance.filtered.txt","ranking_for_evaluation_bm25.txt")
    evaluation.mean_precision_recall()
    evaluation.mean_f1()
    evaluation.mean_average_precision()
    evaluation.mean_ndcg()

test()