from characterClasses import *
from random import randrange
import sys
class SkillCharacter(Character):
	def __init__(self, name, **charStuff):
		self.populate(charStuff, name) #fill old values
		self.skills = {}
	def getSkill(name):
		skl = __import__('skillClasses')
		try:
			self.skills[name] = getattr(skl,name)()
		except:
			print "We don't have that skill yet: " + name

def roller():
	die = 2
	sides = 6
	sum = 0
	for i in range(die):
		sum += randrange(1,sides+1)
	return sum
			
def main(argv):
	characterData = readInJSON('peopleJSON.txt')
	
	p1 = "Lincoln Hale"
	p2 = "Gwendolyn Janusdottir"

	player1 = getCharacter(p1)
	player2 = getCharacter(p2)
	
	print runSkillCheck(player1, "Carry", 13)
	print runSkillCheck(player2, "Carry", 33)
	
	#print player1.skills
	#print player2.skills
	#print runSkillCombat(player1,"Charm",player2, "Charm")
	#runSkillCombat(player1, player2)

def runSkillCombat(p1, s1, p2, s2):
	val = 0
	for i in range(0,7):
		#Player 1 Wins on Tie - Remember this!
		if p1.skills[s1]+roller()>=p2.skills[s2]+roller():
			val+=1
		else:
			val-=1
		if abs(val)>4:
			break
	return val
def runSkillCheck(p1, skill, dc, display=False):
	array = []
	val = 0
	for i in range(0,7):
		roll = p1.skills[skill]+roller()
		array.append("Pass" if roll >= dc else "Fail")
		if roll >= dc:
			val+=1
		else:
			val-=1
		if abs(val)>4:
			break
	if display:
		return val, array
	else:
		return val
	
#Make sure this is the main file being run
if __name__ == "__main__":
	main(sys.argv)