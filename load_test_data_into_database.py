import MySQLdb

def create_users_table():
	check_table = "SELECT 1 FROM users LIMIT 1"
	# check if the table exists or not

	create_table = """CREATE TABLE users (
	  id int NOT NULL AUTO_INCREMENT,
	  email varchar(255) NOT NULL UNIQUE,
	  username varchar(255) NOT NULL,
	  PRIMARY KEY (id)
	) ENGINE=MyISAM"""
	drop_table = "Drop TABLE users"
	try:
	    cursor.execute(check_table)
	except:
	    cursor.execute(create_table)
	else:
	    pass



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

def insert_project(cursor, table, name, description, url):
	query = ''
	if table == 'test':
		query = "INSERT INTO testprojects(name,description,url) " \
	            "VALUES(%s,%s,%s)"
	elif table == 'candidate':
		query = "INSERT INTO candidateprojects(name,description,url) " \
	            "VALUES(%s,%s,%s)"
	args = (name, description, url)
 	cursor.execute(query, args)


db = MySQLdb.connect(
    'localhost',
    'root',
    'passw0rd'
)


cursor = db.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS saps')
cursor.execute('USE saps')

check_table = "SELECT 1 FROM testprojects LIMIT 1"
# check if the table exists or not

create_table = """CREATE TABLE testprojects (
  id int NOT NULL AUTO_INCREMENT,
  name varchar(255) NOT NULL,
  description varchar(1024) NOT NULL,
  url varchar(1024) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=MyISAM"""
drop_table = "Drop TABLE testprojects"
try:
    cursor.execute(check_table)
except:
    cursor.execute(create_table)
else:
    cursor.execute(drop_table)
    cursor.execute(create_table)


check_table = "SELECT 1 FROM candidateprojects LIMIT 1"
# check if the table exists or not

create_table = """CREATE TABLE candidateprojects (
  id int NOT NULL AUTO_INCREMENT,
  name varchar(255) NOT NULL,
  description varchar(1024) NOT NULL,
  url varchar(1024) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=MyISAM"""
drop_table = "Drop TABLE candidateprojects"
try:
    cursor.execute(check_table)
except:
    cursor.execute(create_table)
else:
    cursor.execute(drop_table)
    cursor.execute(create_table)

# create users table if not created
create_users_table()

# load test data from files into database
query_description_path = "./data/testProjectDetails.txt"
query_giturl_path = "./data/testProjectGitURL.txt"
# load candidate data from files into database
candidate_description_path = "./data/trainProjectDetails.txt"
candidate_giturl_path = "./data/trainProjectGitURL.txt"


query_project_name_des, query_description = readProjectDetails(query_description_path)
query_project_name_giturl, query_giturl = readProjectDetails(query_giturl_path)

candidate_project_name_des, candidate_description = readProjectDetails(candidate_description_path)
candidate_project_name_giturl, candidate_giturl = readProjectDetails(candidate_giturl_path)

for i in range(len(query_project_name_des)):
	name = query_project_name_des[i]
	description = query_description[i]
	url = query_giturl[i]
	insert_project(cursor, 'test', name, description, url)

for i in range(len(candidate_project_name_des)):
	name = candidate_project_name_des[i]
	description = candidate_description[i]
	url = candidate_giturl[i]
	# print (name,description,url)
	insert_project(cursor, 'candidate', name, description, url)


cursor.close()
db.close()
