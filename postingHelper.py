class Character:
	member = None
	group = ""
	name = ""
	wordCount = 0
	postCount = 0
	patience = 0
	slowness = 0
	patienceCount = 0
	slownessCount = 0
	threads = []
	activeThreads = []
	posts = []
	def __init__(self, name, member):
		self.name = name
		self.member = member
		self.posts = []
		self.threads = []
		self.activeThreads = []
		self.group = ""
		self.wordCount = 0
		self.postCount = 0
		self.patience = 0
		self.slowness = 0
		self.patienceCount = 0
		self.slownessCount = 0
	
	def calcInfo(self):
		self.wordCount = 0
		self.postCount = 0
		for p in self.posts:
			self.wordCount += p.length
			self.postCount += 1
	
	def __repr__(self):
		return self.name
		
	def fullPrint(self):
		return '\nName: {3}\nMember: {0}\nPosts: {2}\nWords: {1:,}\nThreads: {4} ({5} Active)'.format(self.member.name, self.wordCount, self.postCount, self.name, len(self.threads), len(self.activeThreads))
		
class Member:
	name = ""
	characters = []
	wordCount = 0
	postCount = 0
	patience = 0
	slowness = 0
	posts = []
	threads = []
	activeThreads = []
	group = ""
	patienceCount = 0
	slownessCount = 0
	def __init__(self, name, group):
		self.name = name
		self.characters = []
		self.threads = []
		self.activeThreads = []
		self.group = group
		self.calcInfo()
	def calcInfo(self):
		self.patience = 0
		self.slowness = 0
		self.patienceCount = 0
		self.slownessCount = 0
		self.getPosts()
		self.wordCount = 0
		self.postCount = 0
		for p in self.posts:
			self.wordCount += p.length
			self.postCount += 1
	def getPosts(self):
		self.posts = []
		for c in self.characters:
			c.calcInfo()
			self.posts.extend(c.posts)
			self.threads.extend(c.threads)
			self.patience += c.patience
			self.patienceCount += c.patienceCount
			self.slowness += c.slowness
			self.slownessCount += c.slownessCount
		self.activeThreads = [i for i in self.threads if i.active]
	
	def getPrimary(self):
		self.primary = sorted(self.characters, key=lambda x: x.wordCount, reverse=True)[0]
	def __repr__(self):
		self.getPrimary()
		return '\nName: {0}\nPrimary: {4}\nPosts: {2}\nWords: {1:,}\nThreads: {3} ({7} Active)\nPatience: {5:4.2f} Hours\nSlowness: {6:4.2f} Hours'.format(self.name, self.wordCount, self.postCount, len(self.threads), self.primary.name, self.patience, self.slowness, len(self.activeThreads))
		
class Post:
	date = None
	character = None
	thread = None
	length = 0
	def __init__(self, date, character, thread, length):
		self.date = date
		self.character = character
		self.thread = thread
		self.length = length
	def __repr__(self):
		dateFormat = self.date.strftime("%b %d, %Y %H:%M")
		return '{1} in {2} ({0}) for {3:,} words'.format(dateFormat, self.character.name, self.thread.title, self.length)
	
class Thread:
	title = ""
	posts = []
	characters = []
	active = True
	def __init__(self, title, active, open):
		self.title = title
		self.posts = []
		self.characters = []
		self.active = True if active == "TRUE" else False
		self.open = True if open == "Open" else False
	def sortPosts(self):
		self.posts = sorted(self.posts, key=lambda x: x.date, reverse=False)
		
	def wordCount(self):
		return sum([i.length for i in self.posts])
		
	def __repr__(self):
		s = self.title + "\n"
		for p in self.posts:
			s += p.__repr__() + "\n"
		return s
		
	def showDuration(self):
		return str(self.posts[-1].date - self.posts[0].date)