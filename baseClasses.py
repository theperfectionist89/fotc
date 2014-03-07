import pprint, traceback, re
from random import randrange

class perk:
	def modifyAccuracyOffense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def modifyAccuracyDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def modifyCritDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def modifyCritOffense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def modifyCharacterPreCombat(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def modifyCharacterPostCombat(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def modifyOffense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def modifyDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def modifyDamageOffense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def modifyDamageDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def modifyConditionDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def modifyAfterOffense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def modifyAfterDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def statusImmunity(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def statusOffense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def statusDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def modifyCooldownOffense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def modifyCooldownDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def modifyCharacterPreTurn(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def modifyCharacterPostTurn(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def reduceDuration(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def modifySkills(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def modifyHealing(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def modifyPurify(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def modifyFlee(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def modifyFleeAfter(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		pass
	def __repr__(self):
		return " ".join(re.findall('[A-Z]+[a-z]*',str(self.__class__.__name__)))
		
class Weapon:
	def __init__(self, **weaponStats):
		try:
			self.__dict__.update(weaponStats)
			#pprint.pprint(traceback.format_stack())
			if self.Contact == "Yes":
				self.Contact = True 
			else:
				self.Contact = False
			self.Priority = 0
			self.currentCooldown = 0
		except:
			print traceback.format_exc()

	def __repr__(self):
		return self.Name	

class Healing:
	uses = 1
	cooldown = 1
	currentCooldown = 0
	
	def __repr__(self):
		#return self.__class__.__name__ + ', '.join("%s: %s" % item for item in vars(self).items())
		return self.text()
		
	def text(self):
		return " ".join(re.findall('[A-Z]+[a-z]*',str(self.__class__.__name__)))
		
class Restorative(Healing):
	healAmt = 0
	healPct = 0
	pureAmt = 0
	purePct = 0
	
	def applyHealing(self, character, printFlag):
		healed = 0
		if self.uses > 0 and self.currentCooldown == 0:
			healed += int(self.healPct/100*character.MaxHP)
			healed += self.healAmt
			for p in character.perks:
				healed = p.modifyHealing(healed)
			character.currentHP += healed
			character.currentHP = min(character.currentHP, character.MaxHP)
			self.uses -= 1
			self.currentCooldown = self.cooldown
			if healed > 0 and printFlag:
				print character.name + ' healed ' + str(healed) + ' HP using ' + self.text()
		else:
			pass
	def applyPurify(self, character, printFlag):
		purified = 0
		if self.uses > 0 and self.currentCooldown == 0:
			purified += int(self.purePct/100*character.MaxLust)
			purified += self.pureAmt
			for p in character.perks:
				purified = p.modifyPurify(purified)
			character.currentLust -= purified
			character.currentLust = max(character.currentLust, 0)
			self.uses -= 1
			self.currentCooldown = self.cooldown
			if purified > 0 and printFlag:
				print character.name + ' cured ' + str(purified) + ' Lust using ' + self.text()
		else:
			pass
			
	def getHealValue(self, character):
		return self.healAmt + int(self.healPct/100*character.MaxHP)
	
	def getPureValue(self, character):
		return self.pureAmt + int(self.purePct/100*character.MaxHP)
		
class Curative(Healing):
	cures = ""
	def cureStatus(self, character, attack):
		pass
	def cureStatusAuto(self, character, attack):
		pass
	
class Buff(Healing):
	activeTrigger = "" #Start, Health, Lust
	activeAmount = 0
	isActive = False
	Priority = 0
	
	def checkActive(self, character, enemy=None): #Enemy is here for possible future triggers
		check = False
		
		if self.activeTrigger == "Start":
			check = True	
		elif self.activeTrigger == "Health" and character.currentHP <= self.activeAmount:
			check = True
		elif self.activeTrigger == "Lust" and character.currentLust >= self.activeAmount:
			check = True
			
		if check and self.uses > 0 and self.currentCooldown == 0:
			return True
		else:
			return False
			
	def useBuff(self):
		#Called by children when their applyBuff is triggered
		self.currentCooldown = self.cooldown
		self.uses -= 1
		self.isActive = True
		
	def useFailed(self):
		self.useBuff()
		self.isActive = False
			
	def applyBuff(self, character, printFlag=False):
		pass
		
class PerkWeapon(Weapon):
	def __init__(self, **weaponStats):
		pass

class PerkBuff(perk):
	duration = 2
	first = True
	
class PerkDebuff(PerkBuff):
	modifier = 0
	magnitude = 0
	def __init__(self, mod):
		self.modifier = mod
		
class Status:
	text = ""
	printFlag = True
	hitChance = 0
	activeChance = 0
	called = 0
	
	def startOfTurn(self, character):
		if self.called == 0:
			if randrange(1,101) <= self.activeChance:
				self.activate(character)
			elif isinstance(character.status, Paralyze):
				if self.printFlag:
					print character.name + " is still paralyzed but can move this turn"
				else:
					pass
			else:
				if self.printFlag:
					print character.name + " shakes off their condition and is healthy"
				character.status = Healthy()
				character.status.printFlag = self.printFlag
		else:
			pass
		
	def endOfTurn(self, character):
		pass
	def activate(self, character):
		pass
	def __repr__(self):
		return self.text
		
class Power:
	Name = ""
	def setName(self):
		self.Name = addSpacing(self.__class__.__name__)
	def offshoot(self):
		return []
	def setPreference(self, character):
		pass
	def __repr__(self):
		return self.__class__.__name__

class PowerPerk(perk, Power):
	pass
	
class PowerWeapon(Weapon, Power):
	def __init__(self, **weaponStats):
		pass
	
class PowerRestore(Restorative, Power):
	maxUses = 0
	pass
	
class PowerCure(Curative, Power):
	maxUses = 0
	pass
	
class PowerBuff(Buff, Power):
	maxUses = 0
	pass
	
class PowerDebuff(PowerBuff):
	magnitude = 0
	def applyDebuff(self, attack, mod=0):
		pass
	
		