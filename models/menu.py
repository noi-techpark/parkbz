from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'Bolzano parking'
settings.subtitle = 'Parking situation'
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
response.page_title=T("Bolzano parking situation")
response.google_map_key = 'AIzaSyA9DDSrqpql5y89lZfnnwu6dkOiCcLf9Bk'

response.menu = [
	(SPAN('INTEGREEN'), False, 'http://www.integreen-life.bz.it', [
        (A(CAT(TAG.I(_class="icon-info-sign"), " %s" % T('Parking situation')), _href='http://parking.integreen-life.bz.it', _title="Bolzano parking situation") , False, None),
		(A(CAT(TAG.I(_class="icon-road"), " %s" %  T('Traffic monitoring')),_href='http://traffic.integreen-life.bz.it', _title="Bluetooth traffic monitoring"), False, None),
	]),
	(T('Index'),URL('default','index')==URL(),URL('default','index'),[]),
	(T('Widget'),URL('default','widget')==URL(),URL('default','widget')),]

if "auth" in locals():
    response.menu += auth.wikimenu()
