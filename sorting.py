from __future__ import division
import io, sys, copy

sortValues = {}
sortings = {}
people = list()
sortingHeaders = []
finalData = {}
sortingAvgs = {'N':14,'VL':24,'L':36,'BA':49,'A':59,'AA':68,'H':81, 'VH':93,'E':103}


def readIn(file):
	f = open(file, 'r')
	text = f.read()
	stored = text.split()
	f.close()
	return stored
	
def setup(data, responses):
	input = readIn(data)
	inputR = readIn(responses)
	x = 0
	
	while x < len(inputR):
		size = 8+13
		people.append(inputR[x])
		sortings[inputR[x]] = inputR[x+1:x+size]
		x += size
	
	global sortingHeaders
	sortingHeaders = input[1:9]
	sortingNumbers = input[9::9]
	sortingData = list()
	for i in range(0,12*6):
		sortingData.append(input[10+9*i:18+9*i])

	for i in range(0,12):
		for n in range(0,6):
			for k in range(0,8):
				lookup = sortingHeaders[k] + '-' + sortingNumbers[i*6+n]
				sortValues[lookup] = sortingData[i*6+n][k]

def sort(person, data):
	values = {}
	valuesD = {}
	responses = data[0:12]
	desired = data[12:]
	trials = 1
	count = 0
	
	for i, s in enumerate(responses):
		trials *= len(s)
		
	for i, h in enumerate(sortingHeaders):
		valuesD[h] = sortingAvgs[desired[i]]
		
	for i, r in enumerate(responses):
		l = len(r)
		if l == 1:
			responses[i] = [r] * trials
		else: 
			temp = list()
			for p in range(0, trials):
				m = (p // l**count) % l
				temp.append(r[m])
			responses[i] = temp
			count += 1
	
	for n in range(0, trials):
		currentResponses = list()
		for h in sortingHeaders:
			values[h] = 0
		
		for i, r in enumerate(responses):
			currentResponses.append(r[n])
			for h in sortingHeaders:
				values[h] += int(sortValues[h + '-' + str(i+1) + r[n]])
			
		score = calcDeviation(values, valuesD)
				
		if trials < 10 and trials > 1:
			printData(values, score)
		
		finalData[person + "Trial" + str(n)] = currentResponses
		finalData[person + "Trial" + str(n) + "Values"] = copy.deepcopy(values)
		finalData[person + "Trial" + str(n) + "Score"] = score
		
	print trials
	return evaluate(person, trials) #(PERSON, TRIALS)

def evaluate(person, trials):
	minimum = finalData[person + "Trial0Score"]
	best = finalData[person + "Trial0"]
	values = finalData[person + "Trial0Values"]
	
	for i in range(1, trials):
		m = finalData[person + "Trial" + str(i) + "Score"] 
		if m < minimum:
			minimum = m
			best = finalData[person + "Trial" + str(i)]
			values = finalData[person + "Trial" + str(i) + "Values"]
			
	return {'set': best, 'values': values, 'score': minimum}
	
def printData(values, score):
	print 'STR:{STR} TGH:{TGH} SPE:{SPE} INT:{INT} SPI:{SPI} CHA:{CHA} LST:{LST} CRP:{CRP}'.format(**values),
	print '- {:4.2f}'.format(score)
	print ''
	
def calcDeviation(values, valuesD):
	avg = 0
	n = len(sortingHeaders)
	
	for h in sortingHeaders:
		v = values[h] - valuesD[h]
		v = v ** 2
		v = v / n
		avg += v
		
	avg = avg ** (1/2)
	
	return avg

def roundOff(x, base=5):
	return int(base * round(float(x)/base))
		
def main(argv):
	setup('SortingData.txt', 'Sorts.txt')
	for p in people:
		if p[0]=="#":
			continue
		print p
		best = sort(p, sortings[p])
		for i in range(0, 12):
			print str(i+1) + "." + best['set'][i] + " ",
		print ''
		printData(best['values'], best['score'])
		print '--------------------------------------------------'
	
#Make sure this is the main file being run
if __name__ == "__main__":
	main(sys.argv)
	