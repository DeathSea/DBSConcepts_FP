from web import template,form
from web import config as webconfig
import hashlib
from database.data import connect,query_admin_user_password
from sys import path
from os import chdir,sep
session = webconfig.get("_session")

vname = form.regexp(r".{1,20}$", 'must be between 1 and 20 characters')
vpass = form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
loginform = form.Form(
	form.Textbox("username",vname,description='UserName'),
	form.Password("password",vpass,description='password'),
	form.Button('Submit',type='submit',description='Submit'),
	)
def md5st(string):
	Nmd5 = hashlib.md5()
	Nmd5.update(string)
	return Nmd5.hexdigest()

class index:
	def GET(self):
		global session
		chdir(path[0]+sep+'index')
		render = template.render('templates/')
		fo = loginform()
		if session == None:
			session = webconfig._session
		if session.login == 0:
         		return render.index(False,fo)
         	elif session.login == 1:
         		return render.index(True,fo)
	def POST(self):
		global session
		chdir(path[0]+sep+'index')
		render = template.render('templates/')
		fo = loginform()
		if session == None:session = webconfig._session
		if not fo.validates():
			return render.index(False,fo)
		else:
			name = fo["username"].value
			up = fo["password"].value
			tc = connect()
			dp = query_admin_user_password(tc,name)
			if dp == "":
				fo["username"].note = "username not exist"
				return render.index(False,fo)				
			if md5st(up) != dp:
				fo["password"].note = "Password incorrect"
				return render.index(False,fo)
			session.login = 1
			session.name = fo["username"].value
			# print session.login,session.name
			return render.index(True,fo)
