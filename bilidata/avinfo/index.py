from web import template
from web import input as webinput
from database.data import connect,query_av_count,query_av_info
from sys import path
from os import chdir,sep
import datetime
testdata = [
    (7, u'2012\u5730\u7403\u4fbf\u5f53\u4e4b\u65e5\u5ba3\u4f20\u7247', 2, u'\u78a7\u8bd7', datetime.datetime(2009, 6, 26, 15, 11, 36), 755578, 3330, 15576, 8490, 708), 
    (11, u'\u521d\u604b\u9650\u5b9a \u771f\u4ebapv', 245050, u'blackfox', datetime.datetime(2009, 6, 29, 12, 42, 16), 98414, 349, 1146, 870, 36), 
    (12, u'\u97f3\u4e50\u4e0e\u5f39\u5e55\u540c\u6b65 3.5', 2, u'\u78a7\u8bd7', datetime.datetime(2009, 7, 3, 19, 10, 16), 384888, 452, 771, 950, 6), 
    (16, u'\u3010FATE\u76f8\u5173\u3011CRUCIS FATAL FAKE MV \u300aFaker\u300b', 1, u'bishi', datetime.datetime(2009, 7, 9, 1, 15, 33), 67087, 354, 1218, 443, 29), 
    (20, u'\u3010\u521d\u97f3\u30df\u30af(40mP)\u3011\u5de8\u5927\u5c11\u5973', 68, u'hpkm4036', datetime.datetime(2009, 7, 9, 14, 7, 51), 93994, 921, 2497, 740, 112), 
    (23, u'\u3010\u614e\u5165\u3011\u88ab\u84dd\u84dd\u8def\u7684\u4e03\u53d8\u5316\u6d17\u8111\u540e\uff0c\u5174\u81f4\u5f88\u9ad8', 68, u'hpkm4036', datetime.datetime(2009, 7, 9, 15, 55, 49), 925326, 10558, 21162, 2730, 892), 
    (24, u'\u591a\u90a3\u8def\u591a\u4fe1\u4ef0\u98ce\u5316\u66f2', 68, u'hpkm4036', datetime.datetime(2009, 7, 9, 15, 59, 12), 144236, 1634, 4141, 420, 148), 
    (25, u'\u6559\u4e3b \u6559\u4e3b GO MY WAY\uff01', 112943, u'\u795e\u7957\u6b8b\u9b42', datetime.datetime(2009, 7, 9, 16, 42, 55), 37969, 241, 688, 151, 16), 
    (26, u'\u84dd\u84dd\u8def\u7684\u571f\u8033\u5176\u8fdb\u884c\u66f2', 184568, u'\u70e4\u591c\u96c0', datetime.datetime(2009, 7, 9, 16, 56, 50), 55018, 689, 1652, 250, 105), 
    (28, u'\u6a31\u82b1\u5927\u6218COSPLAY\uff5e\u975e\u5e38\u903c\u771f', 79, u'saber\u9171', datetime.datetime(2009, 7, 9, 17, 2, 50), 36466, 137, 1282, 234, 14)
]
class avindex:
    def GET(self):
        user_data = webinput(page=1,splitlimit=10,order="")
        try:
            page = int(user_data.page)
        except ValueError,p:
            return 500
        try:
                splitlimit = int(user_data.splitlimit)
        except ValueError,p:
            return 500
        order = user_data.order
        all_order = {
        "cs":'create_stamp',
        "pc":"play_times",
        "ct":"collect_times",
        "dc":"dan_count",
        "rc":"review_times",
        "cc":"coins_count",
        "csa":"create_stamp desc",
        "pca":"play_times desc",
        "cta":"collect_times desc",
        "dca":"dan_count desc",
        "rca":"review_times desc",
        "cca":"coins_count desc",
        "":""
        }
        default_order = ['cs', 'pc', 'ct', 'dc', 'rc','cc']
        if order != '' and order not in all_order.keys():
            return 500
        if len(order) == 2:
            ind = default_order.index(order)
            default_order[ind] = order+'a'
        startitemid = (page -1)*splitlimit 

        c = connect()
        allcount = query_av_count(c)
        all_page = allcount/splitlimit

        c = connect()
        print startitemid,splitlimit,all_order[order]
        gotdata = query_av_info(c,startitemid,splitlimit,all_order[order])

        chdir(path[0]+sep+'avinfo')
        render = template.render('templates/')
        #totalCounts,pageSize,currentPage
        return render.index(gotdata,allcount,splitlimit,page,default_order,order)
    def POST(self):
        return None