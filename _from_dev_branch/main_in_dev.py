from collections import namedtuple

import datetime

import data._iter
import data.gui_elements

import data.collector as collect#......сбор инфы с хх
import data.jsonEz as jsonEz#..........сохраниение в формате жсон

url='https://samara.hh.ru/search/vacancy?clusters=true&enable_snippets=true&'

main_list = [['Python','C#','Data science','JavaScript'],
			['Санкт-Петербург', 'Самара','Россия'],
			['Любой опыт работы','Нет опыта работы','1..3 года опыта']]

Appeals = namedtuple('Appeal', ['field_type', 'dictionary','additional'])
area_apls = Appeals('area', {'Санкт-Петербург':'2',
							'Самара':'78',
							'Россия':''}, 
					'')

exp_apls = Appeals('experience',{'Нет опыта работы':'noExperience',
								'1..3 года опыта':'between1And3',
								'Любой опыт работы':''},
					'from=cluster_experience')

text_field = data.gui_elements.URLQuoteFiled('text')
area_field = data.gui_elements.CompareField(area_apls.field_type, area_apls.dictionary, additional=area_apls.additional)
exp_field = data.gui_elements.CompareField(exp_apls.field_type, exp_apls.dictionary, additional=exp_apls.additional)

text_list = []
area_list = []
exp_list = []


for x in main_list[0]:
	text_field(x)
	text_list.append((text_field.orig(), text_field.reform()))

for x in main_list[1]:
	try:
		_compare = area_apls.dictionary[x]
	except KeyError:
		_compare = "Error: Not such key founded"
		continue
	if not _compare == '':
		area_field(x)
		area_list.append((area_field.orig(), area_field.reform()))
	else:
		area_list.append((x, ''))

for x in main_list[2]:
	try:
		_compare = exp_apls.dictionary[x]
	except KeyError:
		_compare = "Error: Not such key founded"
		continue
	if not _compare == '':
		exp_field(x)
		exp_list.append((exp_field.orig(), exp_field.reform()))
	else:
		exp_list.append((x, ''))

res1 = data._iter.unpack(text_list,area_list,exp_list)
comb_lists=[]
comb_lists.append(data._iter.comb(*res1[0]))
comb_lists.append(data._iter.comb(*res1[1],sep=''))
#[[список строк с человеческим названием][список строк с юрл отображением]]

now = datetime.date.today()
strftime = now.strftime("%Y_%m_%d")

#if(not jsonEz.check(strftime)):
dict_new = collect.collect(comb_lists[1], comb_lists[0], url)
jsonEz.save(strftime, dict_new)