from Evaluation import Evaluation

def test():
    evaluation = Evaluation('queries.relevance.filtered.txt','ranking_for_evaluation_bm25.txt')
    evaluation.precision_recall()
    evaluation.f1_score()

test()