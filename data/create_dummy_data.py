
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


'''
	create some dummy data for project main language
'''
dummy_languages = ['Java', 'Python', 'C++', "Objective-C", "Javascript"]
query_giturl_path = "testProjectGitURL.txt"
candidate_giturl_path = "trainProjectGitURL.txt"

query_f = open("testProjectLanguage.txt", "a")
candidate_f = open("trainProjectLanguage.txt", "a")

testProjectName = readProjectDetails(query_giturl_path)[0]
candidateProjectName = readProjectDetails(candidate_giturl_path)[0]

for i, name in enumerate(testProjectName):
    query_f.write(name + "\t" + dummy_languages[i%5] +"\n")
for i, name in enumerate(candidateProjectName):
    candidate_f.write(name + "\t" + dummy_languages[i%5]+ "\n")

query_f.close()
candidate_f.close()
