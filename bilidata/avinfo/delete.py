from web import template
from web import input as webinput
from database.data import connect,delete_av_info

from sys import path
from os import chdir,sep
class avdel:
	def GET(self):
		userdata = webinput(did=0)
		did = userdata.did
		if did == 0 or did=="0":
			return 404
		else:
			c = connect()
			delete_av_info(c,did)
			chdir(path[0]+sep+'avinfo')
			render = template.render('templates/')
			return render.delete()
