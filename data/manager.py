import os
import glob

from . import jsonEz

def _getAllNLine(length,n):
	list_out=[]
	for c in range(length):
		if((c%9)==n):
			list_out.append(c)
	return(list_out)

def list_data(jsonStr, ePos, name='*', n=10):
	#['data\\2019_02_19.json', 'data\\2019_02_18.json'...]
	list_of_files = glob.glob('json/{}.json'.format(name)) # * means all if need specific format then *.csv
	list_sorted = []
	if(n>len(list_of_files)):
		n=len(list_of_files)
	for x in range(n):
		latest_file = max(list_of_files, key=os.path.getctime)
		list_sorted.append(latest_file)
		list_of_files.remove(latest_file)
	list_data=[]
	list_ePos=_getAllNLine(len(jsonStr),ePos)
	for x in list_sorted:
		dict_temp = jsonEz.load(x)
		tempList=[]
		for c in list_ePos:
			tempList.append(dict_temp[jsonStr[c]])
		list_data.append(tempList)
	list_data.reverse()#originaly: 0-newest..n-oldest, after reverse:0-oldest..n-newest
	list_data=list(map(list, zip(*list_data)))#each sublist is принадлежитодной лини
	return list_data