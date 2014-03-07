from __future__ import division
from random import randrange

count1 = 3
sides1 = 4
bonus1 = 6

count2 = 3
sides2 = 4
bonus2 = 4

def roller(c, s, b):
	total = [0]*(c*s+b+1)
	for i in range(s**c):
		score = (i % s) + 1 #First Die
		for k in range(1,c+1):
			score += ((i // (s**k)) % s) + 1 #Other Dice
		score += b	
		try:
			total[score-1] += 1 
		except:
			print score
	return total
	
max1 = sides1**count1
set1 = [round(i*100/max1,2) for i in roller(count1, sides1, bonus1)]
print 'From {0} to {1}'.format(count1 + bonus1, count1*sides1 + bonus1)
print set1

max2 = sides2**count2
set2 = [round(i*100/max2,2) for i in roller(count2, sides2, bonus2)]
print 'From {0} to {1}'.format(count2 + bonus2, count1*sides2 + bonus2)
print set2

while len(set1) > len(set2):
	set2.append(0)
while len(set2) > len(set1):
	set1.append(0)
	

def evaluate(s1, s2):
	winChance = 0
	tieChance = set1[0]*set2[0]
	for i in range(1,len(set1)):
		win = 0
		for k in range(i):
			win += set2[k]
		winChance += set1[i]*win/(100**2)
		tieChance += set1[i]*set2[i]/(100**2)
		
	loseChance = 1 - (winChance + tieChance)
	print "Set 1 Wins {0:3.2f}% of the time".format(winChance*100)
	print "They tie {0:3.2f}% of the time".format(tieChance*100)
	print "Set 2 Wins {0:3.2f}% of the time".format(100*loseChance)

evaluate(set1, set2)