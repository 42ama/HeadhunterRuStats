from . import jsonEz
from . import manager


def calculate_last_month_middle(jsonStr, lastMonth):
	list_monthData = []
	for x in (0, 6):
		list_sortedData = manager.list_data(jsonStr, x, name=lastMonth+'*', n=31)
		monthMiddle = []
		for _list in list_sortedData:
			summ = 0
			for x in _list:
				summ+=x
			summ/=len(_list)
			monthMiddle.append(round(summ))
		list_monthData.append(monthMiddle)
	jsonEz.save(lastMonth+'tot', list_monthData)