import web
from index.index import index
from avinfo.index import avindex
from taginfo.index import tagindex
from upinfo.index import upindex
urls = (
	'/' , 'index',
	'/av','avindex',
	'/up','upindex',
	'/tag','tagindex',
)

if __name__ == '__main__':
	app = web.application(urls,globals())
	app.run()