from perkClasses import perk
class Armour(perk):
	def __init__(self, **armourStats):
		self.__dict__.update(armourStats)

	def __repr__(self):
		return self.Name	
		
	def modifyCharacterPreCombat(self, character, enemy=None, printFlag=True):
		character.power += self.STR
		character.defense += self.TGH
		character.agility += self.SPE
		character.energy += self.CHA
		character.resistance += self.SPI
		character.luck += self.LCK
		character.skill += self.INT
		
	def modifyCharacterPostCombat(self, character, enemy=None, printFlag=True):
		character.power -= self.STR
		character.defense -= self.TGH
		character.agility -= self.SPE
		character.energy -= self.CHA
		character.resistance -= self.SPI
		character.luck -= self.LCK
		character.skill -= self.INT