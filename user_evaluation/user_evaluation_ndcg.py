import numpy as np
import time
def ndcg(rank_score_list,at_value):
    active_list_score = rank_score_list[:at_value]

    ground_truth = sorted(active_list_score,reverse=True)
    dcg_gt = dcg(ground_truth)
    dcg_model = dcg(active_list_score)
    if(dcg_gt==0):
        return 0
    ndcg_val = (dcg_model*1.0)/dcg_gt
    return ndcg_val
def dcg(rank_score):
    discounted_cummulative_gain=0
    for i in range(1,len(rank_score)+1):
        rel_score = rank_score[i-1]
        #discounted_gain = (rel_score*1.0)/(np.log2(i))
        discounted_gain = ((2**rel_score) -1.0) / (np.log2(i+1))
        discounted_cummulative_gain = discounted_cummulative_gain + discounted_gain
    return discounted_cummulative_gain
def get_evaluation_list(filepath):
    with open(filepath) as pf:
        content = pf.readlines()
    query_score_list = []
    #for query_index in range(1,len(content),11):
    for query_index in range(1, len(content), 11):
        list_line = []
        for line_index in range(query_index+1,query_index+11):
            line = content[line_index]
            _, _, _, _, relevance_score = line.split("\t")  # split contain additional new line !!!

            relevance_score = relevance_score.replace("\n", "")
            if relevance_score=="":
                relevance_score=0
            #print "re ",relevance_score," ",query_index
            list_line.append(float(relevance_score))
        query_score_list.append(list_line)

    return query_score_list
def main():
    query_score_matrix = get_evaluation_list("qs5 - Sheet1.tsv")
    print("query" + "\t" + "ndcg_5" + "\t" + "ndcg_10")
    countquery=len(query_score_matrix)
    total_ndcg_5=0
    total_ndcg_10 = 0
    for query_index in range(0,len(query_score_matrix)):
        ndcg_5 = ndcg(query_score_matrix[query_index],5)
        ndcg_10 = ndcg(query_score_matrix[query_index], 10)
        total_ndcg_5 = total_ndcg_5 + ndcg_5
        total_ndcg_10 = total_ndcg_10 + ndcg_10
        #print(str(query_index+1)+"\t"+str(ndcg_5)+"\t"+str(ndcg_10))
    print("Mean:" + "\t" + str(total_ndcg_5/countquery) + "\t" + str(total_ndcg_10/countquery))
if __name__ == "__main__":
    main()
