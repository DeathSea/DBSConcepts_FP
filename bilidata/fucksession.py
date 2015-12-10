class sess(object):
	def __init__(self):
		self.session = None
	def getsession(self):
		return self.session
	def setsession(self,session):
		self.session = session
