import itertools#для составления ссылок из списка списков
import datetime

import data.starter as start#..........начальные преобразования списков
import data.collector as collect#......сбор инфы с хх
import data.jsonEz as jsonEz#..........сохраниение в формате жсон
import data.plotter as plotter#........рисование и сохранение графиков
import data.data_middle as data_middle#обработка собранной инфы за месяц

import hhrustats_setup

TESTMODE=hhrustats_setup.TESTMODE

#Иницилизация объектов даты, чтобы собирать информацию 1 раз в день. 
now = datetime.datetime.now()
strftime = now.strftime("%Y_%m_%d")

if(now.month != 1):
	lastMonth=datetime.datetime(now.year,now.month-1,now.day).strftime("%Y_%m_")
else:
	lastMonth=datetime.datetime(now.year-1,1,now.day).strftime("%Y_%m_")

#Основная юрл ссылка, к которой будут дописываться параметры
url='https://samara.hh.ru/search/vacancy?clusters=true&enable_snippets=true&text='


list_pairs_1 = hhrustats_setup.list_pairs_1
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

#Разбираем кортежи в списки значений
list_jsonStr, list_url = start.pairs_to_lists(list_pairs_1)
list_title, list_fileName = start.pairs_to_lists(list_pairs_2)

#Сочетаем значения всех блоков между собой
list_product_jsonStr = list(itertools.product(*list_jsonStr))#Питон, Россия, Самара
list_product_url = list(itertools.product(*list_url))#python, ,area=78 sep=&
list_product_title = list(itertools.product(*list_title))#Ежемесячные, Самаре, абс
list_product_fileName = list(itertools.product(*list_fileName))#Year, Samara, Abs sep=_

#Собираем сочетания в линии текста
jsonStr=start.tupels_to_lines(list_product_jsonStr)
url=start.tupels_to_lines(list_product_url,sep = '&', start = url)
title=start.tupels_to_lines(list_product_title)
fileName=start.tupels_to_lines(list_product_fileName,sep='_')

list_languages = start.names_from_pairs(list_pairs_1)

#Включаем парсер сайта и сохранение в json
if(not jsonEz.check(strftime) or TESTMODE):
	dict_new = collect.collect(url, jsonStr)
	jsonEz.save(strftime, dict_new)

#Строим графики
if(now.weekday()==0  or TESTMODE):
	plotter.draw(list_product_title, list_languages, jsonStr, fileName, strftime, mode='Week')
if(now.day==1):
	plotter.draw(list_product_title, list_languages, jsonStr, fileName, strftime, mode='Month',lastMonth=lastMonth)
