from __future__ import division
from functions import *
from characterClasses import *
from armourClass import *
from powerClasses import *
from skillCombat import *
from perkBuff import DefenseMode
from baseClasses import *
import statusClasses
import healingClass

from random import randrange
from copy import deepcopy
import io, json, sys, re, traceback

def checkPrint(toPrint, flag=False, comma=False):
	if flag:
		if callable(toPrint):
			toPrint()
		else:
			if comma:
				print toPrint,
			else:
				print toPrint

def checkEnd(p1, p2):
	p1defeated = not p1.ableToFight()
	p2defeated = not p2.ableToFight()
	if p1defeated and p2defeated:
		return 5
	if p1defeated:
		return 4
	elif p1.fled:
		return 3
	elif p2defeated:
		return 2
	elif p2.fled:
		return 1
	else:
		return 0
	
def reset(p1, p2):
	p1.reset()
	p2.reset()
	for a in p1.attacks.itervalues():
		a.currentCooldown = 0
	for a in p2.attacks.itervalues():
		a.currentCooldown = 0
	p1.Items[:] = [x for x in p1.Items if isinstance(x, Power)]
	for i in p1.Items:
		i.uses = i.maxUses

	p2.Items[:] = [x for x in p2.Items if isinstance(x, Power)]
	for i in p2.Items:
		i.uses = i.maxUses
		
def main(argv):	
	p1 = "Gwendolyn Janusdottir"
	p2 = "Morcdar"
	n = 1000

	setData()

	#Copied to allow people to fight themselves
	player1 = getCharacter(p1)
	player2 = getCharacter(p2)
	
	results = combatSetup(player1, player2, n)

	#Results = [P2 Runs, P1 Wins, P1 Runs, P2 Wins, Draw]
	
	p1 = re.match('(\w+)',p1).group(1)
	p2 = re.match('(\w+)',p2).group(1)
	length = max(len(text) for text in [p1, p2])
	
	print
	print '{0:{3}}: {1:4d} Wins on KO, {2:4d} Wins on Flee'.format(p1, results[1], results[0], length)
	print '{0:{3}}: {1:4d} Wins on KO, {2:4d} Wins on Flee'.format(p2, results[3], results[2], length)
	print '{0:{2}}: {1:4d}'.format("Draw", results[4], length)

def combatSetup(player1, player2, n):
	#Strategy
	
	#player1.strategy.healBelow = 10
	#player1.strategy.healPrior = True
	#player1.strategy.pureAbove = 15
	player1.strategy.runHealth = 4
	player1.strategy.runLust = 18
	#player1.strategy.fixStatus = False
	player1.strategy.panicMode = True
	#player1.strategy.actOrders = [2, 3, 4, 5, 1] #Heal, Pure, Status, Buff, Run
	#player1.strategy.useBasics = False
	
	#player2.strategy.healBelow = 7
	#player2.strategy.healPrior = True
	#player2.strategy.pureAbove = 16
	#player2.strategy.runHealth = 5
	#player2.strategy.runLust = 25
	#player2.strategy.fixStatus = False
	#player2.strategy.panicMode = True
	#player2.strategy.actOrders = [2, 3, 4, 1] #Heal, Pure, Status, Run
	
	#Override Items
	items1 = ['No Item',1]
	items2 = ['No Item',1]
	
	#Overriding Priorities
	prior1 = [1,2]
	prior2 = []#[1,2,3]
	
	#Weapons
	#addAttack(player1, 'Crossbow')
	#addAttack(player2, 'Scimitar')
	
	return runCombat(player1, player2, n, None, items1, items2, prior1, prior2)
	
def runCombat(player1, player2, trials=1, hunting=None, i1=[], i2=[], pr1=[], pr2=[]):
	
	file = open('combatOutput.txt', 'w')
		
	items1 = i1
	items2 = i2
	
	items1 = player1.setItems(items1)
	items2 = player2.setItems(items2)
	
	print "*************************************"
	print player1
	print player1.name + " is wearing " + player1.armour.Name + " armour\n"
	print player2
	print player2.name + " is wearing " + player2.armour.Name + " armour"
	print "*************************************"
	
	prior1 = pr1
	prior2 = pr2
	
	prior1 = player1.prioritizeAttacks(prior1)
	prior2 = player2.prioritizeAttacks(prior2)
	
	buffPrior1 = []
	buffStrat1 = {}
	buffPrior2 = []
	buffStrat2 = {}
	buffPrior1, buffStrat1 = player1.prioritizeBuffs(buffPrior1, buffStrat1)
	buffPrior2, buffStrat2 = player2.prioritizeBuffs(buffPrior2, buffStrat2)
	
	#Preferences - For powers and perks that can do different things
	player1.setPreferences()
	player2.setPreferences()
	
	results = [0, 0, 0, 0, 0]
	
	for i in range(trials):
		if i == 0:
			print
		r = combat(player1, player2, file, i, i==0, hunting)
		
		if i < trials-1:
			reset(player1, player2)
			prior1 = player1.prioritizeAttacks(prior1)
			prior2 = player2.prioritizeAttacks(prior2)
			items1 = player1.setItems(items1)
			items2 = player2.setItems(items2)
			buffPrior1, buffStrat1 = player1.prioritizeBuffs(buffPrior1, buffStrat1)
			buffPrior2, buffStrat2 = player2.prioritizeBuffs(buffPrior2, buffStrat2)
		results[r-1] += 1
	
	file.close()
	
	return results
	
def fleeAttempt(runner, chaser, printFlag=False):
	runner.runPerkFunc("modifyFlee", character = runner)
	chaser.runPerkFunc("modifyFlee", character = chaser)
	run = runner.skills["Escape"]
	catch = chaser.skills["Acrobatics"]
	if runSkillCombat(runner,"Escape",chaser,"Acrobatics") > 0:
		runner.fled = True
		if printFlag:
			print "\t" + runner.name + " fled the fight", '- Run: {0}, Catch: {1}'.format(run, catch)
	else:
		runner.strategy.runFailed = True
		if printFlag:
			print "\t" + runner.name + " tried to run away but failed", '- Run: {0}, Catch: {1}'.format(run, catch)
	runner.runPerkFunc("modifyFleeAfter", character = runner)
	chaser.runPerkFunc("modifyFleeAfter", character = chaser)

def getFirst(p1,p2):
	#check initiative return 2 if double, 1 if first, 0 if tie, -1 otherwise
	val = p1.checkInitiative(p2)
	if val >0:
		return (p1,p2, val==2)
	elif val<0:
		return (p2,p1,p2.checkInitiative(p1)==2)
	else:
		if randrange(0,2) == 0:
			return (p1,p2, False)
		else:
			return (p2,p1, False)
		
			
def combat(player1, player2, file, trial, printFlag, hunting=None):
	oldName1 = player1.name
	oldName2 = player2.name

	for perk in player1.Perks:
		perk.modifyCharacterPreCombat(player1, player2, printFlag)
	for perk in player2.Perks:
		perk.modifyCharacterPreCombat(player2, player1, printFlag)
	
	attackCount = 0
	end = checkEnd(player1, player2)
	while end == 0:
		# apply buff activate
		for perk in player1.Perks:
			perk.modifyCharacterPreTurn(player1, printFlag)
		for perk in player2.Perks:
			perk.modifyCharacterPreTurn(player2, printFlag)
			
		if attackCount % 3 == 0:
			player1,player2,double = getFirst(player1,player2)
			p1ATK = Attack(player1, player2, file, printFlag)
			p2ATK = Attack(player2, player1, file, printFlag)
			nextTurn1 = player1.strategy.getAction()
			nextTurn2 = player2.strategy.getAction()
			
		if attackCount % 3 == 0:
			#do start of turn status stuffs
			startofTurnStatus(player1)
			checkPrint(player1.getName() + "'s turn", printFlag)
			if not player1.skipTurn:
				if nextTurn1 == "Attack" or isinstance(nextTurn1, PowerDebuff):
					p1ATK.performAttack(nextTurn1, hunting)
				elif nextTurn1 == "Flee":
					fleeAttempt(player1, player2, printFlag)
				else:
					runHealing(player1, player2, nextTurn1, printFlag)
			else:
				checkPrint('\t' + player1.getName() + " cannot act this turn", printFlag)
		elif attackCount % 3 == 1:
			startofTurnStatus(player2)
			checkPrint(player2.getName() + "'s turn", printFlag)
			if not player2.skipTurn:
				if nextTurn2 == "Attack" or isinstance(nextTurn2, PowerDebuff):
					p2ATK.performAttack(nextTurn2, hunting)
				elif nextTurn2 == "Flee":
					fleeAttempt(player2, player1, printFlag)
				else:
					runHealing(player2, player1, nextTurn2, printFlag)
		else:
			if double and not player1.skipTurn and (nextTurn1 == "Attack" or isinstance(nextTurn1, PowerDebuff)):
				startofTurnStatus(player1)
				if not player1.skipTurn and player1.strategy.checkAttack():
					checkPrint(player1.getName() + "'s turn", printFlag)
					p1ATK.performAttack(nextTurn1, hunting)
				elif not player1.skipTurn:
					checkPrint(player1.getName() + "'s turn", printFlag)
					checkPrint("\t" + player1.getName() + " has no available moves", printFlag)
		
		#apply buff remove
		for perk in player1.Perks:
			perk.modifyCharacterPostTurn(player1, printFlag)
		for perk in player2.Perks:
			perk.modifyCharacterPostTurn(player2, printFlag)
		
		if attackCount % 3 == 2:# do end of round shit
			player1.status.printFlag = printFlag
			player2.status.printFlag = printFlag
			player1.status.endOfTurn(player1)
			player2.status.endOfTurn(player2)
			checkPrint(player1.printTurn, printFlag)
			checkPrint(player2.printTurn, printFlag)
			checkPrint("End Round\n", printFlag)
			player1.reduceCooldown(printFlag)
			player2.reduceCooldown(printFlag)
		
		#reduce duration buff
		attackCount += 1
		end = checkEnd(player1, player2)
		
	checkPrint("\nEndgame", printFlag)
	checkPrint(player1.printTurn, printFlag)
	checkPrint(player2.printTurn, printFlag)
		
	if not printFlag:
		if end == 1 or end == 2:
			endText = "P1"
		elif end == 3 or end == 4:
			endText = "P2"
		else:
			endText = "Tie"
		file.write('Trial {0: 4d} - Winner {1:}\t'.format(trial+1, endText))
		file.write('[{0} ({5}): {1}/{2} HP, {3}/{4} Lust]\t'.format(player1.getName(), player1.currentHP, player1.MaxHP, player1.currentLust, player1.MaxLust, player1.status.text))
		file.write('[{0} ({5}): {1}/{2} HP, {3}/{4} Lust]\n'.format(player2.getName(), player2.currentHP, player2.MaxHP, player2.currentLust, player2.MaxLust, player2.status.text))
		
	for perk in player1.Perks:
		perk.modifyCharacterPostCombat(player1, player2, printFlag)
	for perk in player2.Perks:
		perk.modifyCharacterPostCombat(player2, player1, printFlag)

	#convert this back to the P1 and P2 that it was sent in as
	if player1.name != oldName1:
		if end % 2 == 0:
			end = 6 - end
		elif end < 5:
			end = 4 - end
		
	return end

def startofTurnStatus(char):
	char.status.startOfTurn(char)

def checkImmunity(attack):
	chr = attack.defender
	for perk in chr.Perks:
		perk.statusImmunity(chr)
	for item in chr.Items:
		if isinstance(item, Curative):
			item.cureStatusAuto(chr, attack)
		
def runHealing(player, enemy, item, printFlag):
	if isinstance(item, Curative):
		item.cureStatus(player, printFlag = printFlag)
	elif isinstance(item, Restorative):
		item.applyHealing(player, printFlag = printFlag)
		item.applyPurify(player, printFlag = printFlag)
	elif isinstance(item, str):
		player.Perks.append(DefenseMode())
		if printFlag:
			print "\t" + player.name + " protects him/herself"
	else:
		item.applyBuff(player, printFlag = printFlag)		
		
class Attack:
	attacker = None
	weapon = None
	defender = None
	damage = 0
	acc = 0
	offense = 0
	defense = 0
	crit = 0
	critical = False
	perkinfo = []
	output = None
	printFlag = True
	statusAttack = False
	
	def __init__(self,attacker,defender,output, printFlag):
		self.attacker = attacker
		self.attacker.status.printFlag = printFlag
		self.defender = defender
		self.defender.status.printFlag = printFlag
		self.perkinfo = []
		self.output = output
		self.printFlag = printFlag
		
	def advancedInformation(self):
		string = self.attacker.name + " attacks with " + self.weapon.Name + "\n"
		string += '{0:10s} {1:10d}\n'.format("Damage:",self.damage)
		string += '{0:10s} {1:10d}\n'.format("Accuracy:",self.acc)
		string += '{0:10s} {1:>10s} ({2:4d})\n'.format("Critical:",str(self.critical),self.crit)
		string += '{0:10s} {1:>10s}\n'.format("Contact:", str(self.contact))
		string += '{0:10s} {1:>10s} --> {2:10s} ({3:4d})\n'.format("Def State:", self.oldStatus, self.defender.status.text, self.statusChance)
		self.output.write(string)
		self.output.write("****************************\n")
	
	def performAttack(self, attackType="Attack", hunting=None):
		atkName = re.match('(\w+)',self.attacker.name).group(1)
		defName = re.match('(\w+)',self.defender.name).group(1)
		
		self.oldStatus = self.defender.status.text
		checkPrint('\t' + atkName + " is attacking", self.printFlag)
		
		if attackType == "Attack":
			self.weapon = self.attacker.findBestAttack(self.printFlag)
		else:
			self.weapon = Weapon(**weaponData[attackType.Name])
		
		#Defaults
		self.damage = 0
		self.statusChance = 0
		self.statusAttack = False

		self.acc = self.weapon.Tier + self.weapon.Accuracy + int((self.attacker.skill*3+self.attacker.luck)/2)
		self.acc -= int((self.defender.agility*3+self.defender.luck)/2)
		
		self.attacker.runPerkFunc("modifyAccuracyOffense", attack = self)
		self.defender.runPerkFunc("modifyAccuracyOffense", attack = self)
		if hunting is not None:
			hunting.modifyAccuracy(self)
			
		#modify accuracy using conditions and modifiers such as no guard
		#determine if hit (do random and see if in range)
		self.contact = randrange(1,101) <= self.acc
		# maybe do modifier if there are any that would apply here not sure
		#determine damage
		
		if self.contact:
			checkPrint('\t' + atkName + " hits with " + self.weapon.Name + ' ({0:d}%)'.format(self.acc), self.printFlag, True)
			
			self.offense = self.weapon.Tier + self.weapon.Power

			if self.weapon.Category == "Physical":
				self.offense += self.attacker.power
				self.defense = self.defender.defense
			elif self.weapon.Category == "Special":
				self.offense += self.attacker.energy
				self.defense = self.defender.defense
			elif self.weapon.Category == "Tease":
				self.offense += self.attacker.energy
				self.defense = self.defender.resistance
			else: #Status
				self.statusAttack = True
				if self.weapon.DmgType == "Physical":
					self.statusOffense = self.attacker.power
				elif self.weapon.DmgType == "Emotional":
					self.statusOffense = self.attacker.energy
				else: #Mental
					self.statusOffense = self.attacker.skill
				self.statusDefense = self.defender.resistance
				
			if self.statusAttack:
				self.attacker.runPerkFunc("statusOffense",attack = self)
				self.defender.runPerkFunc("statusDefense",attack = self)
				
				self.statusChance = self.statusOffense
				modifier = self.statusOffense - self.statusDefense
				attackType.applyDebuff(self, modifier // 5)
			else:
				self.crit = self.weapon.Critical + int(self.attacker.skill/2)
				self.crit = max(self.crit - self.defender.luck,0)
				self.attacker.runPerkFunc("modifyCritOffense",attack = self)
				self.defender.runPerkFunc("modifyCritDefense",attack = self)
				if hunting is not None:
					hunting.modifyOffense(self)
				
				self.critical = randrange(1,101) <= self.crit
			
				self.attacker.runPerkFunc("modifyOffense",attack = self)
				self.defender.runPerkFunc("modifyDefense",attack = self)		
				
				self.damage = max(self.offense - self.defense,0)
				self.damage *= 3 if self.critical else 1
				
				self.attacker.runPerkFunc("modifyDamageOffense",attack = self)
				self.defender.runPerkFunc("modifyDamageDefense",attack = self)
				if hunting is not None:
					hunting.modifyDamage(self)
				
				if self.weapon.Category == "Physical" or self.weapon.Category == "Special":
					self.defender.currentHP -= self.damage
				else:
					self.defender.currentLust += self.damage
				checkPrint("dealing " + '{0:d} {1:s}'.format(self.damage,self.weapon.DmgType) + " damage", self.printFlag, True)
				
				if self.critical:
					checkPrint("(a critical hit)", self.printFlag)
				else:
					checkPrint("", self.printFlag)
				
			#Apply status effects
			statuses = __import__('statusClasses')
			try:
				status = getattr(statuses,self.weapon.Special)()
			except:
				status = Healthy()
			status.printFlag = self.printFlag
			self.statusChance += status.hitChance - self.defender.resistance

			if randrange(1,101) <= self.statusChance and isinstance(self.defender.status, Healthy):
				self.defender.status = status
				checkImmunity(self)
				
				if isinstance(self.defender.status, Healthy):
					checkPrint('\t' + defName + " is immune to being " + status.text, self.printFlag)
				else:
					checkPrint('\t' + defName + " is now " + status.text, self.printFlag)
		else:
			checkPrint("\t" + atkName + " misses with " + self.weapon.Name + ' ({0:d}%)'.format(self.acc), self.printFlag)
			if self.statusAttack:
				attackType.useFailed()
			
		#do post damage stuff
		self.attacker.runPerkFunc("modifyAfterOffense",attack = self)
		self.defender.runPerkFunc("modifyAfterDefense",attack = self)
			
		#Check for ineffective weapon
		ineff1 = self.weapon.Category == "Status" and self.weapon.Special != "None" and not isinstance(self.defender.status, Healthy)
		ineff2 = self.weapon.Category != "Status" and self.contact and self.damage == 0
		ineff3 = self.acc <= 0
		if ineff1 or ineff2 or ineff3:
			priority = self.weapon.Priority
			results = [attack for attack in self.attacker.attacks.itervalues() if attack.Priority > priority]
			for r in results:
				r.Priority -= 1
			self.weapon.Priority = len(self.attacker.attacks)
			checkPrint("\t" + self.weapon.Name + " is ineffective and drops in priority", self.printFlag)
			
			'''
			print self.attacker.name + "'s New Priorities:"
			for a in self.attacker.attacks.itervalues():
				print a.Name + " - P: " + str(a.Priority)
			print
			'''
	
		if self.printFlag:
			for i in self.perkinfo:
				print i
			self.advancedInformation()
			
		if hunting is not None:
			hunting.runHunting(self)

		self.perkinfo = []
		self.weapon.currentCooldown = self.weapon.Cooldown
		self.attacker.runPerkFunc("modifyCooldownOffense",attack = self)
		self.defender.runPerkFunc("modifyCooldownDefense",attack = self)
			
#Make sure this is the main file being run
if __name__ == "__main__":
	main(sys.argv)