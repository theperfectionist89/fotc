class object:
	def func(self):
		print "hello"
	def __init__(self, a):
		#this is a constructor
		self.master = "Grant"
		self.text = a
		
class childObject(object):
	pass
		
class Character:
	def __init__():
		#initialise stats
		pass
		
	def dealPhysical(self, target, power, acc, crit, allowTriggers=True):
		#do combat shit
		#check reactive abilities on target
		pass

	def poisonBite(self, target):
		#do shit if you has abilities
		#dealPhysical(self,target, 4, 80,
		#applyCond
		pass

class Perk:
	def affectPhysical(self, attack):
		pass

class Invuln1(Perk):
	def affectPhysical(self, attack):
		attack.maxDamage = 0
		
tester = childObject()
print tester.master