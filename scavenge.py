from __future__ import division
from characterClasses import *
from functions import *
from skillCombat import *
from hunting import Huntable
from random import randrange
import math

#SC = Survival Check result
#Degraded Food is poisonous 50 - (SC * 5)% of the time
#	Poisonous food adds 1 SP at SC:1, 2 at SC:-1, or 3 at SC:-3
#	If the food is good, it is always -1 SP
#Dropped Items should be randomized the same way end of thread items are
#Fruits are one, two, three, or four meals depending on SC
#	They have they are poisonous 25 - (SC * 5)% of the time
#	And have a +1 SP rating if they are
#Transformation Items do not affect SP
#Plants are always poisonous and add 2, 3, or 4 SP depending on SC
#Corpses are useful for pelt

#At some point, the transformation items found should be Purified
#Purified items do not increase corruption, do not transform you, and can affect anyone regardless of home city

results = {
	#Degraded Food, Dropped Items, Fruits, Transformations, Plants, Corpses, Nothing
	-5:[0,0,0,0,65,0,35],
	-3:[15,0,0,0,50,0,35],
	-1:[15,0,25,5,20,0,35],
	1:[10,0,50,15,0,0,25],
	3:[0,0,50,30,0,20,0],
	5:[0,5,50,30,0,15,0]
}

freq = {"Small":5,"Medium":3,"Large":2,"Inedible":1}

dcs = {
	"Forest": 10,
	"Desert": 18,
	"Plains": 13,
	"Swamp": 15,
	"Tundra": 20,
	"Mountains": 15,
	"Lake": 10,
	"Island": 25,
	"Jungle": 25,
	"High Mountains": 30,
	"Bog": 30,
	"Ice Floes": 35
}

transform = {
	"Plains": ["Horse", "Kangaroo", "Raccoon"],
	"Lake": ["Bee","Mouse","Horse"],
	"Forest": ["Cat","Rabbit","Bee"],
	"Desert": ["Snake","Kangaroo","Rabbit"],
	"Jungle": ["Bee","Fox","Raccoon"],
	"Mountains": ["Cat","Mouse","Spider"],
	"High Mountains": ["Wolf","Bear","Fox"],
	"Swamp": ["Spider","Mouse","Snake"],
	"Bog": ["Rabbit","Spider","Snake"],
	"Tundra": ["Wolf","Bear","Fox"],
	"Island": ["Raccoon","Kangaroo","Horse"],
	"Ice Floes": ["Wolf","Bear","Cat"]
}

transText = {
	"Spider":"an aranium berry",
	"Bee":"a bottle of golden honey",
	"Snake":"a vial of vipera oil",
	"Bear":"an ursu fruit",
	"Horse":"an equidae potion",
	"Wolf":"a vial of lupus mutatio",
	"Fox":"a bottle of vixen's elixir",
	"Cat":"a felis berry",
	"Kangaroo":"a bottle of kangaroo milk",
	"Raccoon":"a masked fig",
	"Rabbit":"a bottle of carrot elixir",
	"Mouse":"a furry peach"
}

#Lower Tier Areas can't roll the extremes. -5 and +5 SC results are set to -3 and +3
lower = ["Forest","Desert","Plains","Tundra","Mountains","Lake","Swamp"]
def main(argv):
	characterData = readInJSON('peopleJSON.txt')
	p = "Lincoln Hale"
	l = "Plains"
	player = Character(p, **characterData[p])
	
	diff = dcs[l]
#Scavenge Check
	scavenge, successes = runSkillCheck(player, 'Scavenge', diff, True)
	print "Scavenge Skill", player.skills["Scavenge"]
	print "Difficulty:", diff
	print "Results:", successes
	print
	if abs(scavenge) > 3 and l in lower:
		scavenge -= math.copysign(2, scavenge)
	r = randrange(1,101)
	array = results[scavenge]
	total = array[0]
	count = 0
	
	#print scavenge, r, array
	while r > total:
		count += 1
		total += array[count]
	
	kChk = False
	kChk2 = False
	poison = False
	value = 0
	sp = 0
	if count == 0:
		text = " found some old rotting fruit"
		poison = randrange(1,101) <= (50 - scavenge*5)
		sp = 3-(scavenge+3)/2 if poison else -1
		kChk = True
	elif count == 1:
		text = " found a discarded item"
	elif count == 2:
		text = " found some ripe food"
		poison = randrange(1,101) <= (25 - scavenge*5)
		sp = -1*(scavenge+3)/2 if not poison else 1
		kChk = True
	elif count == 3:
		item = transform[l][randrange(0,3)]
		text = transText[item]
		text = " found " + text
		value = 5
		kChk2 = True
	elif count == 4:
		text = " found some interesting plant life"
		poison = True
		kChk = True
		sp = int(3-(scavenge+3)/2)
	elif count == 5:
		#Randomize an animal here
		animal = getAnimal(l)
		text = " found a rotting " + animal.name + " corpse.\nThe meat is worthless, but the pelt might be salvaged"
		#A second scavenge check should be done to determine how much pelt is harvested
		#This check is harder because to even get here, the original scavenge must be at least a +3
		value = animal.Pelt
		chk2, suc = runSkillCheck(player, "Scavenge", 40 - 5*scavenge, True)
		print "Scavenge Skill", player.skills["Scavenge"]
		print "Difficulty:", str(40-5*scavenge)
		print "Results:", successes
		print
		if suc > 0:
			print player.name + " managed to peel some of the pelt away"
		else:
			print player.name + " struggles at collecting pelt from the rotting " + animal.name
		
		
		chk2 += 5
		value *= chk2
		value /= 12
		value = int(value)
		text += "\n" + str(value) + " pieces of pelt were salvaged"
		value *= 5 #Convert to gems
	else:
		text = " couldn't find anything"
#Knowledge Check to Identify Item
	if kChk:
		know, successes = runSkillCheck(player, "Knowledge", 25 - 5*scavenge, True)
		print "Knowledge Skill", player.skills["Knowledge"]
		print "Difficulty:", str(25-5*scavenge)
		print "Results:", successes
		print
		
		if know > 0:
			text += ", and knows it is "
			text += "edible" if not poison else "poisonous"
		else:
			text += ", and thinks it is "
			text += "edible" if randrange(1,3) == 1 else "poisonous"
			text += "\nIt is in fact "
			text += "edible." if not poison else "poisonous"
			
	if kChk2:
		know, successes = runSkillCheck(player, "Knowledge", 25 - 5*scavenge, True)
		print "Knowledge Skill", player.skills["Knowledge"]
		print "Difficulty:", str(25-5*scavenge)
		print "Results:", successes
		print
		
		if know > 0:
			text += "\nAnd knows it might change him/her"
			if know == 5:
				text += " to be more like a " + item
			else:
				text += ", but doesn't know how"
		else:
			text += ", but doesn't realize its true nature"

	print p + text
	print "The find has a value of " + str(value) + " gems,",
	sp = int(sp)
	if sp > 0:
		print "and adds {0} SP if consumed".format(sp)
	elif sp < 0:
		print "and removes {0} SP if consumed".format(abs(sp))
	elif kChk2:
		print "and removes some amount of SP if consumed"
	else:
		print "and cannot be eaten"
#Tell Roleplayer Truth and what their character thinks
#See picture on phone for distribution of scavenged things
#Poisoned food adds SP instead of taking them away
#Transformation Items give variable amounts based on their effect; figure this out when consumed

def getAnimal(location):
	animalList = {}
	npcData = readInJSON('npcJSON.txt')
	for i, c in npcData.iteritems():
		name = i.split("-")[0]
		if c["Type"] == "Fish":
			continue
		if c["Class"] == "Animal":
			animalList[name] = Huntable(name, **c)
	
	options = []
	for c in animalList.itervalues():
		if location in c.Locations:
			k = freq[c.Type]
			for i in range(k):
				options.append(c)
	#print options
	return options[randrange(0,len(options))]
			
#Make sure this is the main file being run
if __name__ == "__main__":
	main(sys.argv)