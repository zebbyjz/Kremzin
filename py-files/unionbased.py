

from req_ import req
from getConf_ import getConf
from getRows_ import getRows

manually = False
payload = ''

usr_url=input("Enter URL with quotes: ")


body = {
	
	'method':'GET',
	'url':usr_url,
	'delay': 0,

	'data': {


	},

	'header': {

	'User-Agent':'Kremzin SQL project'

			
	},

}


config = {

	'dbms': '',
	'escape' : '',
	'operator': '',
	'comment': '',
	'size':'',
	'detection': '',
}

if getConf(body, config):
	print(str(getRows(body, config))+' Columns found')
