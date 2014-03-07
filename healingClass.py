from __future__ import division
from statusClasses import *
from perkBuff import *
from baseClasses import *
import re
		
class MinorHealingPotion(Restorative):
	healAmt = 10

class LightHealingPotion(Restorative):
	healAmt = 20	

class MediumHealingPotion(Restorative):
	healAmt = 30	
			
class GreaterHealingPotion(Restorative):
	healAmt = 50
	
class MaxHealingPotion(Restorative):
	healPct = 100
	
class MinorPurificationPotion(Restorative):
	pureAmt = 10

class LightPurificationPotion(Restorative):
	pureAmt = 20	

class MediumPurificationPotion(Restorative):
	pureAmt = 30	
			
class GreaterPurificationPotion(Restorative):
	pureAmt = 50
	
class MaxPurificationPotion(Restorative):
	purePct = 100
	
class ParalysisHeal(Curative):
	cures = "Paralyzed"
	def cureStatus(self, character, printFlag):
		if uses > 0 and self.currentCooldown == 0 and isinstance(character.status, Paralyze):
			character.status = Healthy()
			self.uses -= 1
			self.currentCooldown = self.cooldown
			if printFlag:
				'\t' + character.name + ' cured his/her Paralysis using ' + self.text()
			
class BurnHeal(Curative):
	cures = "Burned"
	def cureStatus(self, character, printFlag):
		if uses > 0 and self.currentCooldown == 0 and isinstance(character.status, Burn):
			character.status = Healthy()
			self.uses -= 1
			self.currentCooldown = self.cooldown
			if printFlag:
				'\t' + character.name + ' cured his/her Burn using ' + self.text()

class BloodClotPotion(Curative):
	cures = "Bleeding"
	def cureStatus(self, character, printFlag):
		if uses > 0 and self.currentCooldown == 0 and isinstance(character.status, Bleed):
			character.status = Healthy()
			self.uses -= 1
			self.currentCooldown = self.cooldown
			if printFlag:
				'\t' + character.name + ' cured his/her Bleeding using ' + self.text()
			
class ObliviationPotion(Curative):
	cures = "Captivated"
	def cureStatus(self, character, printFlag):
		if uses > 0 and self.currentCooldown == 0 and isinstance(character.status, Attract):
			character.status = Healthy()
			self.uses -= 1
			self.currentCooldown = self.cooldown
			if printFlag:
				'\t' + character.name + ' cured his/her Captivation using ' + self.text()
				
class GeneralAntidote(Curative):
	cures = "Poisoned"
	def cureStatus(self, character, printFlag):
		if uses > 0 and self.currentCooldown == 0 and isinstance(character.status, Poison):
			character.status = Healthy()
			self.uses -= 1
			self.currentCooldown = self.cooldown
			if printFlag:
				'\t' + character.name + ' cured his/her Poisoning using ' + self.text()
			
class SmellingSalts(Curative):
	cures = "Confused"
	def cureStatus(self, character, printFlag):
		if uses > 0 and self.currentCooldown == 0 and isinstance(character.status, Confuse):
			character.status = Healthy()
			self.uses -= 1
			self.currentCooldown = self.cooldown
			if printFlag:
				'\t' + character.name + ' cured his/her Confusion using ' + self.text()
			
class AntiFreezeTalisman(Curative):
	cures = "Frozen"
	def cureStatusAuto(self, character, attack):
		if uses > 0 and self.currentCooldown == 0 and isinstance(character.status, Freeze):
			character.status = Healthy()
			self.uses -= 1
			self.currentCooldown = self.cooldown
			attack.perkinfo.append('\t' + character.name + ' cured his/her Sleep using ' + self.text())
			
class AntiSleepTalisman(Curative):
	cures = "Asleep"
	def cureStatusAuto(self, character, attack):
		if self.uses > 0 and self.currentCooldown == 0 and isinstance(character.status, Sleep):
			character.status = Healthy()
			self.uses -= 1
			self.currentCooldown = self.cooldown
			attack.perkinfo.append('\t' + character.name + ' cured his/her Sleep using ' + self.text())
			
class AntiStunTalisman(Curative):
	cures = "Stunned"
	def cureStatusAuto(self, character, attack):
		if self.uses > 0 and self.currentCooldown == 0 and isinstance(character.status, Stun):
			character.status = Healthy()
			self.uses -= 1
			self.currentCooldown = self.cooldown
			attack.perkinfo.append('\t' + character.name + ' cured his/her Stun using ' + self.text())
			
class SpeedPill(Buff):
	def applyBuff(self, character, printFlag=False):
		character.Perks.append(SpeedPillBuff())
		self.useBuff()
		if printFlag:
			print '\t' + character.name + " boosts his/her Agility with a Speed Pill"
			
class NoItem(Healing):
	pass