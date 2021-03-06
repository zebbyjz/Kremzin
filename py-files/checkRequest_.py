

from data.mysql import *
from req_ import req
from re import search
import urllib.parse

def checkRequest(body, config, payload):

	detection = config['detection']

	rep = req(body, payload)

	if detection == 'booleanBased':

		rep['size'] = len(rep['body'].replace(urllib.parse.unquote_plus(payload), ''))

		if rep['size'] == config['size']:

			return True

		else:

			return False
		
	elif detection == 'errorBased':
		
		for err in MySQL['error']:
			
			if err in rep['body']:	
				
				return False
				
		return True


	elif detection == 'codeBased':

		if search(r'^2', rep['code']):

			return True

		else:
			
			return False
