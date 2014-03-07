from __future__ import division
import io
from pprint import pprint
from datetime import datetime
from postingHelper import *

global posts
global chars
global members
global threads
posts = []
chars = {}
members = {}
threads = {}
file = open('postData.txt','r')
t = file.read()
text = t.split('\n')
dead = ["Afanc","Mariah","Icarus"]

for line in text:
	array = line.split('\t')
	try:
		m = members[array[1]]
	except:
		members[array[1]] = Member(array[1], array[3])
		m = members[array[1]]
	
	try:
		c = chars[array[0]]
	except:
		chars[array[0]] = Character(array[0],m)
		c = chars[array[0]]
	
	try:
		t = threads[array[2]]
	except:
		threads[array[2]] = Thread(array[2], array[4], array[5])
		t = threads[array[2]]
		
	posts.append(Post(datetime.strptime(array[7] + " 2014",'%b %d, %H:%M %Y'),c,t,int(array[6])))
	c.posts.append(posts[-1])
	t.posts.append(posts[-1])
	if c not in t.characters:
		t.characters.append(c)
	if c not in m.characters:
		m.characters.append(c)
	if t not in c.threads:
		c.threads.append(t)
		if t.active:
			c.activeThreads.append(t)

for t in threads.itervalues():
	t.sortPosts()
	for i, p in enumerate(t.posts):
		if i == 0 and t.open and len(t.posts) > 1:
			next = t.posts[1]
			if (next.character.name != p.character.name):
				x = (next.date - p.date).total_seconds() / (60 * 60)
				p.character.patience += x
				p.character.patienceCount += 1
			else:
				print "We are missing an entry in " + t.title
		elif i < (len(t.posts) - 1):
			next = t.posts[i+1]
			if (next.character.name != p.character.name):
				x = (next.date - p.date).total_seconds() / (60 * 60)
				p.character.patience += x
				p.character.patienceCount += 1
				next.character.slowness += x
				next.character.slownessCount += 1
			else:
				print "We are missing an entry in " + t.title
		elif t.active:
			next = datetime.now()
			last = t.posts[i-1]
			if (last.character.name != p.character.name):
				x = (next - p.date).total_seconds() / (60 * 60)
				p.character.patience += x
				p.character.patienceCount += 1
				last.character.slowness += x
				last.character.slownessCount += 1
		
def threadWhore(c):
	return sorted(c.values(), key=lambda x: len(x.activeThreads), reverse=True)[0]

def longThread(t, active=True):
	if active:
		return sorted([k for k in t.values() if k.active], key=lambda x: x.posts[-1].date - x.posts[0].date, reverse=True)
	else:
		return sorted(t.values(), key=lambda x: x.posts[-1].date - x.posts[0].date, reverse=True)
		
for m in members.itervalues():
	m.calcInfo()
	
#print "Biggest Thread Whore (Character)", threadWhore(chars), "\n"
#print "Biggest Thread Whore (Member)", threadWhore(members), "\n"

#These are 1, not zero, to balance the extreme cases of low posters and dead people
patient = sorted(members.values(), key=lambda x: x.patience / x.patienceCount, reverse=True)
patient[:] = [x for x in patient if x.name not in dead]
patient = patient[0:3]

patientC = sorted(chars.values(), key=lambda x: x.patience / x.patienceCount, reverse=True)
patientC[:] = [x for x in patientC if x.member.name not in dead]
patientC = patientC[0:3]

lazy = sorted(members.values(), key=lambda x: x.slowness / x.postCount, reverse=True)
lazy[:] = [x for x in lazy if x.name not in dead]
lazy = lazy[0:3]

lazyC = sorted(chars.values(), key=lambda x: x.slowness / x.postCount, reverse=True)
lazyC[:] = [x for x in lazyC if x.member.name not in dead]
lazyC = lazyC[0:3]

print "\nMost Patient Members"
for i in patient:
	print '\t{0}: Time Waited (Avg across {2} waits): {1:.2f} Hours'.format(i.name, i.patience / i.patienceCount, i.patienceCount)

print "\nMost Patient Characters"
for i in patientC:
	print '\t{0}: Time Waited (Avg across {2} waits): {1:.2f} Hours'.format(i.name, i.patience / i.patienceCount, i.patienceCount)

print "\nMost Waited For Members"
for i in lazy:
	print '\t{0}: Time Waited (Avg across {2} posts): {1:.2f} Hours'.format(i.name, i.slowness / i.postCount, i.postCount)

print "\nMost Waited For Characters"
for i in lazyC:
	print '\t{0}: Time Waited (Avg across {2} posts): {1:.2f} Hours'.format(i.name, i.slowness / i.postCount, i.postCount)
	
print

print 'Longest Threads By Time'
for i in longThread(threads, False)[0:3]:
	print "\t{0} {2} - {1}".format(i.title, i.showDuration(), i.characters)
print

print 'Longest Threads By Time (Active Only)'
for i in longThread(threads, True)[0:3]:
	print "\t{0} {2} - {1}".format(i.title, i.showDuration(), i.characters)
print

#Longest Thread (by Posts)
longPosts = sorted(threads.values(), key=lambda x: len(x.posts), reverse=True)[0:3]
print "Longest Threads By Posts"
for i in longPosts:
	print "\t{0} {2} - {1} Posts".format(i.title, len(i.posts), i.characters)
#Longest Thread (by Words)
longWords = sorted(threads.values(), key=lambda x: x.wordCount(), reverse=True)[0:3]
print "\nLongest Threads By Words"
for i in longWords:
	print "\t{0} {2} - {1:,} Words".format(i.title, i.wordCount(), i.characters)
#Longest Post
longPost = sorted(posts, key=lambda x: x.length, reverse=True)[0:3]
print "\nLongest Posts:"
for i in longPost:
	print "\t{0}".format(i)
