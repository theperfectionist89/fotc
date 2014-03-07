from baseClasses import *

class DefenseMode(PerkBuff):
	duration = 1
	def modifyDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		attack.defense += 5
		attack.perkinfo.append("\t" + attack.defender.name + " is protecting themselves, making them harder to hurt")
	
	def reduceDuration(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		self.duration -= 1
		if self.duration == 0:
			character.Perks.remove(self)
			if printFlag:
				print character.name + " comes out of Defense Mode"
				
	def modifyCharacterPostCombat(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.Perks.remove(self)

class SpeedPillBuff(PerkBuff):
	duration = -1
	
	def modifyCharacterPreTurn(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.agility += 4
		
	def modifyCharacterPostTurn(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		if not self.first:
			character.agility -= 4
		self.first = False
		
	def reduceDuration(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		self.duration -= 1
		if self.duration == 0:
			character.Perks.remove(self)
			if printFlag:
				print character.name + "'s Speed Pill wears off"
				
	def modifyCharacterPostCombat(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.Perks.remove(self)
		
class DuplicationBuff(PerkBuff):
	duration = 1
	fadedAway = False
	def modifyAccuracyDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		attack.acc /= 2
		
	def modifyAfterDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		if attack.damage > 0 and not self.fadedAway:
			attack.perkinfo.append("\t" + attack.attacker.name + " saw through the illusion")
		elif not self.fadedAway and not attack.contact:
			attack.perkinfo.append("\t" + attack.attacker.name + " attacked the illusion and it fades away")
			self.fadedAway = True
			
	def reduceDuration(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		if self.fadedAway:
			self.duration = 0
			character.Perks.remove(self)
			if printFlag:
				print character.name + "'s Duplication wears off"
				
	def modifyCharacterPostCombat(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.Perks.remove(self)
		
class DesireNegationBuff(PerkBuff):
	duration = -1
	
	def modifyDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		if attack.weapon.Category == "Tease":
			attack.defender.resistance += 7
	
	def reduceDuration(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass #Desire Negation never wears off
				
	def modifyCharacterPostCombat(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.Perks.remove(self)
		
class InvulnerabilityIBuff(PerkBuff):
	duration = 1
	
	def modifyDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		if attack.weapon.Category in ["Physical","Special"]:
			attack.defense += 99
			attack.perkinfo.append("\t" + attack.defender.name + " is invulnerable")
	
	def reduceDuration(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		self.duration -= 1
		if self.duration == 0:
			character.Perks.remove(self)
			if printFlag:
				print character.name + "'s Invulnerability wears off"
				
	def modifyCharacterPostCombat(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.Perks.remove(self)
		
class InvulnerabilityIIBuff(InvulnerabilityIBuff):
	duration = 2
	
	def modifyDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		attack.defense += 99
		attack.perkinfo.append("\t" + attack.defender + " is invulnerable")
		
	def statusDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		attack.statusDefense += 99
		attack.perkinfo.append("\t" + attack.defender + " is immune to status attacks")
	
class GravityManipulationIDebuff(PerkDebuff):
	duration = 4
	def modifyCharacterPreTurn(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		self.magnitude = max(3 + self.modifier, 1)
		character.agility -= self.magnitude
		
	def modifyCharacterPostTurn(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		if not self.first:
			character.agility += self.magnitude
		self.first = False
		
	def reduceDuration(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		self.duration -= 1
		if self.duration == 0:
			character.Perks.remove(self)
			if printFlag:
				print character.name + " is no longer slowed by Gravity Manipulation"
				
	def modifyCharacterPostCombat(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.Perks.remove(self)
		
class SenseManipulationIDebuff(PerkDebuff):
	duration = 3
	def modifyAccuracyOffense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		self.magnitude = max(6 + self.modifier,1)
		attack.acc -= self.magnitude
		
	def modifyAccuracyDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		self.magnitude = max(6 + self.modifier,1)
		attack.acc += self.magnitude
		
	def reduceDuration(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		self.duration -= 1
		if self.duration == 0:
			character.Perks.remove(self)
			if printFlag:
				print character.name + " is no longer oversensitive to pain"
				
	def modifyCharacterPostCombat(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.Perks.remove(self)
		
class SenseManipulationIIDebuff(PerkDebuff):
	duration = 4
	def modifyAccuracyOffense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		self.magnitude = max(10 + self.modifier,1)
		attack.acc -= self.magnitude
		
	def modifyAccuracyDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		self.magnitude = max(10 + self.modifier,1)
		attack.acc += self.magnitude
		
	def reduceDuration(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		self.duration -= 1
		if self.duration == 0:
			character.Perks.remove(self)
			if printFlag:
				print character.name + " is no longer oversensitive to pain"
				
	def modifyCharacterPostCombat(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.Perks.remove(self)