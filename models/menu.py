from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'Bolzano parking'
settings.subtitle = 'Real-time parking situation'
settings.author = 'Paolo Valleri'
settings.author_email = 'paolo.valleri at gmail.com'
settings.keywords = ''
settings.description = ''
settings.layout_theme = 'Default'
settings.database_uri = 'sqlite://storage.sqlite'
settings.security_key = 'a5e342b6-3d7d-4952-81cc-8fadc6caaee7'
settings.email_server = 'smtp.digital.tis.bz.it'
settings.email_sender = 'project@integreen-life.bz.it'
settings.email_login = ''
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = []

response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.google_analytics_id = "UA-34703572-1"
response.meta.description = settings.description 
response.page_title=T("Real-time Bolzano parking situation")
response.google_map_key = 'AIzaSyA9DDSrqpql5y89lZfnnwu6dkOiCcLf9Bk'
response.header_msg = XML("<i class='icon-bullhorn icon-white'></i> %s" % T('Servizio sperimentale'))

response.menu = [
	(T('Index'),URL('default','index')==URL(),URL('default','index'),[]),
	(T('Widget'),URL('default','widget')==URL(),URL('default','widget')),]
	
response.static_version = "0.0.2"
