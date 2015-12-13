import web
from sys import path
from os import chdir
from index.index import index
from avinfo.index import avindex
from avinfo.delete import avdel
from avinfo.updata import avupd
from avinfo.insert import avins
from taginfo.index import tagindex
from upinfo.index import upindex
web.config.debug = False

urls = (
    '/' , 'index',
    '/av','avindex',
    '/avdel','avdel',
    '/avupd','avupd',
    '/avins',"avins",
    '/up','upindex',
    '/tag','tagindex',
    '/statics/(js|css)/(.*)\.(js|css)', 'static',
)
class static:
    def GET(self,media, name, suffix):
        chdir(path[0])
        try:
            f = open('static/'+media+'/'+name+'.'+suffix, 'r')
            return f.read()
        except:
            return 404
store = web.session.DiskStore('sessions')
app = web.application(urls,globals())

session = web.session.Session(app,store,initializer={'login':0,'name':''})
web.config._session = session
 
if __name__ == '__main__':
    app.run()