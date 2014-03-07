from __future__ import division
from math import sqrt
from statusClasses import Healthy
from healingClass import *
from powerClasses import *
from functions import *
from armourClass import *
import perkClasses
import healingClass
import powerClasses
import re, traceback

biteCreatures = ["Basilisk", "Snake", "Wolf", "Bear", "Spider"]
biteAnimals = ["Chimera", "Tanuki", "Horse", "Kangaroo", "Cat", "Fox", "Raccoon"]
hungerEffects = {
	"Healthy":0,
	"Hungry":5,
	"Famished":10,
	"Starving":15,
	"Dying":20
}

class Character(object):
	def __init__(self, name, **charStuff):
		try:
			self.__dict__.update(charStuff)
			self.name = name
			
			try:
				self.STR -= hungerEffects[self.Hunger]
				self.TGH -= hungerEffects[self.Hunger]
				self.SPE -= hungerEffects[self.Hunger]
				self.INT -= hungerEffects[self.Hunger]
				self.SPI -= hungerEffects[self.Hunger]
				self.CHA -= hungerEffects[self.Hunger]
			except:
				pass
				#Animals and NPCs have no hunger values
			
			self.Powers = re.findall('..',self.Powers)
			self.PerkList = re.findall('..',self.Perks)
			self.Items = []
			self.fled = False
			self.attacks = {}
			self.strategy = Strategy(self)
			self.skills = {}
			self.setCombatStats()
			self.setPerks()
			self.setPowers()
			self.setSkills()
			#Add Default Attacks
			if self.Class == "Animal":
				if self.Creature in biteCreatures or self.name in biteAnimals:
					self.addAttack('Bite')
			else:
				if self.Creature in biteCreatures:
					self.addAttack('Bite')		
				else:
					self.addAttack('Fists')
				self.addAttack('Tease')
			self.armour = Armour(**armourData['None'])
			#self.addArmour('None')
			self.skipTurn = False
			
			self.reset()
		except:
			print traceback.format_exc()
		
	def setCombatStats(self):
		tempLck = (self.SPE + self.INT + self.CHA) / 3
		tempLst = int(round(sqrt(self.Lust*2) * 17/5 - 3,0))
		self.escape = int(self.SPE / 4) 
		
		self.luck = int(round(sqrt(tempLck) * 17/5 - 3,0))
		self.power = int(round(sqrt(self.STR) * 17/5 - 3,0))
		self.energy = int(round((sqrt(self.CHA) * 17/5 - 3)*2/3 + tempLst/3,0))
		self.skill = int(round(sqrt(self.INT) * 17/5 - 3,0))
		self.agility = int(round(sqrt(self.SPE) * 17/5 - 3,0))
		self.defense = int(round(sqrt(self.TGH) * 17/5 - 3,0))
		self.resistance = int(round((sqrt(self.SPI) * 17/5 - 3)*4/3 - tempLst/3,0))
	
	def __repr__(self):
		return '\n'.join("%s: %s" % item for item in vars(self).items())
	
	def reset(self):
		self.status = Healthy()
		self.currentHP = self.MaxHP
		self.currentLust = 0
		self.strategy.runFailed = False
		self.fled = False
		
	def findBestAttack(self, printFlag=True):
		result = None
		priority = 1
		while result is None:
			result = next((attack for attack in self.attacks.itervalues() if attack.Priority == priority), None)
			if result is None:
				priority += 1
			elif result.currentCooldown > 0:
				if printFlag:
					print '\t' + result.Name + " is on cooldown"
				result = None
				priority += 1
			else:
				return result
				
	def setPreferences(self):
		for p in self.Powers:
			p.setPreference(self)
		
	def printAttacks(self):
		s = "["
		for k in self.attacks.iterkeys():
			s += k
			s += ", "
		s = s[:-2] + "]"
		return s
		
	def printItems(self):
		s = ""
		for i in self.Items:
			if isinstance(i, NoItem): #None
				continue
			try:
				s += i.text()
			except:
				s += i.Name
			s += " (" + str(i.uses) + ")"
			s += ", "
		s = "[" + s[:-2] + "]"
		return s
		
	def hasHealing(self):
		results = {'HP':[],'Lust':[],'Burned':[],'Paralyzed':[],'Captivated':[],
			'Frozen':[],'Poisoned':[],'Stunned':[],'Asleep':[],'Bleeding':[],'Healthy':[],'Buffs':[]}
		for i in self.Items:
			if i.uses > 0 and isinstance(i, Restorative) and (i.healAmt > 0 or i.healPct > 0):
				results['HP'].append(i)
			elif i.uses > 0 and isinstance(i, Restorative) and (i.pureAmt > 0 or i.purePct > 0):
				results['Lust'].append(i)
			elif i.uses > 0 and isinstance(i, Curative):
				results[i.cures].append(i)
			elif isinstance(i, Buff) and i.checkActive(self):
				results['Buffs'].append(i)
			
		return results
		
	def __repr__(self):
		return '{0}\nLevel {1} {2} {18}\nPOW:{3}\tERG:{4}\tSKI:{5}\nAGL:{6}\tDEF:{7}\tRES:{8}\nLCK:{9}\t HP:{10}/{11}\tLust:{12}/{13}\nPerks: {14}\nPowers: {15}\nBuffs: {16}\nAttacks: {17}\n'.format(self.name, self.Level, self.Creature, self.power, self.energy, self.skill, self.agility, self.defense, self.resistance, self.luck, self.currentHP, self.MaxHP, self.currentLust, self.MaxLust, self.Perks, self.Powers, self.printItems(), self.printAttacks(), self.Class)
		
	def printTurn(self):
		print '{0} ({5}): {1}/{2} HP, {3}/{4} Lust'.format(self.name, self.currentHP, self.MaxHP, self.currentLust, self.MaxLust, self.status.text)
		
	def printBasics(self):
		return '{0}\nLevel {1} {2} {13} \nSTR:{3}\tCHA:{4}\tINT:{5}\nSPE:{6}\tTGH:{7}\tSPI:{8}\nLST:{14}\tCRP:{15}\nHP:{9}/{10}\tLust:{11}/{12}\n'.format(self.name, self.Level, self.Creature, self.STR, self.CHA, self.INT, self.SPE, self.TGH, self.SPI, self.currentHP, self.MaxHP, self.currentLust, self.MaxLust, self.Class, self.Lust, self.Corruption) 
		
	def setPerks(self):
		module = __import__('perkClasses')
		perks = list()
		for i in range(len(self.PerkList)):
			try:
				perks.append(getattr(module, perkData[self.PerkList[i]])())
			except:
				print "Perk failed on", perkData[self.PerkList[i]]
		#self.PerkList = perks#makes no sense to overwrite this
		self.Perks = perks
		
		#Load all perk attacks and buffs
		for k in self.Perks:
			if isinstance(k, Weapon):
				name = " ".join(re.findall('[A-Z]+[a-z]*',str(k)))
				self.addAttack(name)
			elif isinstance(k, Buff):
				self.Items.append(k)
		self.Perks[:] = [i for i in self.Perks if (not isinstance(i, Weapon)) and (not isinstance(i, Buff))]
	
	def setSkills(self):
		try:
			self.skills = {
				"Charm":int(self.CHA / 4),
				"Escape":int(self.SPE / 4),
				"Suspicion":int(self.SPI / 4),
				"Knowledge":int(self.INT / 4),
				"Carry":int(self.STR / 6 + self.TGH / 12),
				"Acrobatics":int(self.SPE / 6 + self.STR / 12),
				"Stealth":int(self.SPE / 6 + self.INT / 12),
				"Search":int(self.INT / 6 + self.SPI / 12),
				"Scavenge":int(self.SPI / 6 + self.STR / 12),
				"Perception":int(self.SPI / 6 + self.INT / 12),
				"Intimidate":int(self.CHA / 6 + self.STR / 12)
			}
			self.runPerkFunc("modifySkills", character = self)
		except:
			print traceback.format_exc()
		
	def setPowers(self):
		modulePower = __import__('powerClasses')
		powers = list()
		for i in range(len(self.Powers)):
			try:
				temp = getattr(modulePower, powerData[self.Powers[i]])()
				powers.append(temp)
				tempOffshoot = temp.offshoot()
				if len(tempOffshoot) > 0:
					for off in tempOffshoot:
						if isinstance(off, powerClasses.PowerWeapon):
							name = off.Name
							self.addAttack( name) 
						elif isinstance(off, powerClasses.PowerPerk):
							self.Perks.append(off)
						elif isinstance(off, Healing): #Includes buffs
							self.Items.append(off)
						else:
							pass
				
				if isinstance(temp, powerClasses.PowerWeapon):
					name = " ".join(re.findall('[A-Z]+[a-z]*',str(temp)))
					self.addAttack(name) 
				elif isinstance(temp, powerClasses.PowerPerk):
					self.Perks.append(temp)
				elif isinstance(temp, Healing): #Includes buffs
					self.Items.append(temp)
				else:
					pass
			except:
				print traceback.format_exc()
				print "Power failed on", powerData[self.Powers[i]]
		self.Powers = powers
		
	def addAttack(self, name):
		self.attacks[name] = Weapon(**weaponData[name])
	
	def addArmour(self, name):
		#Armour
		self.armour.modifyCharacterPostCombat(self)
		self.armour = Armour(**armourData[name])
		self.armour.modifyCharacterPreCombat(self)
		
	def setItems(self, override=[]):
		items = []
		itemData = __import__('healingClass')
		count = ""
		input = ""

		if len(override) > 0:
			for i in range(0,len(override),2):
				item = getattr(itemData,override[i].replace(' ',''))()
				item.uses = int(override[i+1])
				self.Items.append(item)
			return override
		else:
			print "Leave Blank When Finished"
			input = raw_input("What is " + self.name + "'s first item?")
			if input == "":
				return ['No Item',1]
			count = raw_input("How many " + input + "s does " + self.name + " have?")
			while type(count) is str:
				try:
					count = int(count)
				except:
					print "Please enter a number"
					count = raw_input("How many " + input + "s does " + self.name + " have?")
			item = getattr(itemData,input.replace(' ',''))()
			item.uses = count
			self.Items.append(item)
			while input != "":
				input = raw_input("What is " + self.name + "'s next item?")
				count = raw_input("How many " + input + "s does " + self.name + " have?")
				while type(count) is str:
					try:
						count = int(count)
					except:
						print "Please enter a number"
						count = raw_input("How many " + input + "s does " + self.name + " have?")
				item = getattr(itemData,input.replace(' ',''))()
				item.uses = count
				self.Items.append(item)
			return items
			
	def reduceCooldown(self, printFlag):
		for a in self.attacks.itervalues():
			if a.currentCooldown > 0:
				a.currentCooldown -= 1
		for i in self.Items:
			if i.currentCooldown > 0:
				i.currentCooldown -= 1
		for perk in self.Perks:
			perk.reduceDuration(self, printFlag)
			
	def prioritizeAttacks(self, override=[]):
		k = 0
		options = [i+1 for i in range(len(self.attacks))]
		choices = []
		for a in self.attacks.itervalues():
			if len(options) > 1 and len(override) == 0:
				text = self.name + " has " + str(len(self.attacks)) + " attacks\n"
				for w in self.attacks.itervalues():
					text += w.Name + ": Priority " + str(w.Priority) + "\n"
				while a.Priority == 0:
					print "Please enter one of: " + str(options) + "\n"
					print text
					i = raw_input('What is the priority of ' + a.Name + "? ")
					try:
						j = int(i)
						if j in options:
							a.Priority = j
							options.remove(j)
						else:
							print "That is not a valid number"
					except:
						print "Please enter a number\n"
			elif len(override) == 0:
				a.Priority = options[0]
			else:
				a.Priority = override[k]
				k += 1
			choices.append(a.Priority)
		return choices
	
	def prioritizeBuffs(self, override=[], strategies={}):
		k = 0
		buffs = [x for x in self.Items if isinstance(x, Buff)]
		
		options = [i+1 for i in range(len(buffs))]
		choices = []
		for a in buffs:
			if len(options) > 1 and len(override) == 0:
				text = self.name + " has " + str(len(buffs)) + " buffs\n"
				for w in buffs:
					text += w.text() + ": Priority " + str(w.Priority) + "\n"
				while a.Priority == 0:
					print "Please enter one of: " + str(options) + "\n"
					print text
					i = raw_input('What is the priority of ' + a.text() + "? ")
					try:
						j = int(i)
						if j in options:
							a.Priority = j
							options.remove(j)
						else:
							print "That is not a valid number"
					except:
						print "Please enter a number\n"				
			elif len(override) == 0:
				a.Priority = options[0]
			else:
				a.Priority = override[k]
				k += 1
			choices.append(a.Priority)
			
			try:
				test = strategies[a.text()]
			except:	
				strategies[a.text()] = {'Trigger':'None','TriggerAmount':-1}
				while strategies[a.text()]['Trigger'] not in ['Start','Health','Lust']:
					input = raw_input('Please enter the trigger condition for ' + self.name + "'s " + a.text() + ' (Start, Health, or Lust): ')
					strategies[a.text()]['Trigger'] = input
				a.activeTrigger = input
				strategies[a.text()]['TriggerAmount'] = 0 if strategies[a.text()]['Trigger'] == "Start" else -1
				while strategies[a.text()]['TriggerAmount'] < 0:
					input = raw_input('Please enter the trigger amount for ' + self.name + "'s " + a.text() + ': ')
					try:
						strategies[a.text()]['TriggerAmount'] = int(input)
					except:
						print "Please enter a number\n"
				a.activeAmount = strategies[a.text()]['TriggerAmount']
		return choices, strategies
		
	def checkInitiative(self, op):
		if self.agility >= op.agility+5:
			return 2
		elif self.agility > op.agility:
			return 1
		elif self.agility == op.agility:
			return 0
		else:
			return -1

	def runPerkFunc(self, funcName, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		for perk in self.Perks:
			func = getattr(perk, funcName)
			func(character, enemy, attack, amount, printFlag)
			
	def ableToFight(self):
		return self.currentHP > 0 and self.currentLust < self.MaxLust
			
	def getName(self):
		return re.match('(\w+)',self.name).group(1)
		#return () or (p2.agility >= p1.agility+5)
		
	def levelUp(self, increase):
		tempHP = self.MaxHP
		tempHP -= self.Level
		tempHP -= int(self.TGH / 2)
		tempLst = self.MaxLust
		tempLst -= self.Level
		tempLst -= int(self.Lust / 2 + self.SPI / 4)
		
		for i in range(increase):
			self.Level += 1
			self.STR += classUpData[self.Class]["STR"]
			self.STR += racesUpData[self.Creature]["STR"]
			self.TGH += classUpData[self.Class]["TGH"]
			self.TGH += racesUpData[self.Creature]["TGH"]
			self.SPE += classUpData[self.Class]["SPE"]
			self.SPE += racesUpData[self.Creature]["SPE"]
			self.INT += classUpData[self.Class]["INT"]
			self.INT += racesUpData[self.Creature]["INT"]
			self.SPI += classUpData[self.Class]["SPI"]
			self.SPI += racesUpData[self.Creature]["SPI"]
			self.CHA += classUpData[self.Class]["CHA"]
			self.CHA += racesUpData[self.Creature]["CHA"]
			self.Lust += classUpData[self.Class]["LST"]
			self.Lust += racesUpData[self.Creature]["LST"]
			self.Corruption += classUpData[self.Class]["CRP"]
			
		tempHP += int(self.TGH / 2)
		tempHP += self.Level
		tempLst += int(self.Lust / 2 + self.SPI / 4)
		tempLst += self.Level
		self.MaxHP = tempHP
		self.currentHP = self.MaxHP
		self.MaxLust = tempLst
		self.setCombatStats()
		self.setSkills()
		
class Strategy:
	healBelow = 0 #The health at which point a healing item will be used
	healPrior = True #True uses the best healing item/power the character has available, False uses the most renewable (powers and then cheap items)
	pureAbove = 999 #The lust at which point a purification item will be used
	purePrior = True #True uses the best purifying item/power the character has available, False uses the most renewable (powers and then cheap items)
	runHealth = 0 #The health at which point the character will attempt to run away
	panicMode = False #If True, the character will run even when the first attempt to flee fails
	runFailed = False #Attempted to run away and failed this combat
	fixStatus = False #Will attempt to cure any status conditions
	useBasics = True #Will use 0 cooldown moves. If this is false, the character will go into Defense Mode until at least one cooldown goes to 0
	actOrders = [] #Order of priority for healing, purifying, status curing, buffs, and running away if multiple apply
	patient = 0 #Not used here, but hunting needs it
	
	#More to come
	
	def __init__(self, character):
		self.character = character
		self.healBelow = 0
		self.healPrior = True
		self.pureAbove = 999
		self.purePrior = True
		self.runHealth = 0
		self.runLust = 999
		self.panicMode = False
		self.runFailed = False
		self.fixStatus = False
		self.useBasics = True
		self.actOrders = [1,2,3,4,5]
		self.patience = 0
		
	def getHealing(self, options):
		powerCount = 0
		healing = []
		powers = []
		best = None
		bestValue = 999
		damage = self.character.MaxHP - self.character.currentHP
		for i in options:
			healing.append(i.getHealValue(self.character))
			if isinstance(i, Power):
				powers.append(i)
				powerCount += 1
			else:
				powers.append(None)
			
		if self.healPrior:
			try:
				val, idx = min((val,idx) for (idx,val) in enumerate(healing) if val - damage > 0)
			except:
				val, idx = max((val,idx) for (idx,val) in enumerate(healing))
			best = options[idx]
		else:
			if powerCount > 0:
				val, idx = min((val,idx) for (idx,val) in enumerate(healing) if powers[idx] is not None)
				best = powers[idx]
			else:			
				val, idx = min((val, idx) for (idx, val) in enumerate(healing))
				best = options[idx]
		return best
		
	def getPurify(self, options):
		powerCount = 0
		healing = []
		powers = []
		best = None
		bestValue = 999
		damage = self.character.currentLust
		for i in options:
			healing.append(i.getPureValue(self.character))
			if isinstance(i, Power):
				powers.append(i)
				powerCount += 1
			else:
				powers.append(None)
			
		if purePrior:
			val, idx = min((val,idx) for (idx,val) in enumerate(healing) if val - damage > 0)
			best = options[idx]
		else:
			if powerCount > 0:
				val, idx = min((val,idx) for (idx,val) in enumerate(healing) if powers[idx] is not None)
				best = powers[idx]
			else:			
				val, idx = min((val, idx) for (idx, val) in enumerate(healing))
				best = options[idx]
		return best
		
	def getCure(self, options):
		#prioritize renewable healing aka powers
		best = None
		for i in options:
			if isinstance(i, Power):
				return i
			else:
				if best is None:
					best = i
		return best
		
	def getBuff(self, options):
		priority = 9999
		best = None
		for b in options:
			if b.Priority < priority:
				best = b
		return best
		
	def getAction(self):
		options = self.character.hasHealing()
		healFlag = self.character.currentHP <= self.healBelow and len(options['HP']) > 0
		pureFlag = self.character.currentLust >= self.pureAbove and len(options['Lust']) > 0
		statFlag = not isinstance(self.character.status, Healthy) and self.fixStatus and options[self.character.status.text]
		fleeFlag = (self.character.currentHP <= self.runHealth or self.character.currentLust >= self.runLust) and (self.panicMode or not self.runFailed)
		buffFlag = len(options['Buffs']) > 0
		healFlag = self.actOrders[0] if healFlag else 9
		pureFlag = self.actOrders[1] if pureFlag else 9
		statFlag = self.actOrders[2] if statFlag else 9
		buffFlag = self.actOrders[3] if buffFlag else 9
		fleeFlag = self.actOrders[4] if fleeFlag else 9
		attkFlag = self.checkAttack()
		
		if healFlag == min(healFlag,pureFlag,statFlag,buffFlag,fleeFlag) and healFlag < 9:
			return self.getHealing(options['HP'])
		elif pureFlag == min(healFlag,pureFlag,statFlag,buffFlag,fleeFlag) and pureFlag < 9:
			return self.getPurify(options['Lust'])
		elif pureFlag == min(healFlag,pureFlag,statFlag,buffFlag,fleeFlag) and statFlag < 9:
			return self.getCure(options[self.character.status.text])
		elif fleeFlag == min(healFlag,pureFlag,statFlag,buffFlag,fleeFlag) and fleeFlag < 9:
			return "Flee"
		elif buffFlag == min(healFlag,pureFlag,statFlag,buffFlag,fleeFlag) and buffFlag < 9:
			return self.getBuff(options['Buffs'])
		elif attkFlag:
			return "Attack"
		else:
			return "Wait"
			
	def checkAttack(self):
		self.useBasics = False if len([x for x in self.character.attacks.itervalues() if x.Cooldown == 0]) == 0 else self.useBasics
		check = len([x for x in self.character.attacks.itervalues() if (x.currentCooldown == 0 and x.Cooldown > 0)]) > 0
		return check or self.useBasics
		
def setData():
	global characterData, perkData, powerData, weaponData, armourData, classUpData, racesUpData
	characterData = readInJSON('peopleJSON.txt')
	weaponData = readInJSON('weaponsJSON.txt')
	powerClasses.weaponData = weaponData
	perkData = readInJSON('perksJSON.txt')
	powerData = readInJSON('powersJSON.txt')
	armourData = readInJSON('armourJSON.txt')
	classUpData = readInJSON('ClassUpsJSON.txt')
	racesUpData = readInJSON('racesJSON.txt')
	
def getCharacter(name):
	return Character(name, **characterData[name])
	
setData()