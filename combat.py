import io
from fotc import *

peopleStats = ['Name','Class','Hidden','City','LVL','EXP','HP','STR','TGH','SPE','INT','SPI', 'CHA','LST','CRP']
cityStats = ['Name', 'Ban1', 'Ban2', 'Ban3', 'Ban4', 'Stat1', 'Stat2', 'Banned']
classStats = ['Name', 'Stat1', 'Stat2']
singleReq = [35, 56, 77, 98]
doubleReq = [25, 40, 55, 70]
powerLevels = {"Alpha":4,"Beta":3,"Omega":2}
cities = []
powers = []
people = []
classes = []

def getCombatData():
	powerText = readIn("powersPython.txt", '\n')
	fillPowers(powerText, powers)
	peopleText = readIn("peoplePython.txt", '\n')
	fillPeople(peopleText, people)
	cityText = readIn("cities.txt", '\n')
	fillList(cityText, cityStats, cities)
	classText = readIn("classes.txt", '\n')
	fillList(classText, classStats, classes)
	
def main(args):
	getCombatData()
	print people

#Make sure this is the main file being run
if __name__ == "__main__":
	main(sys.argv)
