import io, sys
from pprint import pprint
from copy import deepcopy
from functions import *
from characterClasses import Character

#peopleStats = ['Name','Creature','Class','Hidden','City','LVL','EXP','HP','STR','TGH','SPE','INT','SPI','CHA','LST','CRP']
cityStats = ['Name', 'Ban1', 'Ban2', 'Ban3', 'Ban4', 'Stat1', 'Stat2', 'Banned']
classStats = ['Name', 'Stat1', 'Stat2']
singleReq = [35, 65, 95, 125]
doubleReq = [25, 45, 65, 85]
powerLevels = {"Alpha":4,"Beta":3,"Omega":2}
cities = []
powers = []
global people
people = {}
classes = []

def fillPowers(powerList):
	for p in powerList:
		array = p.split(" | ")
		powers.append({'Name':array[0], 'Users': array[1].split(', '), 'Type':array[2],	'Stat1':array[3],
			'Stat2':array[4], 'Single':(array[3] == array[4]), 'Codes':splitChunks(array[5]), 'Level': ""})

def getPowerLevel(code):
	for p in powers:
		if code in p['Codes']:
			p["Level"] = p['Codes'].index(code)+1
			return deepcopy(p)
	return "Missing"
	
def fillPeople(peopleList):
	for name in peopleList.iterkeys():
		people[name] = {}
		for k, v in peopleList[name].iteritems():
			people[name][k] = v
			
		people[name]['Name'] = name
		people[name]['CRP'] = peopleList[name]['Corruption']
		people[name]['LST'] = peopleList[name]['Lust']
		del people[name]['Corruption']
		del people[name]['Lust']
		people[name]['Perks'] = splitChunks(peopleList[name]['Perks'])
		people[name]['PowerLevels'] = []
		for code in splitChunks(peopleList[name]['Powers']):
			people[name]['PowerLevels'].append(getPowerLevel(code))
	
def printPerson(input):
	if type(input) is dict:
		person = input
	else:
		person = people[input]
	
	print person["Name"]
	print '{Class} ({Hidden}) from {City}\nLevel {Level}'.format(**person)
	print 'STR:{STR} TGH:{TGH} SPE:{SPE}\nINT:{INT} SPI:{SPI} CHA:{CHA}'.format(**person)
	'HP:{MaxHP} LST:{MaxLust} CRP:{CRP}'.format(**person)

	print "Powers:"
	for p in person["PowerLevels"]:
		printPeoplePower(p)
	print '\n'
	
def printPeoplePower(power):
	print '{Name} {Level}'.format(**power)
	
def printPower(power):
	print '{Name} {Level}\n{Type} - {Stat1}/{Stat2}\n'.format(**power)	
	
def banCheck(city, power):
	banned = city['Banned'] == power["Stat1"] or city['Banned'] == power["Stat2"]
	safe = city['Stat1'] == power["Stat1"] or city['Stat2'] == power["Stat2"]
	safe = safe or city['Stat2'] == power["Stat1"] or city['Stat1'] == power["Stat2"]
	return banned and (not safe)
	
def creatureCheck(creature, users):
	banned = True
	for u in users:
		if u == creature or u == "Any":
			banned = False
		elif u == "Creatures, Morphs" and creature != "Human":
			banned = False
	return banned
	
def levelCheck(power):
	#Check if a power has another level to grow into
	level = power["Level"]
	cap = powerLevels[power["Type"]]
	if level < cap:
		return level + 1
	else: 
		return -1
	
def getEligiblePowers(person):
	city = findById(cities, 'Name', person['City'])
	cls = findById(classes, 'Name', person['Hidden']) #Hidden Class unlocks Powers
	eligible = []

	'''
	Iterate over powers
	For each, check if they already have it
	Remove it from the list if they do
	Then add its upgrade if they qualify
	If they don't have it, set it to level 1
	And check if they qualify
	'''
	
	for power in powers:
		if banCheck(city, power):
			continue
		if creatureCheck(person['Creature'], power['Users']):
			continue
		s1 = int(person[power['Stat1']])
		s2 = int(person[power['Stat2']])
		
		owned = findById(person["PowerLevels"], 'Name', power['Name'])
		if type(owned) is dict:
			level = levelCheck(owned)
			if level == -1:
				continue
		else:
			level = 1
			
		power["Level"] = level
			
		if power['Stat1'] == cls['Stat1'] and power['Stat2'] == cls['Stat2']:
			eligible.append(deepcopy(power))
		elif power['Stat2'] == cls['Stat1'] and power['Stat1'] == cls['Stat2']:
			eligible.append(deepcopy(power))
		else:
			if power['Single'] is True:
				value = singleReq[level-1]
			else:
				value = doubleReq[level-1]
				
			if s1 >= value and s2 >= value:
				eligible.append(power)
			
	return eligible
	
def checkEligible(name):
	el = getEligiblePowers(people[name])
	print "Powers " + name + " is Eligible For:"
	for e in el:
		printPower(e)
	print '\n'
		
def getData():
	powerText = readIn("powersPython.txt", '\n')
	fillPowers(powerText)
	peopleText = readInJSON("peopleJSON.txt")
	fillPeople(peopleText)
	cityText = readIn("cities.txt", '\n')
	fillList(cityText, cityStats, cities)
	classText = readIn("classes.txt", '\n')
	fillList(classText, classStats, classes)
	
def levelUpPowers(players):
	for p in players:
		printPerson(p)
		checkEligible(p)
		
def main(args):
	getData()
	levelUpPowers(['Lincoln Hale'])
	
#Make sure this is the main file being run
if __name__ == "__main__":
	main(sys.argv)
