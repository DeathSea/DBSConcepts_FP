# -- coding:utf-8
from web import template
from web import input as webinput
from web import form as webform
from database.data import connect,insert_av_info
from sys import path
from os import chdir,sep
import datetime
vav = webform.regexp('\d{1,8}','must a num ')
vtitle = webform.regexp(".{1,200}",'this can\'t blank')
vcreate = webform.regexp("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",'format not correct')
vplay = webform.regexp('\d{1,11}','must a num')

updata_form = webform.Form(
	webform.Textbox(name='id',hidden='True',description='id'),
	webform.Textbox("av",vav,description="av"),
	webform.Textbox('title',vtitle,description='title'),
	webform.Textbox('up',vav,description='up'),
	webform.Textbox('create_time',vcreate,description="create time"),
	webform.Textbox('play_times',vplay,description='play times'),
	webform.Textbox('collects_count',vplay,description='collects count'),
	webform.Textbox('dans_count',vplay,description='dans count'),
	webform.Textbox('reviews_count',vplay,description='reviews count'),
	webform.Textbox('coins_count',vplay,description='coins count'),
	)
class avins():
	def GET(self):
		chdir(path[0]+sep+'avinfo')
		render = template.render('templates/')
		f = updata_form()
		#totalCounts,pageSize,currentPage
		return render.insert(f)
	def POST(self):
		chdir(path[0]+sep+'avinfo')
		render = template.render('templates/')
		f = updata_form();
		if not f.validates():
			return render.updata(f)
		aid = f.id.value
		c = connect()
		nav,ntitle,nupid,\
		ncreate_time,nplay_times,ncollects_count,\
		ndans_count,nreview_count,ncoin_count = \
		int(f.av.value),f.title.value,int(f.up.value),\
		str(f.create_time.value),int(f.play_times.value),int(f.collects_count.value),\
		int(f.dans_count.value),int(f.reviews_count.value),int(f.coins_count.value)
		insertdic = {}
		insertdic["av"] = nav
		insertdic["title"] = ntitle
		insertdic["up_id"] = nupid
		insertdic['create_stamp'] = ncreate_time
		insertdic["create_at"] = ncreate_time
		insertdic["play_times"] = nplay_times
		insertdic["collect_times"] = ncollects_count
		insertdic["dan_count"] = ndans_count
		insertdic["review_times"] = nreview_count
		insertdic['coins_count'] = ncoin_count
		print insertdic
		con = connect()
		result = insert_av_info(con,insertdic)
		if result == 403:
			f.up.note = "该up id不满足约束条件"
			return render.insert(f)
		return render.success('updata')