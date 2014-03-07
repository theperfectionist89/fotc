from __future__ import division
import io, sys, json, traceback, itertools, multiprocessing

sortValues = {}
sortings = {}
people = list()
sortingHeaders = []
finalData = {}
sortingAvgs = {'N':14,'VL':24,'L':36,'BA':49,'A':59,'AA':68,'H':81, 'VH':93,'E':103}
stats = ["STR","TGH","SPE","INT","SPI","CHA","LST","CRP"]
sortingData = {}
desired = {}

def readSortingData(data):
	try:
		global sortingData
		with io.open(data, 'r') as file:
			sortingData = convert(json.load(file))
		
	except:
		traceback.print_exc(file=sys.stdout)
		
def setupResponses(responses):
	input = None
	with io.open(responses,'r') as file:
		input = file.read().split()
	x = 0
	size = 8+13
	global people, sortings
	while x<len(input):
		if not convert(input[x])[0] == "#":
			people.append(input[x])
			sortings[input[x]] = input[x+1:x+size]
		x += size
	people = convert(people)
	sortings = convert(sortings)

def innerSort(q,answers, val, sortingData, desired):
	closestValues = None
	closestDifference = sys.maxint
	closestAnswers = None
	questRange = range(12)
	for check in itertools.product(
		answers[0][val],answers[1],answers[2],answers[3],answers[4],answers[5],
		answers[6],answers[7],answers[8],answers[9],answers[10],answers[11]):
		curValues = {}
		for stat in stats:
			curValues[stat] = 0
		for i in questRange:
			for stat in stats:
				curValues[stat] += sortingData[str(i+1)][check[i]][stat]
		val = calcDeviation(curValues,desired)
		if val < closestDifference:
			closestDifference = val
			closestValues = curValues
			closestAnswers = check
	q.put([closestDifference,closestAnswers,closestValues])
	
def sort(answers):
	global desired
	desired = {
		"STR":sortingAvgs[answers[12]],
		"TGH":sortingAvgs[answers[13]],
		"SPE":sortingAvgs[answers[14]],
		"INT":sortingAvgs[answers[15]],
		"SPI":sortingAvgs[answers[16]],
		"CHA":sortingAvgs[answers[17]],
		"LST":sortingAvgs[answers[18]],
		"CRP":sortingAvgs[answers[19]],
	}
	
	
	q = multiprocessing.Queue()
	processes = list()
	running = multiprocessing.Value('i',len(answers[0]))
	for i in range(len(answers[0])):
		p = multiprocessing.Process(target = innerSort, args = (q, answers,i,sortingData,desired))
		processes.append(p)
		p.start()
	for i in range(len(answers[0])):
		processes[i].join()
	
	closestValues = None
	closestDifference = sys.maxint
	closestAnswers = None
	
	while(not q.empty()):
		data = q.get()
		if data[0] < closestDifference:
			closestDifference = data[0]
			closestAnswers = data[1]
			closestValues = data[2]	
	
	printData(closestAnswers, closestValues, closestDifference)
	return closestAnswers

def printData(chosenAnswers, statValues, deviation):
	for i in range(12):
		print str(i+1)+"."+chosenAnswers[i]+" ",
	print ""
	for stat in stats:
		print stat+":"+str(statValues[stat])+" ",
	print "- " + str(deviation)
	print "----------------------------------"
	
def calcDeviation( values1, values2):
	avg = 0
	for h in stats:
		v = values1[h]-values2[h]
		v = v**2
		v = v / len(stats)
		avg += v
	
	avg = avg ** (1/2)
	return avg
		
	
def main(argv):
	readSortingData('SortingDataJSON.txt')
	setupResponses('Sorts.txt')
	
	for p in people:
		print p
		sort(sortings[p])

#convert dictionary/list of unicode to string
def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
		
#Make sure this is the main file being run
if __name__ == "__main__":
	main(sys.argv)
	
