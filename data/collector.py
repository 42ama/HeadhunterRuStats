#Инструменты для работы с интернетом
from bs4 import BeautifulSoup 
import requests

import progressbar as pb#красивое отображение процесса во время сбора инфы 


def collect(list_url, list_jsonStr, 
			params=('h1', {'class':'header', 'data-qa':'page-title'}), 
			headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}, 
			startswith="По запросу"):
	c=0;
	dict_out={}
	for url in list_url:
		pb.printProgressBar(c, len(list_url), prefix = 'Progress:', suffix = 'Complete', length = 50)
		r=requests.get(url,headers=headers)
		soup=BeautifulSoup(r.text, 'html.parser')
		resultList = soup.find(params)
		dataToProcess = str(resultList.next)
		if(not dataToProcess.startswith(startswith)):
			newStr = '';
			flag_nowNums=False
			for x in range(len(dataToProcess)):
				if(not flag_nowNums and not dataToProcess[x].isdigit()):
					continue
				elif(not flag_nowNums):
					flag_nowNums=True
				if(dataToProcess[x].isdigit()):
					newStr+=dataToProcess[x]
				elif(dataToProcess[x].isspace()):
					if(dataToProcess[x+1].isdigit()):
						continue
					else:
						break
				else:
					break
			dict_out[list_jsonStr[c]]=int(newStr)
			#dict_out[list_url[c]]=int(newStr)
		else:
			dict_out[list_jsonStr[c]]=None
		c+=1;	
	return dict_out
