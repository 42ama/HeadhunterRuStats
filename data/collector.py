#Инструменты для работы с интернетом
from bs4 import BeautifulSoup 
import requests

from . import progressbar as pb#красивое отображение процесса во время сбора инфы 


def collect(list_url, list_jsonStr, 
			params=('h1', {'class':'header', 'data-qa':'page-title'}), 
			headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}, 
			startswith="По запросу"):
	c=0;
	dict_out={}
	for url in list_url:
		pb.printProgressBar(c, len(list_url), prefix = 'Progress:', suffix = 'Complete', length = 50)
		r=requests.get(url,headers=headers)#Подключаемся к сайту
		soup=BeautifulSoup(r.text, 'html.parser')#Получаем объект для парсина
		resultList = soup.find_all(params)#Собираем объекты по вручную определенным параметрам - даёт доступ к числу вакансий который hh.ru выводит
		dataToProcess = str(resultList[1].next)
		if(not dataToProcess.startswith(startswith)):
			#Получаем строку вида:"Найдено 14 828 вакансий" и пробираемся через неё цепляя цифры
			newStr = '';
			flag_nowNums=False
			for x in range(len(dataToProcess)):
				if(not flag_nowNums and not dataToProcess[x].isdigit()):
					#ничего не делаем, пока не найдем первое число
					continue
				elif(not flag_nowNums):
					#нашли первое число - ставим отметку
					flag_nowNums=True
				if(dataToProcess[x].isdigit()):
					#если цифра - забираем
					newStr+=dataToProcess[x]
				elif(dataToProcess[x].isspace()):
					#если пробел и дальше цифра - продолжаем, иначе говорим что сбор окончен
					if(dataToProcess[x+1].isdigit()):
						continue
					else:
						break
				else:
					#если не пробел и не цифра - заканчиваем с ссылкой
					break
			dict_out[list_jsonStr[c]]=int(newStr)
		else:
			#По данному запорсу ничего не найдено
			dict_out[list_jsonStr[c]]=None
		c+=1;	
	return dict_out
