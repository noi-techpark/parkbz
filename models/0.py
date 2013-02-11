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
