response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.google_analytics_id = "UA-34703572-1"
response.meta.description = settings.description
response.page_title=T("Bolzano parking situation")
response.menu = [
	(A('INTEGREEN', _href="http://integreen-life.bz.it/", _class="brand"), False, None),
	(A('Traffic', _href="http://traffic.integreen-life.bz.it/" ), False, None),
	(T('Index'),URL('default','index')==URL(),URL('default','index'),[]),]
response.google_map_key = 'AIzaSyA9DDSrqpql5y89lZfnnwu6dkOiCcLf9Bk'
