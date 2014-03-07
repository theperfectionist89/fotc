from __future__ import division

class Skill:
	def __init__(self, character):
		self.chr = character
		
	def getValue(self):
		pass
		
class Escape(Skill):
	def getValue(self):
		return int(self.chr.SPE / 4)
		
class Intimidate(Skill):
	def getValue(self):
		return int(self.chr.CHA / 6 + self.chr.STR / 12)
		
class Charm(Skill):
	def getValue(self):
		return int(self.chr.CHA / 4)
		
class Search(Skill):
	def getValue(self):
		return int(self.chr.INT / 6 + self.chr.SPI / 12)
		
class Stealth(Skill):
	def getValue(self):
		return int(self.chr.SPE / 6 + self.chr.INT / 12)