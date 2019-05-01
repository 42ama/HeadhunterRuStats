import itertools#для составления ссылок из списка списков
import datetime

#Во встроенных модулях также используеются внешние: bs4, requests, matplotlib, numpy
#и стандартные: json, os, glob, collections(namedtuple)

import data.starter as start#..........начальные преобразования списков
import data.collector as collect#......сбор инфы с хх
import data.jsonEz as jsonEz#..........сохраниение в формате жсон
import data.plotter as plotter#........рисование и сохранение графиков
import data.data_middle as data_middle#обработка собранной инфы за месяц

now = datetime.date.today()
strftime = now.strftime("%Y_%m_%d")

if(now.month != 1):
	lastMonth=datetime.datetime(now.year,now.month-1,now.day).strftime("%Y_%m_")
else:
	lastMonth=datetime.datetime(now.year-1,1,now.day).strftime("%Y_%m_")


###################
TESTMODE=False
###################

#Поле для ввода
class InputField:
	#в field_type хранится тэг - название, с помощью которого формируется стркоа
	text = ''
	def __init__(self, field_type):
		self.field_type = field_type
	def __call__(self, text):
		self.text=text.lower()

class URLQuteFiled(InputField):
	def __call__(self, text):
		InputField(self, self.text)

InputText = InputField('text')
InputText('Python')

url='https://samara.hh.ru/search/vacancy?clusters=true&enable_snippets=true&text='

list_pairs_1 = [('Python', 'python'),
				('C#', 'c%23'),
				('Unity', 'unity'),
				('Data science', 'data+science'),
				('JavaScript', 'javascript'),
				(),
				('Россия', ''),
				('Санкт-Петербург', 'area=2'),
				('Самара', 'area=78'),
				(),
				('',''),
				('Нет опыта работы','experience=noExperience&from=cluster_experience'),
				('1..3 года опыта', 'experience=between1And3&from=cluster_experience'),
				()
				]


'''
d_mainDict = {'text':['Python', 'C#', JavaScript],'area':['Россия','Самара','Санкт-Петербург','Минск'],'expirience':['Любой опыт работы', '1..3 года опыта работы', 'Без опыта работы']}
for key in d_mainDict:
	for x in d_mainDict[key]:
		if len(d_mainDict[key][x])>0:
			val=d_mainDict[key].pop()
			if key = 'text':
				pass
			elif key = 'area':
				pass
			elif key = 'expirience':
				pass
			else:
				raise Exception('Unknown key located')
l_infoField = ['Python', 'C#', JavaScript]#text=
l_areaField = ['Россия','Самара','Санкт-Петербург','Минск']#area=
l_additionalField = ['Любой опыт работы', '1..3 года опыта работы', 'Без опыта работы']



'''
list_pairs_2 = [('Ежедневные (10 дней)','Week'),
				('Ежедневные (месяц)','Month'),
				('Ежемесячные','_Year'),
				(),
				('России', 'Russia'),
				('Самаре', 'Samara'),
				(),
				('абсолютная', 'Abs'),
				('относительная', 'Rel'),
				()
				]

list_jsonStr, list_url = start.pairs_to_lists(list_pairs_1)
list_title, list_fileName = start.pairs_to_lists(list_pairs_2)

list_product_jsonStr = list(itertools.product(*list_jsonStr))#Питон, Россия, Самара
list_product_url = list(itertools.product(*list_url))#python, ,area=78 sep=&
list_product_title = list(itertools.product(*list_title))#Ежемесячные, Самаре, абс
list_product_fileName = list(itertools.product(*list_fileName))#Year, Samara, Abs sep=_

jsonStr=start.tupels_to_lines(list_product_jsonStr)
url=start.tupels_to_lines(list_product_url,sep = '&', start = url)
title=start.tupels_to_lines(list_product_title)
fileName=start.tupels_to_lines(list_product_fileName,sep='_')

list_languages = start.names_from_pairs(list_pairs_1)

if(not jsonEz.check(strftime)):
	dict_new = collect.collect(url, jsonStr)
	jsonEz.save(strftime, dict_new)

if(now.weekday()==0  or TESTMODE):
	plotter.draw(list_product_title, list_languages, jsonStr, fileName, strftime, mode='Week')
if(now.day==1):
	plotter.draw(list_product_title, list_languages, jsonStr, fileName, strftime, mode='Month',lastMonth=lastMonth)
