from __future__ import division
import io, sys, json, traceback, itertools

sortValues = {}
sortings = {}
people = list()
sortingHeaders = []
finalData = {}
sortingAvgs = {'N':14,'VL':24,'L':36,'BA':49,'A':59,'AA':68,'H':81, 'VH':93,'E':103}
stats = ["STR","TGH","SPE","INT","SPI","CHA","LST","CRP"]
sortingData = {}

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

def sort(person, answers):
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
	
	questRange = range(12)
	
	closestValues = None
	closestDifference = sys.maxint
	closestAnswers = None
	count = 0
	
	for check in itertools.product(
		answers[0],answers[1],answers[2],answers[3],answers[4],answers[5],
		answers[6],answers[7],answers[8],answers[9],answers[10],answers[11]):
		curValues = {}
		count += 1
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
	printData(closestAnswers, closestValues, closestDifference, count)
	return closestAnswers

def printData(chosenAnswers, statValues, deviation, count):
	print count
	for i in range(12):
		print str(i+1)+"."+chosenAnswers[i]+" ",
	print ""
	for stat in stats:
		print stat+":"+str(statValues[stat])+" ",
	print '- {:4.2f}'.format(deviation)
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
		sort(p,sortings[p])

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
	
