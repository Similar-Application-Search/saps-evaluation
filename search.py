import numpy
import time
import sys, json
import MySQLdb



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

def queryProjectFromDB(tablename, index):
	db = MySQLdb.connect(
	    'localhost',
	    'root',
	    'passw0rd',
		'saps'
	)
	cursor = db.cursor()
	query = ''
	if tablename == 'testprojects':
		query = 'SELECT * from testprojects WHERE id=%s'
		cursor.execute(query, (str(index)))
	elif tablename == 'candidateprojects':
		query = 'SELECT * from candidateprojects WHERE id=%s' % (str(index))
		cursor.execute(query)
	else:
		return
	data = cursor.fetchone()
	if not data: return None
	desc = cursor.description
	dictionary = {}
	for (name, value) in zip(desc, data):
		dictionary[name[0]] = value
	cursor.close()
	db.close()
	return dictionary




def runevaluation(queryindex, description_matrix,readme_matrix,methodclass_matrix,packageclass_matrix,importpackage_matrix,weight_description,weight_readme,weight_methodclass,weight_packageclass,weight_importpackage,querycategory,candidatecategory,category_stats):

    #query_description_path = "./data/testProjectDetails.txt"
    # candidate_description_path = "./data/trainProjectDetails.txt"

    #query_giturl_path = "./data/testProjectGitURL.txt"
    # candidate_giturl_path = "./data/trainProjectGitURL.txt"

    #query_project_name_des, query_description = readProjectDetails(query_description_path)
    # candidate_project_name_des, candidate_description = readProjectDetails(candidate_description_path)

    #query_project_name_giturl, query_giturl = readProjectDetails(query_giturl_path)
    # candidate_project_name_giturl, candidate_giturl = readProjectDetails(candidate_giturl_path)

    MAP = 0
    MapAt5 = 0
    MapAt1 = 0
    MapAt3 = 0

    P_MAP = 0
    P_MapAt5 = 0
    P_MapAt1 = 0
    P_MapAt3 = 0

    countQuery = 0

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
        if numpy.isnan(importpackage_matrix[queryindex][candidate_index]):
            importpackage_val = 2  # infinite
        else:
            importpackage_val = importpackage_matrix[queryindex][candidate_index]
        '''
        weight_description = 0.1
        weight_readme = 0.6
        weight_methodclass = 0.2
        weight_packageclass = 0.2
        weight_importpackage = 0.1
        '''
        hybrid_distance = (weight_description * des_val) + (weight_readme * readme_val) + (
            weight_methodclass * methodclass_val) + (weight_packageclass * packageclass_val) + (
                              weight_importpackage * importpackage_val)

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
    if totalCategoryRelevance > 0:
        countQuery = countQuery + 1  # include this query in the MAP calculation

	#read query project from database
    data = queryProjectFromDB('testprojects',queryindex+1)
    striped_desc = data['description'].replace(data['name'], "", 1).strip().replace("\n","")
    query_object={'index':queryindex,
		'name':data['name'],
		'url':data['url'].replace("\n",""),
		'description':striped_desc,
		'candidates':[]
	}

    for i in range(1, len(distances)):
        data = queryProjectFromDB('candidateprojects',distances[i][0]+1)
        striped_desc = data['description'].replace(data['name'], "", 1).strip().replace("\n", "")
        candidateObject = {
			'name': data['name'],
			'url': data['url'].replace("\n", ""),
			'description': striped_desc
		}
        query_object['candidates'].append(candidateObject)

        if (querycategory[queryindex] == candidatecategory[distances[i][0]]):
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
    totalCategoryRelevance_at_1 = min(1, true_relevane)
    if totalCategoryRelevance_at_1 > 0:
        avgpAt1 = (avgpAt1 * 1.0) / totalCategoryRelevance_at_1
        P_avgpAt1 = countRelavance_1 / 1.0
        P_MapAt1 = P_MapAt1 + P_avgpAt1
        MapAt1 = MapAt1 + avgpAt1

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

    return json.dumps(query_object)


def main(queryIndex):
    query_project_path = "./data/testProjectCategory.txt"
    candidate_project_path = "./data/trainProjectCategory.txt"



    description_path = "./data/description.txt"
    readme_path = "./data/readme.txt"
    methodclass_path = "./data/methodclass.txt"
    packageclass_path = "./data/packageclass.txt"
    importpackage_path = "./data/importpackage.txt"

    description_matrix = numpy.loadtxt(open(description_path, "rb"), delimiter=",")
    readme_matrix = numpy.loadtxt(open(readme_path, "rb"), delimiter=",")
    methodclass_matrix = numpy.loadtxt(open(methodclass_path, "rb"), delimiter=",")
    packageclass_matrix = numpy.loadtxt(open(packageclass_path, "rb"), delimiter=",")
    importpackage_matrix = numpy.loadtxt(open(importpackage_path, "rb"), delimiter=",")

    query_project_name, querycategory = readProjectDetails(query_project_path)
    candidate_project_name, candidatecategory = readProjectDetails(candidate_project_path)




    learning_matrix = []


    weight_description=0.2
    weight_readme=0.2
    weight_methodclass=0.2
    weight_packageclass=0.2
    weight_importpackage=0.2

    category_stats = {}
    with open(candidate_project_path) as fc:
        for line in fc:
            pname, pcategory = line.split("\t")
            pcategory = pcategory.replace("\n", "")
            count_key = category_stats.get(pcategory, 0)  # if not found will return zero
            category_stats[pcategory] = int(count_key) + 1

    weight_description=0.4
    weight_readme=0.4
    weight_methodclass=0.1
    weight_packageclass=0.1
    weight_importpackage=0.1
    return runevaluation(queryIndex,description_matrix, readme_matrix, methodclass_matrix, packageclass_matrix, importpackage_matrix,
                  weight_description, weight_readme, weight_methodclass, weight_packageclass, weight_importpackage,
                  querycategory, candidatecategory, category_stats)



if __name__ == "__main__":
    start = time.time()
    print main(int(sys.argv[1]))
    sys.stdout.flush()
