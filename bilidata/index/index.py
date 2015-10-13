from web import template
from sys import path
from os import chdir,sep
class index:
	def GET(self):
		chdir(path[0]+sep+'index')
		render = template.render('templates/')
		return render.index()
	def POST(self):
		return None
