
import requests
import time


def req(body, payload):

	method = body['method']
	url = body['url']
	delay = body['delay']
	data  = body['data']
	header = body['header']

	rep = {}

	if delay != 0:
		time.sleep(delay)


	
	if method == 'GET':

		url = url.replace('FUZZ', payload)

	else:

		for key, value in data.items():
			if 'FUZZ' in value:
				data[key] = data[key].replace('FUZZ', payload)

	print(url)
	
	try:
		if method == 'GET':
			r = requests.get(url, headers=header, timeout=30, allow_redirects=False)
		else:
			r = requests.post(url, data=data, headers=header, timeout=30, allow_redirects=False)

	except requests.exceptions.RequestException as e:
		print('Error: {}'.format(e))
	except requests.exceptions.HTTPError as e:
		print('HTTP Error {}'.format(e))
	except requests.exceptions.ConnectionError as e:
		print('Connection Error {}'.format(e))
	except requests.exceptions.Timeout as e:
		print('Timeout Error: {}'.format(e))

	rep['method'] = method
	rep['url'] = url
	rep['code'] = str(r.status_code)
	rep['body'] = str(r.text)
	rep['time'] = int(r.elapsed.total_seconds())
	rep['size'] = len(str(r.text))


	
	if method == 'GET':
		url = url.replace(payload, 'FUZZ')

	else:
		for key, value in data.items():
			if payload in value:
				data[key] = data[key].replace(payload, 'FUZZ')

	return rep



