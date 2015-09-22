# -*- coding: utf-8 -*-
# transle bilibili's av json file into database
import json
import mysql.connector
import ntpath
import urllib2,time
from tt import GetVideoInfo
config = {
  'user': 'root',
  'password': '',
  'host': 'localhost',
  'database': 'dbfp',
  'raise_on_warnings': True,
}
#con = mysql.connector.connect(**config)
#cur = con.cursor()
#UPDATE `dbfp`.`dbfp_av_info` SET `create_stamp` = FROM_UNIXTIME('1246000296') WHERE `dbfp_av_info`.`id` = 1;
add_av_info_req = ("INSERT INTO `dbfp_av_info` "
                   "(`id`, `av`, `title`, `up_id`, `create_stamp`, `create_at`, `play_times`, `collect_times`, `dan_count`, `review_times`, `coins_count`)"
                   "VALUES(NULL, %s, %s, %s, FROM_UNIXTIME(%s), %s, %s, %s, %s, %s, %s);")
add_up_info_req = ("INSERT INTO `dbfp_up_info`" 
                  "(`uid`, `name`, `lvl`, `sign`, `birth`, `reg_date`, `article`, `follow_count`, `fans_count`)"
                  "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);")
av_dir = "D:\\PProject\\bilibili\\allavinfo"
av_dir2 = "D:\\PProject\\bilibili\\allavinfo2-1"
av_dir3 = "D:\\PProject\\bilibili\\allavinfo2"
av_dir4 = 'D:\\PProject\\bilibili\\allavinfo3'
av_dir5 = 'D:\\PProject\\bilibili\\allavinfo4'
user_dir = "D:\\PProject\\bilibili\\alluserinfo"

def getURLContent(url):
    while 1:        
        try:
            headers = {'User-Agent':'Mozilla/5.0 (iPad; CPU OS 4_3_5 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5',
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

def create_av_info(file_name,di):
    if type(file_name) == type(''):
        av = int(file_name)
    elif type(file_name) == type(2):
        av = file_name
    else:
        return -1
    #di = json.loads(string)
    #                av,title,     up_id,create_stamp     ,created_at,            play_times,collect_times,  dan_count,    review_times,coins_count
    #               %d, %s, %d, FROM_UNIXTIME(%d), %s, %d, %d, %d, %d, %d)
    if di['author'] == None:
        id = 0
    else:
        id = int(di['mid'])
    result_tuple = (int(av),di['title'],id,di['created'],di['created_at']+':00',int(di['play']),int(di['favorites']),int(di['video_review']),int(di['review']),int(di['coins']))
    #print result_tuple
    return result_tuple

def create_user_info(di):
    if type(di) != type({}):
        return ()
    #di = json.loads(st)
    #               uid,      name,        lvl,
    #      sign,                     birth,reg_date,
    #     article,     follow_count,   fans_count,
    #VALUES(%d, %s, %d, %s, %s, %s, %d, %d, %d)
    result_tuple = (int(di['mid']),di['name'],di['level_info']["current_level"],
        di["sign"] and di["sign"] or "NULL",di['birthday'],di["regtime"],
        di["article"],di["attention"],di["fans"],
        )
    return result_tuple

def read_av_info(id):
    if type(id) != type(0):
        id = int(id)
    if 0<=id<=174999:
        this_dir = av_dir
    elif 175000<=id<=290998:
        this_dir = av_dir2
    elif 290999<=id<=469999:
        this_dir = av_dir3
    elif 470000<=id<=539999:
        this_dir = av_dir4
    else:
        this_dir = av_dir5
    FILE = this_dir+'\\'+str(id)+'.json'
    FILE_EXIST = ntpath.exists(FILE)
    if FILE_EXIST:
        f = open(FILE,'r')
        jsoncon = f.readline()
        f.close()
    else:
        return 404
    di = json.loads(jsoncon)
    if di.has_key('code') and di['code'] == -403:
        return 404
    elif di.has_key('code') and di['code'] == -503:
        raise NameError, str(id)
        con = GetVideoInfo(id)
        with open(FILE) as f:
            print >> f,con
        di = json.loads(jsoncon)
    return di  

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

def does_user_info_exist(mysql_conn,id):
    flag = False
    QUERY_STR = ("select uid from dbfp_up_info"
        " where uid=%s")
    cur = mysql_conn.cursor()
    cur.execute(QUERY_STR,(id,))
    for x in cur:
        flag = True
    cur.close()
    return flag

def insert_up_info(mysql_conn,tup):
    this_cursor = mysql_conn.cursor()
    this_cursor.execute(add_up_info_req,tup)
    mysql_conn.commit()
    this_cursor.close()

def insert_av_info(mysql_conn,tup):
    uid = tup[2]
    if uid != 0 and not does_user_info_exist(mysql_conn,uid):
        updic = read_user_info(uid)
        up_tup = create_user_info(updic)
        insert_up_info(mysql_conn,up_tup)
    this_cursor = mysql_conn.cursor()
    this_cursor.execute(add_av_info_req,tup)
    mysql_conn.commit()
    this_cursor.close()

if __name__ == '__main__':
    con = mysql.connector.connect(**config)
    #userdic = read_user_info(1)
    for i in range(9978,10000):
        avdic = read_av_info(i)
        if avdic != 404:
            avtup = create_av_info(i,avdic)
            insert_av_info(con,avtup)
            print i,' insert complete'
        else:
            print i,' is unavil or 404'
    con.close()
