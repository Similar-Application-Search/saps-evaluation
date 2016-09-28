import numpy
import time

def main():
    MAP = 0
    MapAt5 = 0
    MapAt1 = 0
    MapAt3 = 0

    P_MAP = 0
    P_MapAt5 = 0
    P_MapAt1 = 0
    P_MapAt3 = 0

    countQuery = 0

    threshold = 3
    f = open("user_evaluation_on_Model_A.txt", "w")
    with open("qs5 - Sheet1.tsv") as pf:
        content = pf.readlines()
    for queryIndex in xrange(1, len(content),11):
        #print "queryIndex =",queryIndex,"#########query########", content[queryIndex]
        topN = 10
        avgp = 0.0
        avgpAt5 = 0
        avgpAt1 = 0
        avgpAt3 = 0

        P_avgp = 0.0
        P_avgpAt5 = 0
        P_avgpAt1 = 0
        P_avgpAt3 = 0

        countRelavance = 0

        countRelavance_1 = 0.0
        countRelavance_3 = 0.0
        countRelavance_5 = 0.0
        countRelavance_10 = 0.0

        true_relevane = 10
        totalCategoryRelevance = 10
        countQuery = countQuery + 1  # include this query in the MAP calculation
        for i in range(1, 11):
            line_index = queryIndex+i

            if(line_index>=len(content)):
                print "Out of index ",line_index
                break
            #print "Index: ", line_index, "\t", content[line_index]
            line = content[line_index]

            _,_,_,_,relevance_score = line.split("\t")#split contain additional new line !!!
            relevance_score = relevance_score.replace("\n","")
            if(relevance_score==" "):
                print "This is query project not the results"
                continue
            #print "re score = ",relevance_score
            if relevance_score=="":
                relevance_score=0
            if (float(relevance_score)>=float(threshold)):
                #print " greater re score = ", relevance_score
                countRelavance = countRelavance + 1
                countRelavance_10 = countRelavance_10 + 1

                avgp = avgp + (countRelavance * 1.0) / i;
                if i <= 5:
                    countRelavance_5 = countRelavance_5 + 1
                    avgpAt5 = avgpAt5 + (countRelavance * 1.0) / i;
                if i <= 3:
                    countRelavance_3 = countRelavance_3 + 1
                    avgpAt3 = avgpAt3 + (countRelavance * 1.0) / i;
                if i <= 1:
                    countRelavance_1 = countRelavance_1 + 1
                    avgpAt1 = avgpAt1 + (countRelavance * 1.0) / i;

        if totalCategoryRelevance > 0:
            avgp = (avgp * 1.0) / totalCategoryRelevance
            P_avgp = countRelavance_10 / 10.0
            P_MAP = P_MAP + P_avgp
            # f.write("Average Prevision@10 = "+str(avgp)+"\n")
            # print ("AVG@10"+str(avgp)+"\t" +str(true_relevane)+"\n")
            MAP = MAP + avgp

        # else:
        # f.write("No relevance judgement for this query category. Average Prevision = none \n")
        totalCategoryRelevance_at_5 = min(5, true_relevane)
        if totalCategoryRelevance_at_5 > 0:
            avgpAt5 = (avgpAt5 * 1.0) / totalCategoryRelevance_at_5
            P_avgpAt5 = countRelavance_5 / 5.0
            P_MapAt5 = P_MapAt5 + P_avgpAt5
            # f.write("Average Prevision@5 = "+str(avgpAt5)+"\n")
            # print ("AVG@5"+str(avgpAt5)+"\t" +str(true_relevane)+"\n")
            MapAt5 = MapAt5 + avgpAt5
        # else:
        # f.write("No relevance judgement for this query category. Average Prevision = none \n")
        totalCategoryRelevance_at_1 = min(1, true_relevane)
        if totalCategoryRelevance_at_1 > 0:
            avgpAt1 = (avgpAt1 * 1.0) / totalCategoryRelevance_at_1
            P_avgpAt1 = countRelavance_1 / 1.0
            P_MapAt1 = P_MapAt1 + P_avgpAt1
            # f.write("Average Prevision@1 = "+str(avgpAt1)+"\n")
            # print ("AVG@1"+str(avgpAt1)+"\t" +str(true_relevane)+"\n")
            MapAt1 = MapAt1 + avgpAt1
        # else:
        # f.write("No relevance judgement for this query category. Average Prevision = none \n")

        totalCategoryRelevance_at_3 = min(3, true_relevane)
        if totalCategoryRelevance_at_3 > 0:
            avgpAt3 = (avgpAt3 * 1.0) / totalCategoryRelevance_at_3
            P_avgpAt3 = countRelavance_3 / 3.0
            P_MapAt3 = P_MapAt3 + P_avgpAt3
            # f.write("Average Prevision@3 = "+str(avgpAt3)+"\n")
            # print ("AVG@1"+str(avgpAt1)+"\t" +str(true_relevane)+"\n")
            MapAt3 = MapAt3 + avgpAt3
            # else:
            # f.write("No relevance judgement for this query category. Average Prevision = none \n")
        f.write("Query: "+str(countQuery)+"\t" + str(threshold) + "\t" + str(avgpAt1) + "\t" + str(avgpAt3) + "\t" + str(avgpAt5) + "\t" + str(
            avgp) + "\t" + str(P_avgpAt1) + "\t" + str(
            P_avgpAt3) + "\t" + str(P_avgpAt5) + "\t" + str(P_avgp))
        #print("Query: "+str(countQuery)+"\t" + str(threshold) + "\t" + str(avgpAt1) + "\t" + str(avgpAt3) + "\t" + str(avgpAt5) + "\t" + str(
        #    avgp) + "\t" + str(P_avgpAt1) + "\t" + str(
        #    P_avgpAt3) + "\t" + str(P_avgpAt5) + "\t" + str(P_avgp))

    if countQuery > 0:
        MAP = (MAP * 1.0) / countQuery
        MapAt5 = (MapAt5 * 1.0) / countQuery
        MapAt1 = (MapAt1 * 1.0) / countQuery
        MapAt3 = (MapAt3 * 1.0) / countQuery

        P_MAP = (P_MAP * 1.0) / countQuery
        P_MapAt5 = (P_MapAt5 * 1.0) / countQuery
        P_MapAt1 = (P_MapAt1 * 1.0) / countQuery
        P_MapAt3 = (P_MapAt3 * 1.0) / countQuery
    #print "Total query = ",countQuery
    f.write("Mean: \t"+str(threshold)+"\t"+str(MapAt1) + "\t" + str(MapAt3) + "\t" + str(MapAt5) + "\t" + str(MAP) + "\t" + str(P_MapAt1) + "\t" + str(
        P_MapAt3) + "\t" + str(P_MapAt5) + "\t" + str(P_MAP) + "\n")
    print("Mean: \t"+str(threshold)+"\t"+str(MapAt1) + "\t" + str(MapAt3) + "\t" + str(MapAt5) + "\t" + str(MAP) + "\t" + str(P_MapAt1) + "\t" + str(
        P_MapAt3) + "\t" + str(P_MapAt5) + "\t" + str(P_MAP) + "\n")


    print "done"
if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)
