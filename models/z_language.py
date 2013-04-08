#Language managment 
languages = {'it':'Italiano', 'en':'English', 'de':'Deutsch'}

language_links = []
orig_lang = request.uri_language
for l in languages:
	request.uri_language = l
	if orig_lang != l:
		language_links.append( (languages[l], False, URL(args=request.args, vars=request.vars)) )
 
request.uri_language = orig_lang

response.menu.append(
		(SPAN('Language'), False, None, 
			language_links))


if request.uri_language in languages:
	T.force(request.uri_language)
