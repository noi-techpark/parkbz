response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.google_analytics_id = "UA-34703572-1"
response.meta.description = settings.description 
response.page_title=T("Bolzano parking situation")

integreen_network_menu = DIV(XML("""d"""))
response.menu = [
	(SPAN('INTEGREEN'), False, 'http://www.integreen-life.bz.it', [
        (T('Bolzano parking situation'), False, 'http://parking.integreen-life.bz.it'),
		(T('Bluetooth traffic monitoring'), False, 'http://traffic.integreen-life.bz.it')
	]),
	(T('Index'),URL('default','index')==URL(),URL('default','index'),[]),]
response.google_map_key = 'AIzaSyA9DDSrqpql5y89lZfnnwu6dkOiCcLf9Bk'
