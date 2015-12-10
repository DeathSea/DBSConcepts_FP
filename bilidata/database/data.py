# -- coding:utf8
# author:deathsea
import mysql.connector
config = {
  'user': 'root',
  'password': 'wkx123456',
  'host': 'localhost',
  'database': 'dbfp',
  'raise_on_warnings': True,
}
query_admin_user_password_req =  "select password from adminuser where name=%s limit 1"
query_av_count_req = "select count(id) from dbfp_av_info"
query_av_info_req = ("select `id`,`av`,`title`,`up_id`,"
    "(select name from dbfp_up_info where dbfp_av_info.up_id=dbfp_up_info.uid),"
  "`create_stamp`,`play_times`,"
  "`collect_times`,`dan_count`,`review_times`,`coins_count` from dbfp_av_info "
  "limit %s,%s"
  )

query_up_count_req = "select count(uid) from dbfp_up_info"
query_up_info_req = ("select `uid`, `name`, `lvl`, `sign`, `birth`, `reg_date`, `article`,"
 "`follow_count`, `fans_count` from dbfp_up_info "
 "where uid=%s"
  )

add_av_info_req = ("INSERT INTO `dbfp_av_info` "
                   "(`id`, `av`, `title`, `up_id`, `create_stamp`, `create_at`, `play_times`,"
                    " `collect_times`, `dan_count`, `review_times`, `coins_count`)"
                   "VALUES(NULL, %s, %s, %s, FROM_UNIXTIME(%s), %s, %s, %s, %s, %s, %s);")
add_up_info_req = ("INSERT INTO `dbfp_up_info`" 
                  "(`uid`, `name`, `lvl`, `sign`, `birth`, `reg_date`, `article`,"
                  " `follow_count`, `fans_count`)"
                  "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);")
add_tag_req = ("INSERT INTO `dbfp_tag` "
                   "(`id`, `name`)"
                   "VALUES(NULL, %s);")
add_av_tag_req = ("INSERT INTO `dbfp_av_tag` "
                   "(`id`, `av_id`,`tag_id`)"
                   "VALUES(NULL, %s,%s);")

update_av_info_req = ["UPDATE `dbfp_av_info` ",
    " set ",
    " where "]
update_up_info_req = ['UPDATE `dbfp_up_info`',
  " set ",
  " where "]
update_tag_req = ["UPDATE `dbfp_tag`"
  " set name=%s"
  " where id=%s"]
update_av_tag_req = ["UPDATE `dbfp_av_tag`",
  " set ",
  " where "]

delete_av_info_by_id_req = ("DELETE from `dbfp_av_info`"
  "where id=%s")
delete_av_info_by_set_req = ("DELETE from `dbfp_av_info`"
  "where id in %s")

delete_up_info_by_id_req = ("DELETE from `dbfp_up_info`"
  "where uid=%s")
delete_up_info_by_set_req = ("DELETE from `dbfp_up_info`"
  "where uid in %s")

delete_tag_by_id_req = ("DELETE from `dbfp_tag`"
  "where id=%s")
delete_tag_by_set_req = ("DELETE from `dbfp_tag`"
  "where id in %s")

delete_av_tag_by_id_req = ("DELETE from `dbfp_av_tag`"
  "where id=%s")
delete_av_tag_by_set_req = ("DELETE from `dbfp_av_tag`"
  "where id in %s")

def connect(mysql_config=None):
  return mysql.connector.connect(**config)

def query_admin_user_password(mysql_conn,name):
  this_cursor = mysql_conn.cursor()
  this_cursor.execute(query_admin_user_password_req,(name,))
  password = ''
  for (password,) in  this_cursor:
    password = password
  this_cursor.close()
  mysql_conn.close()
  return password

def query_av_count(mysql_conn):
    this_cursor = mysql_conn.cursor()
    this_cursor.execute(query_av_count_req)
    count = 0
    for (count,) in  this_cursor:
        count = count
    this_cursor.close()
    mysql_conn.close()
    return count

def query_av_info(mysql_conn,start,split_count):
  this_cursor = mysql_conn.cursor()
  this_cursor.execute(query_av_info_req,(start,split_count))
  resultlist = []
  for idd,av, title, up_id,up, create_stamp, play_times, \
  collect_times, dan_count, review_times, coins_count in  this_cursor:
    resultlist.append((idd,av, title, up_id,up, create_stamp, play_times, 
  collect_times, dan_count, review_times, coins_count,))
  this_cursor.close()
  mysql_conn.close()
  return resultlist

#c = connect()
#print query_av_info(c,0,1)
def query_up_info(mysql_conn,up_id):
    this_cursor = mysql_conn.cursor()
    this_cursor.execute(query_up_info_req,(up_id,))
    flag = False
    resultlist = []  
    for uid, name, lvl, sign, birth, reg_date,\
     article,follow_count, fans_count in this_cursor:
        flag = True
        resultlist.append((uid, name, lvl, sign, birth, reg_date,article,follow_count, fans_count,))
    this_cursor.close()
    mysql_conn.close()   
    if resultlist == []:
      return None
    else:
      return resultlist



def insert_up_info(mysql_conn,dic):
    #this dic format like:
    #{
    #     "key":"value"
    #}
    #the key has:
    #         `uid`,`name`, `lvl`, `sign`, `birth`, `reg_date`, `article`, `follow_count`, `fans_count`
    #          should has all of it
    
    #test:
    all_key = ["uid","name", "lvl", "sign", "birth", "reg_date", "article", "follow_count", "fans_count"]
    if len(map(lambda x:dic.has_key(x),all_key)) != len(all_key):
      return 403
    tup = tuple([dic[key] for key in all_key])
    this_cursor = mysql_conn.cursor()
    this_cursor.execute(add_up_info_req,tup)
    mysql_conn.commit()
    this_cursor.close()
    return

def insert_av_info(mysql_conn,dic):
    # uid = tup[2]
    # if uid != 0 and not does_user_info_exist(mysql_conn,uid):
    #     updic = read_user_info(uid)
    #     up_tup = create_user_info(updic)
    #     insert_up_info(mysql_conn,up_tup)
    #test:
    all_key = ["av", "title", "up_id", "create_stamp", "create_at", "play_times", "collect_times",
     "dan_count", "review_times", "coins_count"]
    if len(map(lambda x:dic.has_key(x),all_key)) != len(all_key):
      return 403
    tup = tuple([dic[key] for key in all_key])

    this_cursor = mysql_conn.cursor()
    this_cursor.execute(add_av_info_req,tup)
    mysql_conn.commit()
    this_cursor.close()

def insert_tag(mysql_conn,dic):
  all_key = ['name']
  if not dic.has_key('name'):
    return 403
  tup = (dic['name'],)
  this_cursor = mysql_conn.cursor()
  this_cursor.execute(add_tag_req,tup)
  mysql_conn.commit()
  this_cursor.close()
def insert_av_tag(mysql_conn,dic):
  all_key = ['av_id','tag_id']
  if len(map(lambda x:dic.has_key(x),all_key)) != len(all_key):
    return 403
  this_cursor = mysql_conn.cursor()
  this_cursor.execute(add_av_tag_req,tup)
  mysql_conn.commit()
  this_cursor.close()

def update_av_info(mysql_conn,dic,av_id):
    #this dic format like:
    #{
    #     "key":"value"
    #}
    #the key has:
    #         "id", "av", "title", "up_id", "create_stamp", "create_at", "play_times", "collect_times", "dan_count", "review_times", "coins_count"
    #          the dic should has one of them
    all_key = ["av", "title", "up_id", "create_stamp", \
    "create_at", "play_times", "collect_times", \
    "dan_count", "review_times", "coins_count"]
    if sum(map(lambda x:dic.has_key(x),all_key)) ==0:
      return 403
    #if there is a up_id update the up_id should in the dbfp_up_info
    if dic.has_key('up_id'):
      c = connect()
      if not query_up_info(c,int(dic["up_id"])):
        return 403
    update_av_info_req_copy = update_av_info_req[:]
    first_update = 1
    for key,value in dic.items():
      if key in all_key:
        if first_update:
            update_av_info_req_copy[1] += '%s=%s'%(key,value)
            first_update = 0
        else:
            update_av_info_req_copy[1]+= ',%s=%s'%(key,value)
    update_av_info_req_copy[2] += 'id=%s'%av_id
    #update query str
    ex = " ".join(update_av_info_req_copy)
    this_cursor = mysql_conn.cursor()
    this_cursor.execute(ex)
    mysql_conn.commit()
    this_cursor.close()
    mysql_conn.close()
#UPDATE `dbfp_av_info` SET `up_id` = '13' WHERE `dbfp_av_info`.`id` = 1
# print update_av_info(None,{"up_id":"13"},1)

def update_up_info(mysql_conn,dic,uid):
    #this dic format like:
    #{
    #     "key":"value"
    #}
    #the key has:
    #         'name','lvl','sign','birth','reg_date','article','follow_count','fans_count'
    #          the dic should has one of them
    all_key = ['name','lvl','sign','birth','reg_date','article','follow_count','fans_count']
    if sum(map(lambda x:dic.has_key(x),all_key)) ==0:
      return 403
    update_up_info_req_copy = update_up_info_req[:]
    first_update = 1
    for key,value in dic.items():
      if key in all_key:
        if first_update:
            update_up_info_req_copy[1] += '%s=%s'%(key,value)
            first_update = 0
        else:
            update_up_info_req_copy[1]+= ',%s=%s'%(key,value)
    update_up_info_req_copy[2] += 'uid=%s'%uid
    #update query str

def update_tag(mysql_conn,dic,id):
    #this dic format like:
    #{
    #     "key":"value"
    #}
    #the key has:
    #         'name','lvl','sign','birth','reg_date','article','follow_count','fans_count'
    #          the dic should has one of them
    all_key = ['name']
    if not dic.has_key('name'):
      return 403
    this_cursor = mysql_conn.cursor()
    this_cursor.execute(update_tag_req,(dic['name'],id))
    mysql_conn.commit()
    this_cursor.close()

def delete_av_info(mysql_conn,id_set):
  if type(id_set) == type('') or type(id_set) == type(u''):
    delete_av_info_copy = delete_av_info_by_id_req
    id_set = (id_set,)
  elif type(id_set) == type(()):
    delete_av_info_copy = delete_av_info_by_set_req
  this_cursor = mysql_conn.cursor()
  this_cursor.execute(delete_av_info_copy,id_set)
  mysql_conn.commit()
  this_cursor.close()
  return True

def  delete_up_info(mysql_conn,id_set):
  if type(id_set) == type(''):
    delete_up_info_copy = delete_up_info_by_id_req
    id_set = (id_set,)
  elif type(id_set) == type(()):
    delete_up_info_copy = delete_up_info_by_set_req
  # this_cursor = mysql_conn.cursor()
  # this_cursor.execute(delete_up_info_copy,id_set)
  # mysql_conn.commit()
  # this_cursor.close()

def delete_tag(mysql_conn,id_set):
  if type(id_set) == type(''):
    delete_tag_copy = delete_tag_by_id_req
    id_set = (id_set,)
  elif type(id_set) == type(()):
    delete_tag_copy = delete_tag_by_set_req
  # this_cursor = mysql_conn.cursor()
  # this_cursor.execute(delete_tag_copy,id_set)
  # mysql_conn.commit()
  # this_cursor.close()
def delete_tag_av(mysql_conn,id_set):
  if type(id_set) == type(''):
    delete_av_tag_copy = delete_av_tag_by_id_req
    id_set = (id_set,)
  elif type(id_set) == type(()):
    delete_av_tag_copy = delete_av_tag_by_set_req
  # this_cursor = mysql_conn.cursor()
  # this_cursor.execute(delete_av_tag_copy,id_set)
  # mysql_conn.commit()
  # this_cursor.close()
