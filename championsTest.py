from random import randrange

class City:
	def __init__(self, name, period, count, success):
		self.name = name
		self.period = period
		self.count = count
		self.success = success
		
class Champion:
	def __init__(self, city, success, time):
		self.city = city
		self.success = success
		self.time = time
		
antithan = City("Antithan", 6,3,65)
draimus = City("Draimus", 3,4,25)
phodela = City("Phodela", 6,5,45)
recomera = City("Recomera", 4,2,55)
sapydra = City("Sapydra", 4,2,55)
tutanethe = City("Tutanethe", 6,4,45)
cities = []
cities.append(antithan)
cities.append(draimus)
cities.append(phodela)
cities.append(recomera)
cities.append(sapydra)
cities.append(tutanethe)

champions = []
victors = {'Antithan':0,'Draimus':0,'Phodela':0,'Recomera':0,'Sapydra':0,'Tutanethe':0}
losers = {'Antithan':0,'Draimus':0,'Phodela':0,'Recomera':0,'Sapydra':0,'Tutanethe':0}

timePeriod = 12*100
f = open('championsOutput.txt', 'w')

for n in range(timePeriod):
	f.write('Year {0}, Month {1}\n'.format((n // 12)+1, (n % 12)+1))
	for c in cities:
		if n % c.period == 0:
			for i in range(0, c.count):
				chance = randrange(1,101)
				time = 36 + randrange(-6,7)
				champions.append(Champion(c.name, chance <= c.success, time))
			f.write(c.name + ' sends ' + str(c.count) + ' champions into Invidia\n')
	for c in champions:
		c.time -= 1
		if c.time == 0:
			if c.success:
				victors[c.city] += 1
				f.write('A champion from ' + c.city + ' succeeds\n')
			else:
				losers[c.city] += 1
				f.write('A champion from ' + c.city + ' has failed\n')
			champions.remove(c)
	f.write('\n')

f.write(str(victors) + "\n")
f.write(str(losers))