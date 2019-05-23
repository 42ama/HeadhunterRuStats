#Для отрисовки графиков
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import numpy as np

from . import manager

#Цвета линий на графиках, если данных будет больше чем цветов в массиве - БУМ
list_colors=['blue','green','red','cyan','black','yellow','gray']

def draw(list_product_title, list_languages, jsonStr, list_fileName, strftime, mode='Week',lastMonth=''):
	for x in range(len(list_product_title)):
		#Формируем подпись графика и название файла
		#{Ежемесячные} тренды по языкам в {России}\n({абсолютная} статистика)
		title = '{0} тренды по языкам в {1}\n({2} статистика)'.format(
												list_product_title[x][0],
												list_product_title[x][1],
												list_product_title[x][2])
		fileName = 'plots/{}_{}.png'.format(strftime,
											list_fileName[x])

		if('Week' in fileName and mode == 'Week'):
			n=10
			name='*'
		elif('Month' in fileName and mode == 'Month'):
			n=31
			name=lastMonth+"*"
		elif('Year' in fileName and mode == 'Year'):
			continue
		else:
			continue
		if('Russia' in fileName):
			elementPostitons=0
		else:
			elementPostitons=6


		fig = plt.figure()   # Создание объекта Figure
		fig.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
		plt.title(title)
		plt.xlabel('Дни')
		plt.ylabel('Кол-во вакансий')
		plt.grid(b=True,alpha=0.3)

		list_sortedData = manager.list_data(jsonStr, elementPostitons, name=name, n=n) #Собираем json файлы с каталога

		if('Abs' in fileName):
			__AbsPlot(list_sortedData, list_languages, fig)
		else:
			__RelPlot(list_sortedData, list_languages, fig)

		plt.legend(loc='lower left', bbox_to_anchor=(0.8, 0.6))
		print(fileName)
		plt.savefig(fileName, fmt='png')
		#plt.show()

def __AbsPlot(list_data,list_languages,fig):
	c=0
	for _list in list_data:
		x=np.array(range(0,-len(_list),-1))
		y=np.array(_list)
		plt.plot(x,y,color=list_colors[c], linewidth=1, linestyle='--', label=list_languages[c])
		plt.scatter(x, y, marker='.', s=20, color=list_colors[c])
		c+=1

def __RelPlot(list_data,list_languages,fig):
	c=0
	for _list in list_data:
		x=np.array(range(-1,-len(_list),-1))
		for i in range(1,len(_list)):
			_list[i]=(_list[i]/_list[0])
		_list.pop(0)
		y=np.array(_list)
		plt.plot(x,y,color=list_colors[c], linewidth=1, linestyle='--', label=list_languages[c])
		plt.scatter(x, y, marker='.', s=20, color=list_colors[c])
		c+=1


