from Evaluation import Evaluation

def test():
    evaluation = Evaluation('queries.relevance.txt')
    print(evaluation.get_relevances())

test()