#import urllib#для перекодирования названий в юрл формат
import itertools#для составления ссылок из списка списков

list_pairs_1 = [('Python', 'python'),
				('C#', 'c%23'),
				('Unity', 'unity'),
				('Data Science', 'data+science'),
				('JavaScript', 'javascript'),
				(),
				('Россия', ''),
				('Санкт-Петербург', 'area=2'),
				('Самара', 'area=78'),
				(),
				('',''),
				('Нет опыта работы','experience=noExperience&from=cluster_experience&'),
				('1..3 года опыта', 'experience=between1And3&from=cluster_experience'),
				()
				]
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

def pairs_to_lists(list_pairs):
	list_a=[]
	list_b=[]
	list_out1=[]
	list_out2=[]
	for x in list_pairs:
		if(len(x)!=0):
			list_a.append(x[0])
			list_b.append(x[1])
		else:
			list_out1.append(list_a)
			list_out2.append(list_b)
			list_a=[]
			list_b=[]
	return (list_out1, list_out2)
def tupels_to_lines(_list,start='',sep=' '):
	list_res = []
	for x in _list:
		line=start+x[0]
		for y in x[1:]:
			line+=sep+y
		list_res.append(line)
	return(list_res)
list_titles, list_tags = pairs_to_lists(list_pairs_1)
list_names, list_calls = pairs_to_lists(list_pairs_2)
list_product_titles = list(itertools.product(*list_titles))#Питон, Россия, Самара
list_product_tags = list(itertools.product(*list_tags))#python, ,area=78 sep=&
list_product_names = list(itertools.product(*list_names))#Ежемесячные, Самаре, абс
list_product_calls = list(itertools.product(*list_calls))#Year, Samara, Abs sep=_
titles=tupels_to_lines(list_product_titles)
tags=tupels_to_lines(list_product_tags,sep='&')
names=tupels_to_lines(list_product_tags)
calls=tupels_to_lines(list_product_calls,sep='_')