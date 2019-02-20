#Инструменты для работы с интернетом
from bs4 import BeautifulSoup 
import requests

#Для отрисовки графиков
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

#Для хранения файлов
import json

#Просто полезные вещи используемые в паре мест
import os#для сохранения графиков
import glob#получаем список файлов в папке
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
		self.incomedList=incomedList
		url='https://samara.hh.ru/search/vacancy?clusters=true&enable_snippets=true&'
		#["text=python&","text=c%23&","text=unity&","text=data+science&","text=javascript&"]
		self.colorList=['blue','green','red','cyan','black','yellow','gray']
		tagList=[['Everyweek','Everymonth'],
							['Russia','Samara'],
							['Absolute','Relate']]
		titleList=[['Еженедельные','Ежемесячные'],
						['России','Самаре'],
						['абсолютная','относительная']]
		#{Ежемесячные} тренды по языкам в {России}\n({абсолютная} статистика)
		self.mainList = [[],
					["","area=2&","&area=78&"],					
					["","experience=noExperience&from=cluster_experience&","experience=between1And3&from=cluster_experience&"]
					]
		compatibleList = 	[[],
								["Россия", "Санкт-Петербург", "Самара"],
								["","Нет опыта работы","1..3 года опыта"]]

		compatibleList[0] = self.incomedList
		for x in compatibleList[0]:
			self.mainList[0].append('text='+urllib.parse.quote_plus(x)+'&')

		mainListProducts = list(itertools.product(*self.mainList))
		compatibleListProducts = list(itertools.product(*compatibleList))
		self.tagListProducts=list(itertools.product(*tagList))
		self.titleListProducts=list(itertools.product(*titleList))

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
		self.langAllAny_exp = []
		for c in range(len(self.namesList)):
			if(c%(len(self.mainList)*len(self.mainList[1]))==0):
				self.langAllAny_exp.append(c)
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
		fileName = 'data/{}.json'.format(self.now.strftime("%Y_%m_%d"))#___%H_%M добавить в название для часов и минут
		with open(fileName, 'w') as fp:
			json.dump(self.dataDictionary, fp)

	def loadJson(self,fileName=None):
		if(fileName==None):
			fileName = 'data/{}.json'.format(self.now.strftime("%Y_%m_%d"))#___%H_%M добавить в название для часов и минут
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
		#plt.close()  'plots/'
	def AbsPlot(self,fig):
		x=np.array(range(0,-len(self.dataList),-1))
		c=0
		for oneList in self.dataList:
			y=np.array(oneList)
			plt.plot(x,y,color=self.colorList[c], linewidth=1, linestyle='--', label=self.incomedList[c])
			plt.scatter(x, y, marker='.', s=20, color=self.colorList[c])
			#plt.text(-0.5, oneList[0]+600, self.incomedList[c], fontsize=12, bbox=dict(edgecolor='w', color='w'))
			#ax.plot(x+1, y, color=self.colorList[c], linewidth=1, label=self.incomedList[c])
			c+=1
	def RelPlot(self,fig):
		x=np.array(range(0,-len(self.dataList),-1))
		c=0
		#for oneList in self.dataList:
		#	for x in oneList[1:]:
		#		x=
		#	y=np.array(oneList)
		pass
	def drawPlot(self):
		#for x in range(len(self.tagListProducts)):
		#	fileName=
		self.getDataFromJson(self.getNlast())
		for x in self.dataList:
			print(x)
		fig = plt.figure()   # Создание объекта Figure
		fig.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
		plt.title('Тренды по языкам в России за последние 10 дней\n(абсолютная статистика)')
		plt.xlabel('Дни')
		plt.ylabel('Кол-во вакансий')
		plt.grid(b=True,alpha=0.3)
		self.AbsPlot(fig)
		plt.legend(loc='upper right', bbox_to_anchor=(1.12, 0.95))
		#plt.savefig('plots/{}_abs.png'.format(self.now.strftime("%Y_%m_%d")), fmt='png')#.format(name, fmt)
		plt.show()
		

	def getNlast(self, n=10):
		list_of_files = glob.glob('data/*.json') # * means all if need specific format then *.csv
		fromLastToFirst = []
		if(n>len(list_of_files)):
			n=len(list_of_files)
		for x in range(n):
			latest_file = max(list_of_files, key=os.path.getctime)
			fromLastToFirst.append(latest_file)
			list_of_files.remove(latest_file)
		return fromLastToFirst

	def getDataFromJson(self,listFiles):
		#['data\\2019_02_19.json', 'data\\2019_02_18.json'...]
		self.dataList=[]
		for x in listFiles:
			self.loadJson(x)
			tempList=[]
			for c in self.langAllAny_exp:
				tempList.append(self.dataDictionary[self.namesList[c]])
			self.dataList.append(tempList)
		self.dataList.reverse()#originaly: 0-newest..n-oldest, after reverse: 0-oldest..n-newest
		self.dataList=list(map(list, zip(*self.dataList)))#each sublist is принадлежит одной линии
		



print("loaded")
if __name__ == '__main__':
	print("also loaded as main")
	Sample=HHStats(["Python","C#","Unity","Data science","JavaScript"])
	#Sample.collectData()
	#Sample.saveJson()
	#Sample.loadJson()
	Sample.drawPlot()