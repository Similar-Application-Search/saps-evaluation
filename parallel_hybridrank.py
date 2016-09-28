import numpy
import time
from joblib import Parallel, delayed
import multiprocessing


def readProjectDetails(projectDetailsFile):
	projectDetails = []
	projectName = []
	for line in open(projectDetailsFile):
		if '\t' in line:
			lineTokens = line.split('\t', 1)
			projectDetails.append(lineTokens[1])
			projectName.append(lineTokens[0])
		else:
			print 'no tap space: ', line
	return projectName, projectDetails

def execute_single_query(description_matrix, readme_matrix,methodclass_matrix, packageclass_matrix, querycategory, candidatecategory, category_stats,queryindex):
    matrix_entry = []
    distances = []
    for candidate_index in range(0, len(candidatecategory)):  # skip very first element ,as it is 0 valued

        if numpy.isnan(description_matrix[queryindex][candidate_index]):
            des_val = 2  # infinite
        else:
            des_val = description_matrix[queryindex][candidate_index]

        if numpy.isnan(readme_matrix[queryindex][candidate_index]):
            readme_val = 2  # infinite
        else:
            readme_val = readme_matrix[queryindex][candidate_index]

        if numpy.isnan(methodclass_matrix[queryindex][candidate_index]):
            methodclass_val = 2  # infinite
        else:
            methodclass_val = methodclass_matrix[queryindex][candidate_index]

        if numpy.isnan(packageclass_matrix[queryindex][candidate_index]):
            packageclass_val = 2  # infinite
        else:
            packageclass_val = packageclass_matrix[queryindex][candidate_index]

        weight_description = 1
        weight_readme = 1
        weight_methodclass = 1
        weight_packageclass = 1
        hybrid_distance = (weight_description * des_val) + (weight_readme * readme_val) + (
            weight_methodclass * methodclass_val) + (weight_packageclass * packageclass_val)

        distances.append((candidate_index, hybrid_distance))

    distances.sort(key=lambda x: x[1])
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

    true_relevane = category_stats.get(querycategory[queryindex].replace("\n", ""),
                                       0)  # minimum between n and total relevance document, n is top
    totalCategoryRelevance = min(topN, true_relevane)
    # f.write("Rank"+"\t"+"Search Project: "+testProjectName[queryIndex]+"\t"+testProjectDetails[queryIndex].replace("\n","")+"\t"+testProjectGitURL[queryIndex].replace("\n","")+"\t"+testProjectCategory[queryIndex])
    # print ("Rank"+"\t"+"Search Project: "+testProjectName[queryIndex]+"\t"+testProjectDetails[queryIndex].replace("\n","")+"\t"+testProjectGitURL[queryIndex].replace("\n","")+"\t"+testProjectCategory[queryIndex])
    for i in range(1, len(distances)):
        if (querycategory[queryindex] == candidatecategory[i]):
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

        if i >= 10:
            break

    return (totalCategoryRelevance, true_relevane, countRelavance_10,  countRelavance_5, countRelavance_3, countRelavance_1, avgp, avgpAt5, avgpAt3, avgpAt1)



def main():
    query_project_path = "./data/testProjectCategory.txt"
    candidate_project_path = "./data/trainProjectCategory.txt"

    description_path = "./data/description.txt"
    readme_path = "./data/readme.txt"
    methodclass_path = "./data/methodclass.txt"
    packageclass_path = "./data/package_class.txt"

    description_matrix = numpy.loadtxt(open(description_path, "rb"), delimiter=",")
    readme_matrix = numpy.loadtxt(open(readme_path, "rb"), delimiter=",")
    methodclass_matrix = numpy.loadtxt(open(methodclass_path, "rb"), delimiter=",")
    packageclass_matrix = numpy.loadtxt(open(packageclass_path, "rb"), delimiter=",")

    query_project_name, querycategory = readProjectDetails(query_project_path)
    candidate_project_name, candidatecategory = readProjectDetails(candidate_project_path)
    learning_matrix = []
    f = open("save_hybrid_rank.txt", "w")

    category_stats = {}
    with open(candidate_project_path) as fc:
        for line in fc:
            pname, pcategory = line.split("\t")
            pcategory = pcategory.replace("\n", "")
            count_key = category_stats.get(pcategory, 0)  # if not found will return zero
            category_stats[pcategory] = int(count_key) + 1

    MAP = 0
    MapAt5 = 0
    MapAt1 = 0
    MapAt3 = 0

    P_MAP = 0
    P_MapAt5 = 0
    P_MapAt1 = 0
    P_MapAt3 = 0

    countQuery = len(querycategory)


    num_cores = multiprocessing.cpu_count()
    print "numcore = ", num_cores
    results = Parallel(n_jobs=num_cores)(delayed(execute_single_query)(description_matrix, readme_matrix, methodclass_matrix, packageclass_matrix, querycategory,
            candidatecategory, category_stats, queryindex) for queryindex in range(countQuery))
    #print results

    for queryindex in range(0, len(querycategory)):
        '''
        totalCategoryRelevance, true_relevane, countRelavance_10, countRelavance_5, countRelavance_3, countRelavance_1, avgp, avgpAt5, avgpAt3, avgpAt1 = execute_single_query(
            description_matrix, readme_matrix, methodclass_matrix, packageclass_matrix, querycategory,
            candidatecategory, category_stats, queryindex)
        '''
        text = results[queryindex]
        totalCategoryRelevance = text[0]
        true_relevane = text[1]
        countRelavance_10 = text[2]
        countRelavance_5 = text[3]
        countRelavance_3 = text[4]
        countRelavance_1 = text[5]
        avgp = text[6]
        avgpAt5 = text[7]
        avgpAt3 = text[8]
        avgpAt1 = text[9]

        if totalCategoryRelevance > 0:
            avgp = (avgp * 1.0) / totalCategoryRelevance
            P_avgp = countRelavance_10 / 10.0
            P_MAP = P_MAP + P_avgp
            MAP = MAP + avgp
        totalCategoryRelevance_at_5 = min(5, true_relevane)
        if totalCategoryRelevance_at_5 > 0:
            avgpAt5 = (avgpAt5 * 1.0) / totalCategoryRelevance_at_5
            P_avgpAt5 = countRelavance_5 / 5.0
            P_MapAt5 = P_MapAt5 + P_avgpAt5
            MapAt5 = MapAt5 + avgpAt5
        # else:
        # f.write("No relevance judgement for this query category. Average Prevision = none \n")
        totalCategoryRelevance_at_1 = min(1, true_relevane)
        if totalCategoryRelevance_at_1 > 0:
            avgpAt1 = (avgpAt1 * 1.0) / totalCategoryRelevance_at_1
            P_avgpAt1 = countRelavance_1 / 1.0
            P_MapAt1 = P_MapAt1 + P_avgpAt1
            MapAt1 = MapAt1 + avgpAt1
        # else:
        # f.write("No relevance judgement for this query category. Average Prevision = none \n")

        totalCategoryRelevance_at_3 = min(3, true_relevane)
        if totalCategoryRelevance_at_3 > 0:
            avgpAt3 = (avgpAt3 * 1.0) / totalCategoryRelevance_at_3
            P_avgpAt3 = countRelavance_3 / 3.0
            P_MapAt3 = P_MapAt3 + P_avgpAt3
            MapAt3 = MapAt3 + avgpAt3
    if countQuery > 0:
        MAP = (MAP * 1.0) / countQuery
        MapAt5 = (MapAt5 * 1.0) / countQuery
        MapAt1 = (MapAt1 * 1.0) / countQuery
        MapAt3 = (MapAt3 * 1.0) / countQuery

        P_MAP = (P_MAP * 1.0) / countQuery
        P_MapAt5 = (P_MapAt5 * 1.0) / countQuery
        P_MapAt1 = (P_MapAt1 * 1.0) / countQuery
        P_MapAt3 = (P_MapAt3 * 1.0) / countQuery

    f.write(str(MapAt1) + "\t" + str(MapAt3) + "\t" + str(MapAt5) + "\t" + str(MAP) + "\t" + str(P_MapAt1) + "\t" + str(
        P_MapAt3) + "\t" + str(P_MapAt5) + "\t" + str(P_MAP) + "\n")
    print(str(MapAt1) + "\t" + str(MapAt3) + "\t" + str(MapAt5) + "\t" + str(MAP) + "\t" + str(P_MapAt1) + "\t" + str(
        P_MapAt3) + "\t" + str(P_MapAt5) + "\t" + str(P_MAP) + "\n")


print "done"
if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)