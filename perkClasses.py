from statusClasses import *
import re, traceback
from baseClasses import *
from perkBuff import *

		
class Flight(perk):
	def modifyCharacterPreCombat(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.power -= 3
		character.agility +=3
	def modifyCharacterPostCombat(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.power += 3
		character.agility -=3
	
class AerialCombat(perk):
	def modifyCharacterPreCombat(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.power += 3
		character.luck += 3	
	def modifyCharacterPostCombat(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.power -= 3
		character.luck -=3
class AromaVeil(perk):
	def modifyDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		if attack.weapon.Category == "Tease":
			attack.defense += 5
			attack.perkinfo.append("\t" + attack.defender.name + " was protected by Aroma Veil")
class BattleArmour(perk):
	def modifyCritDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		attack.crit = -999
class Clarity(perk):
	#immune confuse
	def statusImmunity(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		if isinstance(character.status, Confuse):
			character.status = Healthy()
class Cryogenics(perk):
	#immune freeze
	def statusImmunity(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		if isinstance(character.status, Freeze):
			character.status = Healthy()
class CuteCharm(perk):
	#if hit by category phys opponent may be captivated
	def modifyAfterDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):	
		if attack.weapon.Category == "Physical" and attack.damage > 0:
			statuses = __import__('statusClasses')
			status = statuses.Attract()
			statusChance = status.hitChance - attack.attacker.resistance
			if randrange(1,101) <= statusChance and isinstance(attack.attacker.status, Healthy):
				attack.perkinfo.append('\t' + attack.defender.name + "'s Cute Charm activates")
				attack.attacker.status = status
				for perk in attack.attacker.Perks:
					perk.statusImmunity(attack.attacker)
				if isinstance(attack.attacker.status, Healthy):
					attack.perkinfo.append('\t' + attack.attacker.name + " is immune to being " + status.text)
				else:
					attack.perkinfo.append('\t' + attack.attacker.name + " is now " + status.text)
		
class FireResistance(perk):
	def modifyDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		if attack.weapon.DmgType == "Fire":
			attack.defense = 999
			attack.perkinfo.append(attack.defender.name + " is immune to Fire damage")
class FlameBody(perk):
	#immune to burning
	def statusImmunity(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		if isinstance(character.status, Burn):
			character.status = Healthy()
class Flexibility(perk):
	def modifyCharacterPreCombat(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.agility += 3
	def modifyCharacterPostCombat(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.agility -=3
class Immunity(perk):
	# immune to poison
	def statusImmunity(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		if isinstance(character.status, Poison):
			character.status = Healthy()
class InnerFocus(perk):
	# immunity to stun
	def statusImmunity(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		if isinstance(character.status, Stun):
			character.status = Healthy()
class Insomnia(perk):
	#immunity to sleep
	def statusImmunity(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		if isinstance(character.status, Sleep):
			character.status = Healthy()
class KeenEyes(perk):
	def modifyAccuracyOffense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		attack.acc +=30
class Limber(perk):
	#immune paralyze
	def statusImmunity(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		if isinstance(character.status, Paralyze):
			character.status = Healthy()
class LuckoftheIrish(perk):
	#+3 luck
	def modifyCharacterPreCombat(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.luck += 3
	def modifyCharacterPostCombat(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.luck -=3
class Masochist(perk):
	#trade 3 physical for lust 
	def modifyDamageDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		if attack.weapon.Category == "Physical" and attack.damage > 0:
			attack.damage = max(0,attack.damage - 3)
			attack.defender.currentLust += 3
class MasterHealer(perk):
	#healing item +5
	def modifyHealing(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		return amount + 5
class Miracle(perk):
	uses = 1
	# live at one health once
	def modifyAfterDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character = attack.defender
		if self.uses > 0 and character.currentHP <= 0:
			self.uses -= 1
			character.currentHP = 1
			attack.perkinfo.append("\t" + character.name + " survives with 1 HP thanks to Miracle")
		elif self.uses > 0 and character.currentLust >= character.MaxLust:
			self.uses -= 1
			character.currentLust = character.MaxLust - 1
			attack.perkinfo.append("\t" + character.name + " hangs on by one Lust point thanks to Miracle")
				
class NervesofSteel(perk):
	def modifyOffense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		if attack.attacker.resistance >= attack.defender.resistance + 10:
			attack.offense += 5
			attack.perkinfo.append("\t" + attack.attacker.name + " is empowered by Nerves of Steel")
class NoGuard(perk):
	def modifyAccuracyOffense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		attack.acc = 999
		attack.perkinfo.append("\tNo Guard makes all attacks hit")
	def modifyAccuracyDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		attack.acc = 999
		attack.perkinfo.append("\tNo Guard makes all attacks hit")
class Oblivious(perk):
	#immune captivation
	def statusImmunity(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		if isinstance(character.status, Attract):
			character.status = Healthy()
class Sadist(perk):
	#deal +3 physical take that much lust
	def modifyDamageOffense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		if attack.weapon.Category == "Physical" and attack.damage > 0:
			attack.damage += 3
			attack.attacker.currentLust += 3
class Stealth(perk):
	def modifySkills(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.skills["Stealth"] +=5
		
class ThickFat(perk):
	#take half damage from elemental effects
	def modifyDamageDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		if attack.weapon.Type == "Elemental":
			attack.damage /= 2
			attack.perkinfo.append("\t" + attack.defender.name + " was protected by Thick Fat")
#irrelevant(see flight)
class DragonFlightI(Flight):
	pass
class HarpyFlightI(Flight):
	pass

#irrelevant(see attack)
class BeautifulBirdIII(perk, PerkWeapon):
	pass
class Constriction(perk, PerkWeapon):
	pass
class DangerousBeauty(perk, PerkWeapon):
	pass
class DeathGazeII(perk, PerkWeapon):
	pass
class DeathGazeIII(perk, PerkWeapon):
	pass
class EnticeI(perk, PerkWeapon):
	pass
class EnticeII(perk, PerkWeapon):
	pass
class EnticeIII(perk, PerkWeapon):
	pass	
class FireBreathI(perk, PerkWeapon):
	pass
class FireBreathII(perk, PerkWeapon):
	pass
class FireBreathIII(perk, PerkWeapon):
	pass
class FullMoon(perk, PerkWeapon):
	pass
class HealingFireII(perk, PerkWeapon):
	pass
class HealingFireIII(perk, PerkWeapon):
	pass
class HornAttack(perk, PerkWeapon):
	pass
class PoisonedFangII(perk, PerkWeapon):
	pass
class PoisonedFangIII(perk, PerkWeapon):
	pass
class Slam(perk, PerkWeapon):
	pass
class HeavySlam(perk, PerkWeapon):
	pass
class Peck(perk, PerkWeapon):
	pass
class RazorClaw(perk, PerkWeapon):
	pass
class Kick(perk, PerkWeapon):
	pass
class Charge(perk, PerkWeapon):
	pass
class Trample(perk, PerkWeapon):
	pass
class TripleBite(perk, PerkWeapon):
	pass
class Claw(perk, PerkWeapon):
	pass
class PoisonedClawsI(perk, PerkWeapon):
	pass
class PoisonedClawsII(perk, PerkWeapon):
	pass
class PoisonedClawsIII(perk, PerkWeapon):
	pass	
	
#Modify Skills
class EscapeArtist(perk):
	flag = True
	def modifyFlee(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.skills["Escape"] += 7
	def modifyFleeAfter(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.skills["Escape"] -= 7
	def modifyDamageDefense(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		if self.flag and attack.defender.strategy.runFailed:
			attack.damage *= 1.5
			attack.damage = int(attack.damage)
			self.flag = False
class ExperiencedHunter(perk):
	def modifySkills(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.skills["Scavenge"] += 5
class HeavyLoad(perk):
	def modifySkills(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.skills["Carry"] += 5
class Intellectual(perk):
	def modifySkills(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.skills["Knowledge"] += 5
class Intimidating(perk):
	def modifySkills(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.skills["Intimidate"] += 5
class Perceptive(perk):
	def modifySkills(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.skills["Perception"] += 5
class Scrounger(perk):
	def modifySkills(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.skills["Search"] += 5
class SenseMotive(perk):
	def modifySkills(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.skills["Suspicion"] += 5
class SnakeCharmer(perk):
	def modifySkills(self, character = None, enemy = None, attack = None, amount = None, printFlag = True):
		character.skills["Charm"] += 5
	

#irrelevant Most likely
class AnalyticalMind(perk):
	pass
	
#Irrelevant - See Buffs	
class Duplication(perk, Buff):
	def applyBuff(self, character, printFlag=False):
		character.Perks.append(DuplicationBuff())
		self.useBuff()
		if printFlag:
			print '\t' + character.name + " creates a duplicate of him/herself"

#irrelevant
class AbsoluteDirection(perk):
	pass
class Adventurer(perk):
	pass
class AncientArtefacts(perk):
	pass
class ArousingAura(perk):
	pass
class Attunement(perk):
	pass
class BeautifulBirdI(perk):
	pass
class BeautifulBirdII(perk):
	pass
class Camouflage(perk):
	pass
class Concubine(perk):
	pass
class CorruptDisguise(perk):
	pass
class CursedBody(perk):
	pass
class DeathGazeI(perk):
	pass
class Desecration(perk):
	pass
class Diplomat(perk):
	pass
class DisguisingIllusions(perk):
	pass
class DragonFlightII(perk):
	pass
class DragonFlightIII(perk):
	pass
class EarthSense(perk):
	pass
class FairyWings(perk):
	pass
class FastLearner(perk):
	pass
class FeedingI(perk):
	pass
class FeedingII(perk):
	pass
class Haggler(perk):
	pass
class HarpyFlightII(perk):
	pass
class HarpyFlightIII(perk):
	pass
class HealingFireI(perk):
	pass
class HealingMilk(perk):
	pass
class HighDefenses(perk):
	pass
class HighJump(perk):
	pass
class KitsuneTransformationI(perk):
	pass
class KitsuneTransformationII(perk):
	pass
class KitsuneTransformationIII(perk):
	pass
class Labourer(perk):
	pass
class MemoryCharm(perk):
	pass
class MidasTouch(perk):
	pass
class PhoenixTransformationI(perk):
	pass
class PhoenixTransformationII(perk):
	pass
class PhoenixTransformationIII(perk):
	pass
class PoisonedFangI(perk):
	pass
class Prestidigitation(perk):
	pass
class Purification(perk):
	pass
class QuietFeet(perk):
	pass
class RecklessAbandon(perk):
	pass
class RespawnControl(perk):
	pass
class StarAcrobat(perk):
	pass
class Tanking(perk):
	pass
class TheCollector(perk):
	pass
class Unaffected(perk):
	pass
class WebTrapping(perk):
	pass
class WellPrepared(perk):
	pass
class CultLeaderKnowledge(perk):
	pass
class CultKnowledge(perk):
	pass