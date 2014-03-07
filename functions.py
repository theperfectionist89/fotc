import io, json, re
from copy import deepcopy

def readIn(file, s):
	f = open(file, 'r')
	text = f.read()
	stored = text.split(s)
	f.close()
	return stored
	
def splitChunks(string):
	return re.findall('..',string)
	
def addSpacing(string):
	return ' '.join(re.findall('[A-Z]+[a-z]*',string))
	
def removeSpacing(string):
	return re.sub(' ','',string)

def fillList(lst, names, toFill):
	for c in lst:
		array = c.split("|")
		temp = {}
		for i in range(0, len(names)):
			temp[names[i]] = array[i]
		toFill.append(deepcopy(temp))		
	
def findById(array, key, value):
	for k in array:
		if k[key] == value:
			return k
	return 0
	
def readInJSON(input):
	with io.open(input, 'r') as file:
		return convert(json.load(file))
	
def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input