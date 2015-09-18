# -*- coding: utf-8 -*-
# transle bilibili's av json file into database
import json
import mysql.connector
import ntpath
import urllib2,time

config = {
  'user': 'root',
  'password': '',
  'host': 'localhost',
  'database': 'dbhp',
  'raise_on_warnings': True,
}
con = mysql.connector.connect(**config)
cur = con.cursor()
#UPDATE `dbfp`.`dbfp_av_info` SET `create_stamp` = FROM_UNIXTIME('1246000296') WHERE `dbfp_av_info`.`id` = 1;
add_av_info_req = ("INSERT INTO `dbfp_av_info` "
	               "(NULL, `av`, `title`, `up_id`, `create_stamp`, `create_at`, `play_times`, `collect_times`, `dan_count`, `review_times`, `coins_count`)"
	               "VALUES(%d, %d, %s, %d, FROM_UNIXTIME(%s), %s, %d, %d, %d, %d, %d);")
add_up_info_req = ("INSERT INTO `dbfp_up_info`" 
                  "(`uid`, `name`, `lvl`, `sign`, `birth`, `reg_date`, `article`, `follow_count`, `fans_count`)"
                  "VALUES(%d, %s, %d, %s, %s, %s, %d, %d, %d);")
av_dir = "D:\\PProject\\bilibili\\allavinfo"
av_dir2 = "D:\\PProject\\bilibili\\allavinfo2-1"
av_dir3 = "D:\\PProject\\bilibili\\allavinfo2"
user_dir = "D:\\PProject\\bilibili\\alluserinfo"
def getURLContent(url):
    while 1:        
        try:
            headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
            #'Cookie':'pgv_pvi=9629054976; pgv_si=s7276307456; sid=a84gv3d7; fts=1438695578; LIVE_BUVID=a30f235e687b15cddec7073e271b78dc; LIVE_BUVID__ckMd5=1aff9d63faeeb5dd; PLHistory=bVm2%7Co2}GW; IESESSION=alive; DedeUserID=2754937; DedeUserID__ckMd5=62d03cc207ac353c; SESSDATA=8d08bf28%2C1442638544%2C030d0e52; LIVE_LOGIN_DATA=4f48da9e73ffdd64590fc2812487cb4fb2d8d70f; LIVE_LOGIN_DATA__ckMd5=8840c45c091b3590; _cnt_dyn=0; _cnt_pm=0; _cnt_notify=21; uTZ=-480; DedeID=2837864; _dfcaptcha=55b092b61a3f77ba89cde89af6ed7f90; CNZZDATA2724999=cnzz_eid%3D1895263873-1425444951-%26ntime%3D1442045119'
            }
            req = urllib2.Request(url = url,headers = headers);   
            content = urllib2.urlopen(req,timeout = 10).read();
        except:
            print 'connect error...'
            time.sleep(20)
            continue
        break
    return content;

def GetuserInfo(id):
    url = "http://space.bilibili.com/%d#!/index"%(id)
    con = getURLContent(url)
    s = con.find("_bili_space_info")
    e = con.find("var _bili_is_")
    #print s,e
    resu = con[s:e].replace("_bili_space_info = eval(",'').replace(');',"")
    return resu

def create_av_info(file_name,string):
	if type(file_name) == type(''):
		av = int(file_name)
	elif type(file_name) == type(2):
		av = file_name
	else:
		return -1
	di = json.loads(string)
	#                av,title,     up_id,create_stamp,created_at,play_times,collect_times,dan_count,review_times,coins_count
	result_tuple = (av,di['title'],di['mid'],di['created'],di['created_at']+':00',di['play'],di['favorites'],di['video_review'],di['coins'])
	return result_tuple
def create_user_info(string):
	if type(string) == type(''):
		st = string
	di = json.loads(st)
	#               uid,      name,        lvl,
	#      sign,                     birth,reg_date,
	#     article,     follow_count,   fans_count,
	result_tuple = (di['mid'],di['name'],di['level_info']["current_level"],
		di["sign"]?di["sign"]:"NULL",di['birthday'],di["regtime"],
		di["article"],di["attention"],di["fans"],
		)
def read_user_info(id):
	if type(id) != type(""):
		id = str(id)
    FILE = user_dir+'\\'+id+'.json'
	FILE_EXIST = ntpath.exists(FILE)
	if FILE_EXIST:
		f = open(FILE,'r')
		jsoncon = f.readline()
		f.close()
	else:
		jsoncon = GetuserInfo(int(id))
	return json.loads(jsoncon)
def insert_av_info(mysql_conn,tu):
    pass