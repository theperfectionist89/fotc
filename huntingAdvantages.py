class Advantage:
	mods = {
		"Small":1,
		"Medium":2,
		"Large":3,
		"Inedible":4,
		"NPC":0
	}
	def modifyMeatDamage(self, hunt, attack):
		pass
	def modifyPeltDamage(self, hunt, attack):
		pass
	def modifySkills(self, hunt):
		pass
		
class CarefulHunter(Advantage):
	def modifyMeatDamage(self, hunt, attack):
		if attack.weapon.DmgType == "Bludgeoning":
			hunt.meatDmg = 1
			
	def modifyPeltDamage(self, hunt, attack):
		if attack.weapon.DmgType in ["Piercing","Slashing"]:
			hunt.peltDmg = 1
			
class Gentle(Advantage):
	def modifyPeltDamage(self, hunt, attack):
		if hunt.start == True:
			hunt.peltDmg = 0
			
class Humane(Advantage):
	def modifyMeatDamage(self, hunt, attack):
		if hunt.start == True:
			hunt.meatDmg = 0
			
class LightStep(Advantage):
	def modifySkills(self, hunt):
		mod = self.mods[hunt.prey.Type]*3
		hunt.pred.skills["Stealth"] += mod
		
class SwiftHunter(Advantage):
	def modifySkills(self, hunt):
		mod = self.mods[hunt.prey.Type]*3
		hunt.pred.skills["Acrobatics"] += mod
		
class Brutal(Advantage):
	def modifyMeatDamage(self, hunt, attack):
		if hunt.start == True:
			hunt.meatDmg *= 2
			
class Careless(Advantage):
	def modifyPeltDamage(self, hunt, attack):
		if hunt.start == True:
			hunt.peltDmg *= 2
			
class Rowdy(Advantage):
	def modifySkills(self, hunt):
		mod = (5-self.mods[hunt.prey.Type])*3
		hunt.pred.skills["Stealth"] -= mod
		
class SlowHunter(Advantage):
	def modifySkills(self, hunt):
		mod = (5-self.mods[hunt.prey.Type])*3
		hunt.pred.skills["Acrobatics"] -= mod
		
class SloppyHunter(Advantage):
	def modifyMeatDamage(self, hunt, attack):
		if attack.weapon.DmgType in ["Piercing","Slashing"]:
			hunt.meatDmg = 2
			
	def modifyPeltDamage(self, hunt, attack):
		if attack.weapon.DmgType == "Bludgeoning":
			hunt.peltDmg = 2

class Slothful(Advantage):
	pass
	
class Impatient(Advantage):
	pass
	
#NPC Advantages
class Skittish(Advantage):
	def modifySkills(self, hunt):
		mod = round(hunt.prey.Level / 2,0)
		hunt.prey.skills["Escape"] += mod
		
class Determined(Advantage):
	def modifySkills(self, hunt):
		mod = round(hunt.prey.Level / 2,0)
		hunt.prey.skills["Escape"] -= 3
		
class Observant(Advantage):
	def modifySkills(self, hunt):
		mod = round(hunt.prey.Level / 2,0)
		hunt.prey.skills["Perception"] += 3

class Blind(Advantage):
	def modifySkills(self, hunt):
		mod = round(hunt.prey.Level / 2,0)
		hunt.prey.skills["Perception"] -= 3