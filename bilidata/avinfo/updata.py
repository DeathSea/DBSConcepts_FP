# -- coding:utf-8
from web import template
from web import input as webinput
from web import form as webform
from database.data import connect,update_av_info,query_av_info
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
class avupd():
	def GET(self):
		user_data = webinput(aid=0)
		aid = user_data.aid
		if aid==0:return 404
		if aid!=0 and not aid.isdigit():return 404
		f = updata_form()
		c = connect()
		avin = query_av_info(c,int(aid)-1,1)
		_,av,title,upid,up,create_time,play_times,collects_count,dans_count,\
		reviews_count,coins_count = avin[0]
		f.id.set_value(_)
		f.av.set_value(av)
		f.title.set_value(title)
		f.up.set_value(upid)
		f.create_time.set_value(create_time)
		f.play_times.set_value(play_times)
		f.collects_count.set_value(collects_count)
		f.dans_count.set_value(dans_count)
		f.reviews_count.set_value(reviews_count)
		f.coins_count.set_value(coins_count)
		chdir(path[0]+sep+'avinfo')
		render = template.render('templates/')
		#totalCounts,pageSize,currentPage
		return render.updata(f)
	def POST(self):
		chdir(path[0]+sep+'avinfo')
		render = template.render('templates/')
		f = updata_form();
		if not f.validates():
			return render.updata(f)
		aid = f.id.value
		c = connect()
		avin = query_av_info(c,int(aid)-1,1)
		_,av,title,upid,up,create_time,play_times,collects_count,dans_count,\
		reviews_count,coins_count = avin[0]
		nav,ntitle,nupid,\
		ncreate_time,nplay_times,ncollects_count,\
		ndans_count,nreview_count,ncoin_count = \
		int(f.av.value),f.title.value,int(f.up.value),\
		str(f.create_time.value),int(f.play_times.value),int(f.collects_count.value),\
		int(f.dans_count.value),int(f.reviews_count.value),int(f.coins_count.value)
		updadic = {}
		if nav != av:
			updadic["av"] = nav
		if ntitle != title:
			updadic["title"] = ntitle
		if nupid != upid:
			updadic["up_id"] = nupid
		if ncreate_time != str(create_time):
			updadic['create_stamp'] = ncreate_time
		if nplay_times != play_times:
			updadic["play_times"] = nplay_times
		if ncollects_count != collects_count:
			updadic["collect_times"] = ncollects_count
		if ndans_count != dans_count:
			updadic["dan_count"] = ndans_count
		if nreview_count != reviews_count:
			updadic["review_times"] = nreview_count
		if ncoin_count != coins_count:
			updadic['coins_count'] = ncoin_count
		if len(updadic) == 0:
			f.av.note = "don't change any thing!!"
			return render.updata(f)
		con = connect()
		result = update_av_info(con,updadic,aid)
		if result == 403:
			f.up.note = "该up id不满足约束条件"
			return render.updata(f)
		return render.success('updata')