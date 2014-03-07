from statusClasses import *
from healingClass import *
from functions import addSpacing
from perkBuff import *
from baseClasses import *
import traceback

'''
Rules of Thumb For Defining Powers:
- Offshoots are treated as the tier they offshooted from
- Perks are the equivalent of tier 1, unless they level up
- If a power modifies the stats of either combatant, the following guideline should be used:
---Tier 1: +/- 3 (Permanent), +/- 5 (Conditional or Temporary)
---Add 2 to a given category for every Tier it increases.
---Double this if the buff affects accuracy/dodge rates
'''

'''
Rules for printing with printFlag
- If it is a PreCombat effect, end it with a new line (\n)
- Otherwise, start it with a tab (\t)
'''

weaponData = None


#****************************************

class BloodCurse(PowerPerk):
	Name = "Blood Curse"
	def modifyCharacterPreCombat(self, character, enemy=None, printFlag=True):
		character.status = Bleed()
		if printFlag:
			print character.name + " is Bleeding thanks to Blood Blades\n"

class BloodBladesI(PowerWeapon):
	Name = "Blood Blades I"
	def offshoot(self):
		return [BloodCurse()]
	
class BloodBullets(PowerWeapon):
	Name = "Blood Bullets"
			
class BloodBladesII(BloodBladesI):
	Name = "Blood Blades II"
	def offshoot(self):
		try:
			offshootList = BloodBladesI.offshoot(self)
			offshootList.extend([BloodBullets()])
			return offshootList
		except:
			print traceback.format_exc()
		
class DeathTrigger(PowerPerk):
	Name = "Death Trigger"
	hpThresh = 0.2
	lustThresh = 0.8
	def modifyAfterDefense(self, attack):
		dfn = attack.defender
		prior = 0
		if dfn.currentHP <= self.hpThresh*dfn.MaxHP or dfn.currentLust >= self.lustThresh*dfn.MaxLust:
			dfn.attacks['Blood Explosion'] = Weapon(**weaponData['Blood Explosion'])
			for i in dfn.attacks.itervalues():
				if str(i) == "Blood Explosion":
					i.Priority = 0
			for i in dfn.attacks.itervalues():
				i.Priority += 1
	def modifyCharacterPostCombat(self, character, enemy=None, printFlag=True):
		try:
			del character.attacks['Blood Explosion']
		except:
			pass
		
class BloodExplosion(PowerWeapon):
	Name = "Blood Explosion"
	
class BloodDeath(PowerPerk):
	Name = "Blood Death"
	def modifyAfterOffense(self, attack):
		if attack.weapon.Name == "Blood Explosion":
			attack.attacker.currentHP = 0
			attack.perkinfo.append('\t' + attack.attacker.name + " explodes in a fountain of blood and dies")
		
class BloodBladesIII(BloodBladesII):
	Name = "Blood Blades III"
	def offshoot(self):
		try:
			offshootList = BloodBladesII.offshoot(self)
			offshootList.extend([BloodDeath(),DeathTrigger()])#BloodExplosion(),
			return offshootList
		except:
			print traceback.format_exc()
		
class BloodBladesIV(BloodBladesIII):
	Name = "Blood Blades IV"
	#Offshoot doesn't apply to combat
		
class ReactiveAdaptionI(PowerPerk):
	Name = "Reactive Adaption I"
	#Level 1 - Half damage from physical attacks if used in succession
	lastAttack = "None"
	def modifyDamageDefense(self, attack):
		if self.lastAttack == attack.weapon.DmgType and self.weapon.Category == "Physical" and attack.damage > 0:
			attack.damage /= 2
			attack.perkinfo.append("\t" + attack.defender.name + " has adapted to physical attacks and takes less damage")
		elif attack.damage > 0:
			self.lastAttack = attack.weapon.DmgType
	def modifyCharacterPostCombat(self, character, enemy=None, printFlag=True):
		self.lastAttack = "None"
	
class ReactiveAdaptionII(ReactiveAdaptionI):
	Name = "Reactive Adaption II"
	#Level 2 - No damage from attacks if used in succession
	#Offshoot - Resistance applies to all Damage Types, not just Physical
	lastAttack = "None"
	def modifyDamageDefense(self, attack):
		if self.lastAttack == attack.weapon.DmgType and attack.damage > 0:
			attack.damage = 0
			attack.perkinfo.append("\t" + attack.defender.name + " has adapted to " + attack.weapon.DmgType +" attacks and took no damage")
		elif attack.damage > 0:
			self.lastAttack = attack.weapon.DmgType
	def modifyCharacterPostCombat(self, character, enemy=None, printFlag=True):
		self.lastAttack = "None"
		
class PheromoneControlI(PowerWeapon):
	Name = "Pheromone Control I"
	
class DesireAmplification(PowerPerk):
	Name = "Desire Amplification"
	def modifyOffense(self, attack):
		if attack.weapon.DmgType == "Lust":
			attack.defense -= 6
			attack.perkinfo.append("\t" + attack.attacker.name + " amplifies " + attack.defender.name + "'s desires, making him/her weaker to Lust attacks")
	
class PheromoneControlII(PheromoneControlI):
	Name = "Pheromone Control II"
	def offshoot(self):
		try:
			offshootList = PheromoneControlI.offshoot(self)
			offshootList.extend([DesireAmplification()])
			return offshootList
		except:
			print traceback.format_exc()
	
class DesireNegation(PowerBuff):
	Name = "Desire Negation"
	def applyBuff(self, character, printFlag=False):
		character.Perks.append(DesireNegationBuff())
		self.useBuff()
		if printFlag:
			print '\t' + character.name + " bolsters her Resistance with Desire Negation"	
	
class PheromoneControlIII(PheromoneControlII):
	Name = "Pheromone Control III"
	def offshoot(self):
		try:
			offshootList = PheromoneControlII.offshoot(self)
			offshootList.extend([DesireNegation()])
			return offshootList
		except:
			print traceback.format_exc()
	
class ElectricManipulationI(PowerWeapon):
	Name = "Electric Manipulation I"
	
class ElectricManipulationII(ElectricManipulationI):
	Name = "Electric Manipulation II"
	#Offshoot not relevant

class ElectricWeapons(PowerWeapon):
	Name = "Electric Weapons"
	
class ElectricManipulationIII(ElectricManipulationII):
	Name = "Electric Manipulation III"
	def offshoot(self):
		try:
			offshootList = ElectricManipulationII.offshoot(self)
			offshootList.extend([ElectricWeapons()])
			return offshootList
		except:
			print traceback.format_exc()

class WarlordArmourI(PowerPerk):
	Name = "Warlord Armour I"
	def modifyCritDefense(self,attack):
		attack.crit = -999
			
class WarlordClaws(PowerWeapon):
	Name = "Warlord Claws"
	
class WarlordArmourII(WarlordArmourI):
	Name = "Warlord Armour II"
	def statusImmunity(self, character):
		if isinstance(character.status, Bleed):
			character.status = Healthy()
	def offshoot(self):
		return [WarlordClaws()]

class WarlordAura(PowerPerk):
	'''Description:
	Your very presence fills the lesser willed with fear,
	rendering them weak. Creatures whose Resistance is
	lower than your Energy take a -3 penalty on Energy,
	Skill, and Agility
	'''
	def modifyCharacterPreCombat(self, character, enemy, printFlag):
		if character.energy > enemy.resistance:
			enemy.energy -= 3
			enemy.skill -= 3
			enemy.agility -= 3
			if printFlag:
				print enemy.name + " is weakened by " + character.name + "'s Warlord Aura\n"
		else:
			if printFlag:
				print enemy.name + " resists " + character.name + "'s Warlord Aura\n"
		
class WarlordArmourIII(WarlordArmourII):
	Name = "Warlord Armour III"
	def statusImmunity(self, character):
		if isinstance(character.status, Bleed) or isinstance(character.status, Kill):
			character.status = Healthy()
	def offshoot(self):
		try:
			offshootList = WarlordArmourII.offshoot(self)
			offshootList.extend([WarlordAura()])
			return offshootList
		except:
			print traceback.format_exc()
			
class GravityManipulationI(PowerDebuff):
	#Status Attack - Physical
	Name = "Gravity Manipulation I"
	def applyDebuff(self, attack, mod=0):
		attack.defender.Perks.append(GravityManipulationIDebuff(mod))
		self.useBuff()
		attack.perkinfo.append(" slowing " + attack.defender.name)
			
class EnergyBowI(PowerWeapon):
	Name = "Energy Bow I"
	def setPreference(self, character):
		t = ""
		options = ['Fire','Ice','Poison','Electric','Energy','Sonic']
		status = ['Burn','Freeze','Poison','Paralyze','Confuse','Stun']
		t = raw_input('What type of damage will ' + character.name + "'s Energy Bow do this battle? ")
		while t not in options:
			print "Choose from", options
			t = raw_input('What type of damage will Energy Bow do this battle? ')
		character.attacks[self.Name].DmgType = t
		if self.Name in ["Energy Bow II", "Energy Bow III"]:
			character.attacks[self.Name].Special = status[options.index(t)]
		if self.Name == "Energy Bow III":
			character.attacks["Rain Of Arrows"].DmgType = t
		
class EnergyBowII(EnergyBowI):
	Name = "Energy Bow II"
	#Offshoot Charged Arrow is built in
		
class RainOfArrows(PowerWeapon):
	Name = "Rain Of Arrows"
		
class EnergyBowIII(EnergyBowII):
	Name = "Energy Bow III"
	def offshoot(self):
		try:
			offshootList = EnergyBowII.offshoot(self)
			offshootList.extend([RainOfArrows()])
			return offshootList
		except:
			print traceback.format_exc()
		
class InvulnerabilityI(PowerBuff):
	cooldown = 6
	def applyBuff(self, character, printFlag=False):
		character.Perks.append(InvulnerabilityIBuff())
		self.useBuff()
		if printFlag:
			print '\t' + character.name + " becomes invulnerable to health damage"
			
class InvulnerabilityII(InvulnerabilityI):
	#Offshoot gets absorbed into this
	maxUses = 99
	cooldown = 6
	def applyBuff(self, character, printFlag=False):
		character.Perks.append(InvulnerabilityIIBuff())
		self.useBuff()
		if printFlag:
			print '\t' + character.name + " becomes invulnerable to all damage and status effects"
	
class MentalBacklash(PowerPerk):
	def statusDefense(self, attack):
		if attack.weapon.DmgType == "Mental" and isinstance(attack.attacker.status, Healthy):
			attack.attacker.status = Stun()
			attack.perkinfo.append('\t' + attack.attacker.name + " is stunned by " + attack.defender.name + "'s Mental Backlash I")
		elif attack.weapon.DmgType == "Mental":
			attack.attacker.currentHP -= 3
			attack.perkinfo.append('\t' + attack.attacker.name + " takes 3 damage from " + attack.defender.name + "'s Mental Backlash I")
	
class MentalShieldI(PowerPerk):
	def statusDefense(self, attack):
		if attack.weapon.DmgType == "Mental":
			attack.statusDefense += attack.defender.resistance #Double resistance against mental attacks
			attack.perkinfo.append('\t' + attack.defender.name + " is protected from mental attacks by Mental Shield I")

class MentalShieldII(MentalShieldI):
	#Offshoot built in
	def statusDefense(self, attack):
		if attack.weapon.DmgType in ["Mental","Emotional"]:
			attack.statusDefense += attack.defender.resistance #Double resistance
			attack.perkinfo.append('\t' + attack.defender.name + " is protected from " + attack.weapon.DmgType + " attacks by Mental Shield II")
	def offshoot(self):
		try:
			offshootList = MentalShieldI.offshoot(self)
			offshootList.append(MentalBacklash())
			return offshootList
		except:
			print traceback.format_exc()

class SenseManipulationI(PowerDebuff):
	#Status Attack - Physical
	Name = "Sense Manipulation I"
	def applyDebuff(self, attack, modifier):
		attack.defender.Perks.append(SenseManipulationIDebuff())
		self.useBuff()
		attack.perkinfo.append(" making " + enemy.name + " more sensitive to pain")

class SenseManipulationII(SenseManipulationI):
	#Status Attack - Physical
	Name = "Sense Manipulation II"
	def applyDebuff(self, attack, modifier):
		attack.defender.Perks.append(SenseManipulationIIDebuff())
		self.useBuff()
		attack.perkinfo.append(" making " + enemy.name + " more sensitive to pain")

class DampeningField(PowerPerk):
	Name = "Dampening Field"
	def modifyCooldownOffense(self, attack):
		if isinstance(attack.weapon, Power) and attack.weapon.currentCooldown>0:
			attack.weapon.currentCooldown += 2
	def modifyCooldownDefense(self, attack):
		if isinstance(attack.weapon, Power) and attack.weapon.currentCooldown>0:
			attack.weapon.currentCooldown += 2
			
class PyrokinesisI(PowerWeapon):
	Name = "Pyrokinesis I"			
			
#Non-Combat Powers
class UmbrakinesisI(Power):
	pass 