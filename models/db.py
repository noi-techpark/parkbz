# -*- coding: utf-8 -*-

db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
#response.optimize_css = 'concat,minify'
#response.optimize_js = 'concat,minify'

from gluon.tools import Auth
#, Crud, Service, PluginManager, prettydate
auth = Auth(db)
#crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
#auth.define_tables(username=False, signature=False)

## configure email
#mail = auth.settings.mailer
#mail.settings.server = 'logging' or 'smtp.gmail.com:587'
#mail.settings.sender = 'you@gmail.com'
#mail.settings.login = 'username:password'


#mail.settings.server = settings.email_server
#mail.settings.sender = settings.email_sender
#mail.settings.login = settings.email_login
T.is_writable = False

if not request.is_local:
	from gluon.contrib.memcache import MemcacheClient
	memcache_servers = ['127.0.0.1:11211']
	cache.memcache = MemcacheClient(request, memcache_servers)
	cache.ram = cache.disk = cache.memcache


db.define_table('question',
	Field('sentence', 'string'),
	#auth.signature
)
db.define_table('feedback',
    Field('answer', 'boolean'),
    Field('question_id', 'reference question'),
    Field('gathered_on', 'datetime', default=request.now),
)	

db.feedback.answer.label = T('Hai mai problemi di parcheggio a Bolzano?')
db.feedback.answer.widget = BuildRadioButtonWidget
db.feedback.answer.reppresent = None
db.feedback.question_id.writable = False 
db.feedback.gathered_on.writable = False
