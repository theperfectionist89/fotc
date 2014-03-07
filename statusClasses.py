from random import randrange
from baseClasses import *	

class Healthy(Status):
	text = "Healthy"
	def startOfTurn(self, character):
		pass
	def endOfTurn(self, character):
		if self.printFlag:
			print character.name + " is Healthy"
		
class Attract(Status):
	text = "Captivated"
	hitChance = 60
	activeChance = 100
	def endOfTurn(self, character):
		if self.printFlag:
			print character.name + " is captivated and takes 3 lust damage"
		character.currentLust += 3
	
class Bleed(Status):
	text = "Bleeding"
	hitChance = 50
	activeChance = 100
	def endOfTurn(self, character):
		if self.printFlag:
			print character.name + " is bleeding and loses 3 health"
		character.currentHP -= 3
	
class Burn(Status):
	text = "Burned"
	hitChance = 60
	activeChance = 100
	def endOfTurn(self, character):
		if self.printFlag:
			print character.name + " loses 3 health from being burned"
		character.currentHP -= 3
	
class Confuse(Status):
	text = "Confused"
	hitChance = 90
	activeChance = 60
	def activate(self, character):
		weapon = character.weapon
		offense = weapon.Tier + weapon.Power
			
		if weapon.DmgType == "Physical":
			offense += character.power
			defense = character.defense
		elif weapon.DmgType == "Special":
			offense += character.energy
			defense = character.defense
		elif weapon.DmgType == "Tease":
			offense += character.energy
			defense = character.resistance
		else: #Status
			offense += character.power
			defense = character.resistance
			
		damage = max(offense - defense,0)
		
		print character.name + " attacks themselves in confusion"
		if weapon.DmgType == "Physical" or weapon.DmgType == "Special":
			character.currentHP -= damage
			if self.printFlag:
				print character.name + " received "+str(damage)+" physical damage"
		else:
			character.currentLust += damage
			if self.printFlag:
				print character.name + " received "+str(damage)+" Lust damage"
				
		character.skipTurn = True
		self.called += 1
	def endOfTurn(self, character):
		character.skipTurn = False
		self.called = 0
	
class Freeze(Status):
	text = "Frozen"
	hitChance = 70
	activeChance = 80
	def activate(self, character):
		if self.printFlag:
			print character.name + " is frozen and cannot attack"
		character.skipTurn = True
		self.called += 1
	def endOfTurn(self, character):
		character.skipTurn = False
		self.called = 0
		
class Kill(Status):
	text = "Killed"
	hitChance = 40
	activeChance = 100
	def endOfTurn(self, character):
		if self.printFlag:
			print character.name + " has been killed by a Death attack"
		character.currentHP = 0
	
class Paralyze(Status):
	text = "Paralyzed"
	hitChance = 60
	activeChance = 30
	def startOfTurn(self, character):
		if self.called == 0:
			if randrange(1,101) <= self.activeChance:
				self.activate(character)
			else:
				pass
		else:
			pass
	def activate(self, character):
		if self.printFlag:
			print character.name + " is paralyzed and cannot attack"
		character.skipTurn = True
		self.called += 1
	def endOfTurn(self, character):
		character.skipTurn = False
		self.called = 0

class Poison(Status):
	text = "Poisoned"
	hitChance = 60
	activeChance = 100
	def endOfTurn(self, character):
		if self.printFlag:
			print character.name + " loses 3 health from being poisoned"
		character.currentHP -= 3

class Venom(Poison):
	def endOfTurn(self, character):
		if self.printFlag:
			print character.name + " loses 5 health from venom"
		character.currentHP -= 5
		
class Sleep(Status):
	text = "Asleep"
	hitChance = 80
	activeChance = 70
	def activate(self, character):
		if self.printFlag:
			print character.name + " is asleep and cannot attack"
		character.skipTurn = True
		self.called += 1
	def endOfTurn(self, character):
		character.skipTurn = False
		self.called = 0
	
class Stun(Status):
	text = "Stunned"
	hitChance = 60
	activeChance = 100
	stunned = 0
	def activate(self, character):
		if self.printFlag:
			print character.name + " is stunned and cannot attack"
		if self.called == 0:
			character.skipTurn = True
		self.called += 1
	def endOfTurn(self, character):
		character.skipTurn = False
		if self.stunned>0:
			if self.printFlag:
				print character.name + " is Healthy"
			character.status = Healthy()
		self.stunned = 1