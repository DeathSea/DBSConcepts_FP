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
add_av_info_req = ("INSERT INTO `dbfp_av_info` "
                   "(`id`, `av`, `title`, `up_id`, `create_stamp`, `create_at`, `play_times`, `collect_times`, `dan_count`, `review_times`, `coins_count`)"
                   "VALUES(NULL, %s, %s, %s, FROM_UNIXTIME(%s), %s, %s, %s, %s, %s, %s);")
add_up_info_req = ("INSERT INTO `dbfp_up_info`" 
                  "(`uid`, `name`, `lvl`, `sign`, `birth`, `reg_date`, `article`, `follow_count`, `fans_count`)"
                  "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);")
def insert_up_info(mysql_conn,tup):
    this_cursor = mysql_conn.cursor()
    this_cursor.execute(add_up_info_req,tup)
    mysql_conn.commit()
    this_cursor.close()
    return

def insert_av_info(mysql_conn,tup):
    # uid = tup[2]
    # if uid != 0 and not does_user_info_exist(mysql_conn,uid):
    #     updic = read_user_info(uid)
    #     up_tup = create_user_info(updic)
    #     insert_up_info(mysql_conn,up_tup)
    this_cursor = mysql_conn.cursor()
    this_cursor.execute(add_av_info_req,tup)
    mysql_conn.commit()
    this_cursor.close()

def updata_av_info(mysql_conn,):
