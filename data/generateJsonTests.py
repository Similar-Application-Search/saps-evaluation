import sys, json

inputfile = sys.argv[1]

queryoptions = [] #store names
for line in open(inputfile):
    lineArr = line.split()
    queryoptions.append(lineArr[0])
f = open("testProjectName.json", "w")
json.dump(queryoptions, f, indent=4)
f.close()
