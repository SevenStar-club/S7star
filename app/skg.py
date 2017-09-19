import requests
from pprint import *
import json

def findpass(q):
	url = "http://www.fangzhuangku.com/function/pwdsearch.php"

	data = {'q':q}
	http = requests.post(url,data)
	res  = json.loads(http.content)
	sdata = res["data"]
	# pprint(sdata) 
	dic = []
	print len(sdata)
	if len(sdata):
		for key in sdata:
			for key1 in sdata[key]:
				ls_data = {'u':'','p':'','e':'','s':key}
				if 'u' in key1.keys():
					ls_data["u"] = key1["u"]
				if 'p' in key1.keys():
					ls_data["p"] = key1["p"]
				if 'e' in key1.keys():
					ls_data["e"] = key1["e"]
				dic.append(ls_data)
	# pprint(dic)
	return dic


	           

if __name__ == '__main__':
	findpass('wanggang')