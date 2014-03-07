from __future__ import division
from characterClasses import *
from functions import *
from skillCombat import *
from random import randrange
from huntingAdvantages import *
import newCombat, sys

longplaces = {'P':'Plains','L':'Lake','I':'Island','F':'Forest','T':'Tundra','S':'Swamp','B':'Bog',
	'C':'Ice Floes','J':'Jungle','M':'Mountains','H':'High Mountains','D':'Desert'}
places = {
	"Ice Floes": {"Stealth":-2, "Perception":0, "Acrobatics":0, "Escape":0},
	"Lake": {"Stealth":0, "Perception":0, "Acrobatics":2, "Escape":0},
	"Island": {"Stealth":0, "Perception":0, "Acrobatics":0, "Escape":-2},
	"Mountains": {"Stealth":0, "Perception":-2, "Acrobatics":-2, "Escape":0},
	"High Mountains": {"Stealth":-2, "Perception":0, "Acrobatics":-2, "Escape":-2},
	"Swamp": {"Stealth":-2, "Perception":0, "Acrobatics":0, "Escape":0},
	"Bog": {"Stealth":0, "Perception":0, "Acrobatics":-2, "Escape":0},
	"Desert": {"Stealth":2, "Perception":2, "Acrobatics":0, "Escape":2},
	"Plains": {"Stealth":2, "Perception":2, "Acrobatics":0, "Escape":2},
	"Forest": {"Stealth":0, "Perception":-2, "Acrobatics":2, "Escape":0},
	"Jungle": {"Stealth":0, "Perception":-2, "Acrobatics":2, "Escape":0},
	"Tundra": {"Stealth":-2, "Perception":0, "Acrobatics":0, "Escape":-2},
}
startWeapons = {
	"Centaur":"Longbow",
	"Cyclops":"Greatclub"
}
victories = {
	"Kill": "With one more swing of {0}'s {2}, {1} lies lifeless on the ground. Your character has been killed.",
	"Rape": "The {0}, overcome by Lust, gives in to its desires. Your character is the victim of a brutal rape.",
	"Destroy": "The {0} is both enraged and aroused. After brutally raping {1} the {0} swings its {2}. Your character has been killed.",
	"Pillage": "Not content just to kill {1}, the {0} strips them of all his/her items first before driving its {2} into {1}'s heart.",
	"Assault": "{1} is not sure what is worse; blacking out while being raped by the {0}, or waking up to find all of his/her items gone",
	"Violate": "After stripping {1} of all of his/her items, the {0} pulls out an item and shoves it down {1}'s throat.",
	"Gavage": "A little on the sadistic side, the {0} takes an item from its pocket. It forces it down {1}'s throat.",
	"Burgle": "Some things in {1}'s inventory catch the {0}'s eye. All of your character's items have been stolen.",
	"Ravage": "As if being brutally raped by the {0} was not enough, {1} also has his/her mouth forced open and a mysterious item shoved into his/her mouth.",
	"None": "The {0} decides to leave {1} alone and walks away."
}

#Fish don't attack; fishing subset of hunting must be done differently
	
class Huntable(Character):
	personality = None
	personTraits = {}
	def __init__(self, name, **charStuff):
		super(Huntable,self).__init__(name, **charStuff)
		self.advantages = []
		self.Locations = list()
		loc = re.findall('.',self.Places)
		for l in loc:
			self.Locations.append(longplaces[l])
		#self.Creature = name
		if self.name in startWeapons.iterkeys():
			self.addAttack(startWeapons[self.name])
		
	def processPersonality(self):
		i = randrange(0,3)
		if i == 0:
			p = self.Strat1
		elif i == 1:
			p = self.Strat2
		else:
			p = self.Strat3
		self.setPersonality(p)
			
	def setPersonality(self, person):
		self.personality = person
		self.personTraits = npcStrategies[self.personality]
		if self.Creature != "Animal":
			self.getWeapons()
			self.getArmour()
		self.setAdvantage()
		self.changeStats()
		
	def changeStats(self):
		mod = 5 if self.Level < 10 else 10
		self.STR += mod if self.personTraits["StatUp"] == "STR" else 0 
		self.STR -= mod if self.personTraits["StatDown"] == "STR" else 0 
		self.TGH += mod if self.personTraits["StatUp"] == "TGH" else 0 
		self.TGH -= mod if self.personTraits["StatDown"] == "TGH" else 0 
		self.SPE += mod if self.personTraits["StatUp"] == "SPE" else 0 
		self.SPE -= mod if self.personTraits["StatDown"] == "SPE" else 0 
		self.INT += mod if self.personTraits["StatUp"] == "INT" else 0 
		self.INT -= mod if self.personTraits["StatDown"] == "INT" else 0 
		self.SPI += mod if self.personTraits["StatUp"] == "SPI" else 0 
		self.SPI -= mod if self.personTraits["StatDown"] == "SPI" else 0 
		self.CHA += mod if self.personTraits["StatUp"] == "CHA" else 0 
		self.CHA -= mod if self.personTraits["StatDown"] == "CHA" else 0 
		self.Lust += mod if self.personTraits["StatUp"] == "LST" else 0 
		self.Lust -= mod if self.personTraits["StatDown"] == "LST" else 0 

		self.levelUp(0)
		
	def setAdvantage(self):
		self.advantages = []
		module = __import__('huntingAdvantages')
		try:
			self.advantages.append(getattr(module, self.personTraits['Advantage'])())
		except:
			pass
			
	def getWeapons(self):
		tier = min(self.Level - (self.Level % 3),12)
		try:
			self.addAttack(self.personTraits['W'+str(tier)])
		except:
			pass
			
	def getArmour(self):
		tier = min(self.Level - (self.Level % 3),12)
		try:
			self.addArmour(self.personTraits['A'+str(tier)])
		except:
			pass
		
def getPrey(location, type = None, taboo = False):
	options = []
	for c in animalList.itervalues():
		if location in c.Locations:
			if type is None or c.Type in type:
				if not taboo or c.Creature != c.name:
					options.append(c)
	#print options
	select = options[randrange(0,len(options))]
	select.strategy.panicMode = True
	select.Creature = select.name
	select.processPersonality()
	try:
		select.strategy.runHealth = (select.personTraits["RunHP"] / 100)*select.MaxHP
		select.strategy.runLust = (select.personTraits["RunLust"] / 100)*select.MaxLust
	except:
		select.strategy.runHealth = 5
		
	return select

def main(argv):
	global animalList
	animalList = {}
	npcList = {}
	characterData = readInJSON('peopleJSON.txt')
	npcData = readInJSON('npcJSON.txt')
	for i, c in npcData.iteritems():
		name = i.split("-")[0]
		if c["Type"] == "Fish":
			continue
		if c["Class"] == "Animal":
			animalList[name] = Huntable(name, **c)
		else:
			npcList[name] = Huntable(name, **c)

	#Global Setup
	p = "Gwendolyn Janusdottir"
	l = "Plains"
	player = Character(p, **characterData[p])
	player.hasSkinningKnife = False
	player.hasTaboo = False
	player.advantages = []
	#player.advantages.append(Brutal())
	#player.advantages.append(Careless())
	player.advantages.append(CarefulHunter())
	#player.advantages.append(SwiftHunter())
	#player.advantages.append(LightStep())
	
	player.strategy.runHealth = 5
	player.strategy.runLust = 18
	player.strategy.panicMode = True
	player.strategy.patience = 1
	
	#player.addAttack("Fists")

	#player.currentLust = 0
	#player.currentHP = 21
	
	#Setup #1 - Hunting For Food
	t = ["Small"]
	prey = getPrey(l, t, player.hasTaboo)
	
	#Setup #2 - Hunting Specific Animals
	a = "Basan"
	animal = animalList[a]
	
	#Setup #3 - Bounty Hunting
	n = "Rabbit"
	npc = npcList[n]
	#npc.levelUp(0)
	
	'''Run only one of these'''
	#npc.processPersonality()
	#npc.setPersonality('Tempered')
	
	#npc.addAttack("Entice I")
	#npc.addArmour("Leather")

	'''Run Relevant One'''
	hunt = Hunting(player, prey, l)
	#hunt = Hunting(player, animal, l)
	#hunt = Hunting(player, npc, l)
	
	if not hunt.fail:
		setData()
		newCombat.runCombat(hunt.pred, hunt.prey, 1, hunt, ["No Item", 1], ["No Item", 1], [], [])
		hunt.afterCombat()
	
class Hunting:
	pred = None
	prey = None
	meat = 0
	pelt = 0
	fail = False
	start = True
	meatDmg = 0
	peltDmg = 0
	teaseBonus = 0
	teaseTurns = 0
	loc = ""
	
	def __init__(self,hunter,hunted,location,chase=True):
		self.pred = hunter
		self.prey = hunted
		self.meat = self.prey.Meat
		self.pelt = self.prey.Pelt
		self.fail = False
		self.start = True
		self.peltDmg = 0
		self.meatDmg = 0
		self.teaseBonus = 0
		self.teaseTurns = hunter.strategy.patience
		self.loc = location
		if chase:
			self.huntingSkills()
	
	def huntingSkills(self):
		self.fail = False
		for a in self.pred.advantages:
			a.modifySkills(self)
		for a in self.prey.advantages:
			a.modifySkills(self)
		
		self.pred.skills["Stealth"] += places[self.loc]["Stealth"]
		self.pred.skills["Acrobatics"] += places[self.loc]["Acrobatics"]
		self.prey.skills["Perception"] += places[self.loc]["Perception"]
		self.prey.skills["Escape"] += places[self.loc]["Escape"]
		
		sneak = runSkillCombat(self.pred, "Stealth", self.prey, "Perception")
		print self.pred.name + " has spotted a " + self.prey.name + " and tries to sneak up on it",
		print '(Stealth: {0}, Perception: {1})'.format(self.pred.skills["Stealth"],self.prey.skills["Perception"])
		if sneak == -5:
			print self.prey.name + " was startled and fled"
			self.fail = True
			return
		elif sneak < 0:
			print self.prey.name + " is suspicious that something is nearby"
		elif sneak < 5:
			print self.prey.name + " hears a noise but can't locate it"
		else:
			print self.pred.name + " sneaks up undetected"
			return
			
		chase = runSkillCombat(self.pred, "Acrobatics", self.prey, "Escape")
		print self.pred.name + " chases down the " + self.prey.name,
		print '(Acrobatics: {0}, Escape: {1})'.format(self.pred.skills["Acrobatics"],self.prey.skills["Escape"])
		if chase == -5 or sneak+chase < 0:
			print self.prey.name + " managed to get away"
			self.fail = True
		else:
			print self.pred.name + " catches the target and the fight begins"
	
	def modifyAccuracy(self, attack):
		if not isinstance(attack.defender, Huntable):
			return
		if attack.defender.Type == "NPC":
			return
		if self.teaseBonus > 0 and attack.weapon.DmgType != "Lust":
			attack.acc += self.teaseBonus * 3
			
	def modifyOffense(self, attack):
		if not isinstance(attack.defender, Huntable):
			return
		if attack.defender.Type == "NPC":
			return
		if self.teaseBonus > 0 and attack.weapon.DmgType != "Lust":
			attack.offense += self.teaseBonus // 3
			attack.crit += self.teaseBonus
	
	def modifyDamage(self, attack):
		if not isinstance(attack.defender, Huntable):
			return
		if attack.defender.Type == "NPC":
			return
		if attack.weapon.DmgType == "Lust":
			attack.perkinfo.append("\t" + attack.attacker.name + " lulls the " + attack.defender.name + " into a false sense of security (" + str(attack.damage) + " lust points)")
			self.teaseBonus += attack.damage
			self.teaseTurns -= 1
			if self.teaseTurns == 0:
				attack.damage = 0
			else:
				attack.defender.currentLust -= attack.damage
		else:
			if self.teaseBonus > 0:
				attack.perkinfo.append("\tThe " + attack.defender.name + " is no longer fooled by " + attack.attacker.name + "'s coaxings")
			self.teaseBonus = 0
			self.teaseTurns = self.pred.strategy.patience
	
	def runHunting(self, attack):
		status = {
			'Burned':'Fire',
			'Paralyzed':'Electric',
			'Poisoned':'Poison',
			'Freeze':'Ice'
		}
		damage = {
			'Physical':{'Meat':0,'Skin':0}, #Status attacks
			'Mental':{'Meat':0,'Skin':0}, #Status attacks
			'Emotional':{'Meat':0,'Skin':0}, #Status attacks
			'Piercing':{'Meat':1,'Skin':2},
			'Bludgeoning':{'Meat':2,'Skin':1},
			'Slashing':{'Meat':1,'Skin':2},
			'Fire':{'Meat':0,'Skin':10},
			'Electric':{'Meat':2,'Skin':2},
			'Ice':{'Meat':2,'Skin':1},
			'Poison':{'Meat':10,'Skin':1},
			'Lust':{'Meat':0,'Skin':0},
			'Psychic':{'Meat':0,'Skin':0},
		}
		
		if not isinstance(attack.defender, Huntable):
			return
		if attack.defender.Type == "NPC":
			return
			
		if attack.damage > 0:
			self.meatDmg = damage[attack.weapon.DmgType]['Meat']
			self.peltDmg = damage[attack.weapon.DmgType]['Skin']

			for a in attack.attacker.advantages:
				if isinstance(a, CarefulHunter) or isinstance(a, SloppyHunter):
					a.modifyMeatDamage(self, attack)
					a.modifyPeltDamage(self, attack)
			
			for a in attack.attacker.advantages:
				if isinstance(a, CarefulHunter) or isinstance(a, SloppyHunter):
					continue
				else:
					a.modifyMeatDamage(self, attack)
					a.modifyPeltDamage(self, attack)
		
			self.meat -= self.meatDmg
			self.pelt -= self.peltDmg
			self.start = False
			
		try:
			self.meat -= damage[status[attack.defender.status.text]]['Meat']
			self.pelt -= damage[status[attack.defender.status.text]]['Skin']
		except:
			pass
			
	def afterCombat(self):
		print
		if not self.prey.fled and not self.prey.ableToFight():
			print self.pred.name + " successfully felled a " + self.prey.name
			if self.prey.Type != "NPC":
				diff = 5 + self.prey.TGH // 2
				diff -= 5 if self.pred.hasSkinningKnife else 0
				success = runSkillCheck(self.pred, "Scavenge", diff)
				print '(Scavenge: {0}, Difficulty: {1} [Result: {2}])'.format(self.pred.skills["Scavenge"],diff, success)
				if success > 0:
					print self.pred.name + " managed not to damage the meat and pelt too much"
				else:
					print self.pred.name + " struggles at collecting meat and pelt from the " + self.prey.name
				self.meat *= 1 + (success - 1) / 6
				self.pelt *= 1 + (success - 1) / 6
				self.meat = min(int(self.meat), self.prey.Meat)
				self.pelt = min(int(self.pelt), self.prey.Pelt)
				self.printResult()
			else:
				success = runSkillCombat(self.pred, "Carry", self.prey, "Escape")
				print self.pred.getName() + " tries to drag the " + self.prey.name + " off to claim their bounty",
				print '(Carry: {0}, Escape: {1} [Result: {2}])'.format(self.pred.skills["Carry"],self.prey.skills["Escape"], success)
				rep = 5 + self.prey.Level - self.pred.Level
				
				if success > 0:
					print "The capture is successful, earning " + self.pred.getName() + " " + str(self.prey.Level * 20) + " gems"
				else:
					print self.pred.getName() + " was forced to kill the " + self.prey.name + " and only earned " + str(self.prey.Level * 10) + " gems"
					rep /= 2
				
				print self.pred.getName() + "'s reputation went up by " + str(int(rep))
				print self.prey.getName() + " dropped",
				print "{0} Gems and {1} {2} Items".format(self.prey.personTraits["GemX"]*self.prey.Level, int(self.prey.personTraits["LootX"]*self.prey.Level), self.prey.personTraits["Loot"])
		elif self.prey.fled:
			print self.prey.name + " got away"
		elif self.pred.fled:
			print self.pred.name + " fled the fight, hurt but not injured"
		else:
			print self.pred.name + " was beaten by the " + self.prey.name,
			if self.prey.Type == "NPC":
				print
				isHurt = self.prey.currentHP < (self.prey.MaxHP/2)
				isHorny = self.prey.currentLust > (self.prey.MaxLust/2)
				isBoth = isHurt and isHorny
				isNeither = (not isHurt) and (not isHorny)
				if isBoth:
					self.runVictory(self.prey.Both)
				elif isHurt:
					self.runVictory(self.prey.Hurt)
				elif isHorny:
					self.runVictory(self.prey.Horny)
				else:
					self.runVictory(self.prey.Neither)
				print self.pred.getName() + "'s reputation went down by " + str(5 + self.pred.Level - self.prey.Level)
			else:
				print "and barely managed to escape"
				print self.pred.getName() + " has been injured and will be reset to",
				if self.pred.currentHP <= 0:
					print "1 HP"
				else:
					print str(self.pred.MaxLust - 1) + " Lust"
				print self.pred.getName() + " will be unable to hunt for the next 96 hours, even if healed"
		
	def printResult(self):
		print '{0} obtained {1} cuts of meat (worth {3} SP) and {2} pieces of pelt'.format(self.pred.name, max(self.meat,0), max(self.pelt,0), max(self.meat,0)*2)
	
	def randItem(self):
		items = ["an aranium berry", 
		"a bottle of golden honey",
		"a vial of vipera oil",
		"an ursu fruit",
		"an equidae potion",
		"a vial of lupus mutation",
		"a bottle of vixen's elixir",
		"a felis berry",
		"a bottle of kangaroo milk",
		"a masked fig",
		"a bottle of carrot elixir",
		"a furry peach"]
		return items[randrange(len(items))]
	
	def runVictory(self, condition):
		text = victories[condition]
		if condition in ["Kill", "Destroy","Pillage"]:
			print text.format(self.prey.name, self.pred.getName(), self.prey.attacks[0])
		else:
			print text.format(self.prey.name, self.pred.getName())
		if condition in ["Ravage", "Violate","Gavage"]:
			print self.pred.getName() + " has been force-fed " + self.randItem()
	
#Make sure this is the main file being run
if __name__ == "__main__":
	global npcStrategies
	npcStrategies = readInJSON('npcStrategiesJSON.txt')
	main(sys.argv)