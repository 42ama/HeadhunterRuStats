#Инструменты для работы с интернетом
from bs4 import BeautifulSoup 
import requests

#Для отрисовки графиков
import matplotlib.pyplot as plt

#Для хранения файлов
import json

#Просто полезные вещи используемые в паре мест
import os#для сохранения графиков
import itertools#для составления ссылок из списка списков
import datetime#для составления названия json файла
import progressbar#красивое отображение процесса во время сбора инфы
import urllib#для перекодирования названий в юрл формат
'''
https://samara.hh.ru/search/vacancy?area=78&&clusters=true&enable_snippets=true&text=c%23

clusters=true&enable_snippets=true&text=python&area=2&from=cluster_area - чот системное попробывать оставить включеным

https://samara.hh.ru/search/vacancy? - основа
text=python - Питон
&area=78 - Самара
area=2 - СПБ
&experience=noExperience&from=cluster_experience - Нет Опыта
&experience=between1And3&from=cluster_experience - 1..3 года опыта

text=c%23
Парметры text:
python
c%23
unity
javascript
Data+science


<h1 class="header" data-qa="page-title">
        5 790 вакансий «python»
       </h1>


'https://hh.ru/search/vacancy?text=unity'
Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0


НЕ НАЙДЕНО =  "По запросу «data science» ничего не найдено""
'''

class HHStats:
	def __init__(self, incomedList):

		self.dataDictionary = {}
		self.urlList=[]
		self.namesList=[]

		self.now = datetime.datetime.now()
		self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}

		url='https://samara.hh.ru/search/vacancy?clusters=true&enable_snippets=true&'
		#["text=python&","text=c%23&","text=unity&","text=data+science&","text=javascript&"]
		mainList = [[],
					["","area=2&","&area=78&"],					
					["","experience=noExperience&from=cluster_experience&","experience=between1And3&from=cluster_experience&"]
					]
		compatibleList = 	[[],
								["Россия", "Санкт-Петербург", "Самара"],
								["","Нет опыта работы","1..3 года опыта"]]

		compatibleList[0] = incomedList
		for x in compatibleList[0]:
			mainList[0].append('text='+urllib.parse.quote_plus(x)+'&')

		mainListProducts = list(itertools.product(*mainList))
		compatibleListProducts = list(itertools.product(*compatibleList))

		for x in mainListProducts:
			newurl = url
			for y in x:
				newurl += y
			self.urlList.append(newurl)
		for x in compatibleListProducts:
			newName = ""
			for y in x:
				newName += " " + y
			self.namesList.append(newName[1:])
		#self.urlList=["https://samara.hh.ru/search/vacancy?text=unity&only_with_salary=false&clusters=true&area=78&enable_snippets=true&","https://samara.hh.ru/search/vacancy?clusters=true&enable_snippets=true&text=C%23&experience=noExperience&from=cluster_experience"]
		

	def collectData(self):
		c=0;
		for url in self.urlList:
			progressbar.printProgressBar(c, len(self.urlList), prefix = 'Progress:', suffix = 'Complete', length = 50)
			r=requests.get(url,headers=self.headers)
			soup=BeautifulSoup(r.text, 'html.parser')
			resultList = soup.find('h1', {'class':'header', 'data-qa':'page-title'})
			dataToProcess = str(resultList.next)
			if(not dataToProcess.startswith("По запросу")):
				newStr = '';
				for x in range(len(dataToProcess)):
					if(dataToProcess[x].isdigit()):
						newStr+=dataToProcess[x]
					elif(dataToProcess[x].isspace()):
						if(dataToProcess[x+1].isdigit()):
							continue
						else:
							break
					else:
						break
				self.dataDictionary[self.namesList[c]]=int(newStr)
				#self.dataDictionary[self.urlList[c]]=int(newStr)
			else:
				self.dataDictionary[self.namesList[c]]=None
			c+=1;

	def saveJson(self):
		fileName = self.now.strftime("%Y_%m_%d")+'.json'#___%H_%M добавить в название для часов и минут
		with open(fileName, 'w') as fp:
			json.dump(self.dataDictionary, fp)

	def loadJson(self):
		fileName = self.now.strftime("%Y_%m_%d")+'.json'#___%H_%M добавить в название для часов и минут
		with open(fileName, 'r') as fp:
			self.dataDictionary = json.load(fp)

	def petrifyToTxt(self):
		with open("out.txt", "w", encoding='utf-8') as f:
			f.write(soup.prettify())

	def save(name='', fmt='png'):
		pwd = os.getcwd()
		iPath = '{}'.format(fmt)
		if not os.path.exists(iPath):
			os.mkdir(iPath)
		os.chdir(iPath)
		plt.savefig('{}.{}'.format(name, fmt), fmt='png')
		os.chdir(pwd)
		#plt.close()

	def drawingPlot(self):
		#https://nbviewer.jupyter.org/github/whitehorn/Scientific_graphics_in_python/blob/master/P1%20Chapter%201%20Pyplot.ipynb
		fig = plt.figure()   # Создание объекта Figure
		print(fig.axes)   # Список текущих областей рисования пуст
		print(type(fig))   # тип объекта Figure
		plt.scatter(1.0, 1.0)   # scatter - метод для нанесения маркера в точке (1.0, 1.0)
		
		# После нанесения графического элемента в виде маркера
		# список текущих областей состоит из одной области
		print (fig.axes)
		
		# смотри преамбулу
		#save(name='pic_1_4_1', fmt='pdf')
		#save(name='pic_1_4_1', fmt='png')
		plt.savefig('{}.{}'.format('pic_1_4_1', 'png'))
		plt.show()


print("loaded")
if __name__ == '__main__':
	print("also loaded as main")
	Sample=HHStats(["Python","C#","Unity","Data science","JavaScript"])
	Sample.collectData()
	Sample.saveJson()
	#Sample.loadJson()
	#Sample.drawingPlot()
