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
	def __init__(self, incomedList, test=False):
		self.test=test
		self.dataDictionary = {}
		self.urlList=[]
		self.namesList=[]
		self.dataList_month=[]
		self.now = datetime.datetime.now()
		self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}
		self.incomedList=incomedList
		url='https://samara.hh.ru/search/vacancy?clusters=true&enable_snippets=true&'
		#["text=python&","text=c%23&","text=unity&","text=data+science&","text=javascript&"]
		self.colorList=['blue','green','red','cyan','black','yellow','gray']
		tagList=[['Week','Month','Year'],
							['Russia','Samara'],
							['Absolute','Relate']]
		titleList=[['Ежедневные','Ежедневные','Ежемесячные'],
						['России','Самаре'],
						['абсолютная','относительная']]
		#{Ежемесячные} тренды по языкам в {России}\n({абсолютная} статистика)
		mainList = [[],
					["","area=2&","&area=78&"],					
					["","experience=noExperience&from=cluster_experience&","experience=between1And3&from=cluster_experience&"]
					]
		compatibleList = 	[[],
								["Россия", "Санкт-Петербург", "Самара"],
								["","Нет опыта работы","1..3 года опыта"]]

		compatibleList[0] = self.incomedList
		for x in compatibleList[0]:
			mainList[0].append('text='+urllib.parse.quote_plus(x)+'&')

		mainListProducts = list(itertools.product(*mainList))
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
		self.chooseDataList=[]
		langAllAny_exp = []
		langSamaraAny_exp = []
		def getAllNLine(out,n=0):
			for c in range(len(self.namesList)):
				if(c%(len(mainList)*len(mainList[1]))==n):
					out.append(c)
		getAllNLine(langAllAny_exp,n=0)
		getAllNLine(langSamaraAny_exp,n=6)
		self.chooseDataList.append(langAllAny_exp)
		self.chooseDataList.append(langSamaraAny_exp)
		#self.urlList=["https://samara.hh.ru/search/vacancy?text=unity&only_with_salary=false&clusters=true&area=78&enable_snippets=true&","https://samara.hh.ru/search/vacancy?clusters=true&enable_snippets=true&text=C%23&experience=noExperience&from=cluster_experience"]
	

	def collectAndSaveData(self):
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
		self.saveJson()
	


	def drawPlot(self):
		if(self.now.weekday()==0 or self.now.day==1 or self.test==True):
			if(self.now.month != 1):
				dateObj=datetime.datetime(self.now.year,self.now.month,self.now.day)#MONTH - 1 !!!!!!!!!!!!!
			else:
				dateObj=datetime.datetime(self.now.year-1,1,self.now.day)		
			for x in range(len(self.tagListProducts)):
				fileName = 'plots/{0}_{1}{2}{3}.png'.format(self.now.strftime("%Y_%m_%d"),
														self.tagListProducts[x][0],
														self.tagListProducts[x][1],
														self.tagListProducts[x][2])
				#{Ежемесячные} тренды по языкам в {России}\n({абсолютная} статистика)
				title = '{0} тренды по языкам в {1}\n({2} статистика)'.format(
														self.titleListProducts[x][0],
														self.titleListProducts[x][1],
														self.titleListProducts[x][2])
				if('Week' in self.tagListProducts[x][0]):
					if(self.now.weekday()==0 or self.test==True):
						n=10
						name='*'
					else:
						continue
				elif('Month' in self.tagListProducts[x][0]):	
					if(self.now.day == 1 or self.test==True):
						n=31
						name=dateObj.strftime("%Y_%m_*")
						self.PrepareMonthMiddle(dateObj)
					else:
						continue
				else:#Year
					continue
				if('Russia' in self.tagListProducts[x][1]):
					dataList_name='Russia'
				else:
					dataList_name='Samara'
				fig = plt.figure()   # Создание объекта Figure
				fig.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
				plt.title(title)
				plt.xlabel('Дни')
				plt.ylabel('Кол-во вакансий')
				plt.grid(b=True,alpha=0.3)
				self.getDataFromJson(self.getNlast(name=name,n=n),dataList_name=dataList_name)
				if('Absolute' in self.tagListProducts[x][2]):
					self.AbsPlot(fig)
				else:
					self.RelPlot(fig)
				plt.legend(loc='lower left', bbox_to_anchor=(1, 1))#, bbox_to_anchor=(1.12, 0.95))#loc='upper right', bbox_to_anchor=(1.12, 0.95))
				plt.savefig(fileName, fmt='png')#'plots/{}_abs.png'.format(self.now.strftime("%Y_%m_%d")), fmt='png')#.format(name, fmt)
				#plt.show()
		else:
			print("Sorry, today no plots")


	def AbsPlot(self,fig):
		#x=np.array(range(0,-len(self.dataList),-1))
		c=0
		for oneList in self.dataList:
			x=np.array(range(0,-len(oneList),-1))
			y=np.array(oneList)
			plt.plot(x,y,color=self.colorList[c], linewidth=1, linestyle='--', label=self.incomedList[c])
			plt.scatter(x, y, marker='.', s=20, color=self.colorList[c])
			#plt.text(-0.5, oneList[0]+600, self.incomedList[c], fontsize=12, bbox=dict(edgecolor='w', color='w'))
			#ax.plot(x+1, y, color=self.colorList[c], linewidth=1, label=self.incomedList[c])
			c+=1
	def RelPlot(self,fig):
		c=0
		for oneList in self.dataList:
			x=np.array(range(-1,-len(oneList),-1))
			for i in range(1,len(oneList)):
				oneList[i]=(oneList[i]/oneList[0])
			oneList.pop(0)
			y=np.array(oneList)
			plt.plot(x,y,color=self.colorList[c], linewidth=1, linestyle='--', label=self.incomedList[c])
			plt.scatter(x, y, marker='.', s=20, color=self.colorList[c])
			c+=1


	def PrepareMonthMiddle(self,dateObj):
		#self.dataList_month
		for x in ['Russia','Samara']:
			self.getDataFromJson(self.getNlast(name=dateObj.strftime("%Y_%m_*"),n=31),dataList_name=x)
			monthMiddle = []
			for oneList in self.dataList:
				summ = 0
				for x in oneList:
					summ+=x
				summ/=len(oneList)
				monthMiddle.append(round(summ))
			self.dataList_month.append(monthMiddle)
		self.saveJson(name=dateObj.strftime("%Y_%m__tot"),data=self.dataList_month)
		#self.MonthData


	def getNlast(self,name='*', n=10):
		list_of_files = glob.glob('data/{}.json'.format(name)) # * means all if need specific format then *.csv
		fromLastToFirst = []
		if(n>len(list_of_files)):
			n=len(list_of_files)
		for x in range(n):
			latest_file = max(list_of_files, key=os.path.getctime)
			fromLastToFirst.append(latest_file)
			list_of_files.remove(latest_file)
		return fromLastToFirst	
	def getDataFromJson(self,listFiles,dataList_name='Russia'):
		#['data\\2019_02_19.json', 'data\\2019_02_18.json'...]
		self.dataList=[]
		if(dataList_name=='Russia'):
			dl_num=0
		elif(dataList_name=='Samara'):
			dl_num=1
		else:
			dl_num=0
		for x in listFiles:
			self.loadJson(x)
			tempList=[]
			for c in self.chooseDataList[dl_num]:
				tempList.append(self.dataDictionary[self.namesList[c]])
			self.dataList.append(tempList)
		self.dataList.reverse()#originaly: 0-newest..n-oldest, after reverse: 0-oldest..n-newest
		self.dataList=list(map(list, zip(*self.dataList)))#each sublist is принадлежит одной линии


	def saveJson(self,name=None,data=None):
		if(name==None):
			name=now.strftime("%Y_%m_%d")
		if(data==None):
			data=self.dataDictionary
		fileName = 'data/{}.json'.format(name)#___%H_%M добавить в название для часов и минут
		with open(fileName, 'w') as fp:
			json.dump(data, fp)
	def loadJson(self,fileName=None):
		if(fileName==None):
			fileName = 'data/{}.json'.format(self.now.strftime("%Y_%m_%d"))#___%H_%M добавить в название для часов и минут
		with open(fileName, 'r') as fp:
			self.dataDictionary = json.load(fp)


	def TodayIsSaved(self):
			fileName = 'data/{}.json'.format(self.now.strftime("%Y_%m_%d"))
			try:
				with open(fileName, 'w') as fp:
					pass
			except FileNotFoundError:
				return False
			else:
				return True
				#test = json.load(fp)



print("loaded")

if __name__ == '__main__':
	print("also loaded as main")
	Sample=HHStats(["Python","C#","Unity","Data science","JavaScript"])#,test=True)
	if(not Sample.TodayIsSaved()):
		Sample.collectAndSaveData()
	Sample.drawPlot()
	if(False):
		dateObj=datetime.datetime(2019,2,1)
		Sample.PrepareMonthMiddle(dateObj)