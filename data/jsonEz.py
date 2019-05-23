import json #Для хранения файлов


def save(name,data):
	fileName = 'json/{}.json'.format(name)#___%H_%M добавить в название для часов и минут
	with open(fileName, 'w') as fp:
		json.dump(data, fp)

def load(name):
	fileName = '{}'.format(name)#___%H_%M добавить в название для часов и минут
	dict_out = {}
	with open(fileName, 'r') as fp:
		dict_out = json.load(fp)
	return(dict_out)

def check(name):
		fileName = 'json/{}.json'.format(name)#___%H_%M добавить в название для часов и минут
		try:
			with open(fileName, 'r') as fp:
				pass
		except FileNotFoundError:
			return False
		else:
			return True