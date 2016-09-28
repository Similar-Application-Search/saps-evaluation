import numpy
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

def main():
    query_project_path = "./data/testProjectCategory.txt"
    candidate_project_path = "./data/trainProjectCategory.txt"

    description_path = "./data/description.txt"
    readme_path = "./data/readme.txt"
    methodclass_path = "./data/methodclass.txt"
    packageclass_path = "./data/package_class.txt"
    importpackage_path = "./data/importpackage.txt"

    description_matrix = numpy.loadtxt(open(description_path, "rb"), delimiter=",")
    readme_matrix = numpy.loadtxt(open(readme_path, "rb"), delimiter=",")
    methodclass_matrix = numpy.loadtxt(open(methodclass_path, "rb"), delimiter=",")
    packageclass_matrix = numpy.loadtxt(open(packageclass_path, "rb"), delimiter=",")
    importpackage_matrix = numpy.loadtxt(open(importpackage_path, "rb"), delimiter=",")

    query_project_name, querycategory = readProjectDetails(query_project_path)
    candidate_project_name, candidatecategory = readProjectDetails(candidate_project_path)
    learning_matrix = []
    f = open("learning_matrix.txt", "w")
    #len(querycategory)
    for queryindex in range(0, 15):
        matrix_entry = []
        for candidate_index in range(1, len(candidatecategory)):#skip very first element ,as it is 0 valued
            flag = 0
            if querycategory[queryindex] == candidatecategory[candidate_index] :
                flag =1
            if numpy.isnan(description_matrix[queryindex][candidate_index]) :
                des_val = 2#infinite
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
            matrix_entry.append(des_val)
            matrix_entry.append(readme_val)
            matrix_entry.append(methodclass_val)
            matrix_entry.append(packageclass_val)
            matrix_entry.append(importpackage_val)
            matrix_entry.append(flag)

            #f.write(str(des_val)+","+str(readme_val)+","+str(methodclass_val)+","+str(packageclass_val)+","+str(flag)+"\n")
            f.write(str(flag) + " qid:"+str(queryindex)+" 1:"+str(des_val) + " 2:" + str(readme_val) + " 3:" + str(methodclass_val) + " 4:" + str(
                packageclass_val)+ " 5:" + str(importpackage_val)+ "\n")

            #learning_matrix.append(matrix_entry)
    #print "learning matrix is\n"
    #print learning_matrix
    #numpy.savetxt("learning_matrix.csv", learning_matrix, delimiter=",")
    print "done"
if __name__ == "__main__":
    main()