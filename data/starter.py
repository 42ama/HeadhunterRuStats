import itertools#для составления ссылок из списка списков

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

def names_from_pairs(list_paris):
	out_list = []
	for x in list_paris:
		if(len(x)!=0):
			out_list.append(x[0])
		else:
			break
	return(out_list)

def tupels_to_lines(_list,start='',sep=' '):
	list_res = []
	for x in _list:
		line=start+x[0]
		for y in x[1:]:
			line+=sep+y
		list_res.append(line)
	return(list_res)