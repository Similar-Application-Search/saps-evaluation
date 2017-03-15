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

def insert_project(cursor, table, name, description, url, category, language):
	query = ''
	if table == 'test':
		query = "INSERT INTO testprojects(name,description,url,category,language) " \
	            "VALUES(%s,%s,%s,%s,%s)"
	elif table == 'candidate':
		query = "INSERT INTO candidateprojects(name,description,url,category,language) " \
	            "VALUES(%s,%s,%s,%s,%s)"
	args = (name, description, url, category, language)
 	cursor.execute(query, args)


def create_ratings_table():
	check_table = "SELECT 1 FROM ratings LIMIT 1"
	# check if the table exists or not

	create_table = """CREATE TABLE ratings (
	  user_id INT UNSIGNED NOT NULL,
	  test_proj_id INT UNSIGNED NOT NULL,
	  candidate_proj_id INT UNSIGNED NOT NULL,
	  PRIMARY KEY pk_ratings(user_id, test_proj_id, candidate_proj_id)
	) ENGINE=MyISAM"""
	try:
	    cursor.execute(check_table)
	except:
	    cursor.execute(create_table)
	else:
	    pass

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
  category varchar(1024) NOT NULL,
  language varchar(1024) NOT NULL,
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
  category varchar(1024) NOT NULL,
  language varchar(1024) NOT NULL,
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
query_category_path = "./data/testProjectCategory.txt"
query_language_path = "./data/testProjectLanguage.txt"
# load candidate data from files into database
candidate_description_path = "./data/trainProjectDetails.txt"
candidate_giturl_path = "./data/trainProjectGitURL.txt"
candidate_category_path = "./data/trainProjectCategory.txt"
candidate_language_path = "./data/trainProjectLanguage.txt"



query_project_name_des, query_description = readProjectDetails(query_description_path)
query_project_name_giturl, query_giturl = readProjectDetails(query_giturl_path)
query_project_name_category, query_category = readProjectDetails(query_category_path)
query_project_name_language, query_language = readProjectDetails(query_language_path)

candidate_project_name_des, candidate_description = readProjectDetails(candidate_description_path)
candidate_project_name_giturl, candidate_giturl = readProjectDetails(candidate_giturl_path)
candidate_project_name_category, candidate_category = readProjectDetails(candidate_category_path)
candidate_project_name_language, candidate_language = readProjectDetails(candidate_language_path)


for i in range(len(query_project_name_des)):
	name = query_project_name_des[i]
	description = query_description[i]
	url = query_giturl[i]
	category = query_category[i]
	language = query_language[i]
	insert_project(cursor, 'test', name, description, url, category, language)

for i in range(len(candidate_project_name_des)):
	name = candidate_project_name_des[i]
	description = candidate_description[i]
	url = candidate_giturl[i]
	category = candidate_category[i]
	language = candidate_language[i]
	insert_project(cursor, 'candidate', name, description, url, category, language)


cursor.close()
db.close()
