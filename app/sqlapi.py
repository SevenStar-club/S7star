#coding:utf-8

import requests
import json
import time
from pprint import *

class AutoSqli(object):
	def __init__(self,server='',target='',data='',referer='',cookie=''):
		super(AutoSqli,self).__init__()
		self.server = server
		if self.server[-1] != '/':#厉害，规则化url
			self.server = self.server + '/'
		self.target = target
		self.taskid = ''
		self.engineid = ''
		self.status = ''
		self.data = data
		self.detail = {}
		self.referer = referer
		self.cookie = cookie
		self.start_time = time.time()

	#新建扫描任务
	def task_new(self):
		html = requests.get(self.server+'task/new').text
		# print html
		self.taskid = json.loads(html)['taskid']
		print 'Created new task:' + self.taskid
		if len(self.taskid) > 0 :
			return True 
		return False 

	#新建删除任务
	def task_delete(self):
		html = requests.get(self.server+'task/'+self.taskid+'/delete').text
		# print html
		if json.loads(html)['success']:
			print '[%s] Delete task'%(self.taskid)
			return True 
		return False
	#扫描任务开始
	def scan_start(self):
		headers = {'Content-Type':'application/json'}
		payload = json.dumps({'url':self.target})
		html = requests.post(url=self.server+'scan/'+self.taskid+'/start',data=payload,headers=headers).text
		# print html
		self.engineid = json.loads(html)['engineid']
		if len(str(self.engineid)) > 0 and json.loads(html)['success']:
			print 'Started scan'
			return True 
		return False

	#扫描任务的状态
	def scan_status(self):
		html = requests.get(url=self.server+'scan/'+self.taskid+'/status').text
		# print html
		data = json.loads(html)
		self.status = data['status']
		if self.status == 'running':
			return 'running'
		elif self.status == 'terminated':
			return 'terminated'
		else:
			return 'error'

	#扫描任务的细节
	def scan_data(self):
		html = requests.get(url=self.server+'scan/'+self.taskid+'/data').text
		# print html 
		self.data = json.loads(html)['data']
		# pprint(self.data) 
		detail = {}
		if len(self.data) == 0:
			print 'not injection:\t'
		else:
			print 'injection:\t'+self.target
			detail['success'] = json.loads(html)["success"]
			tmp = self.data[0]["value"][0]
			detail["parameter"] = tmp["parameter"]
			detail["place"] = tmp["place"]
			detail['info'] = list()
			for i in tmp["data"]:
				t = {}
				t['title'] = tmp["data"][i]["title"]
				t['payload'] = tmp["data"][i]["payload"]
				detail['info'].append(t)

			detail["dbms"] = tmp["dbms"]
			detail["dbms_version"] =tmp["dbms_version"]
			pprint(detail)
			self.detail = detail 



	#扫描的设置，主要是参数的设置
	def option_set(self):
		headers = {'Content-type':'application/json'}
		option = json.dumps({'options':{
			'smart':True,
		}})
		url = self.server + 'option/' + self.taskid + '/set'
		html = requests.post(url,data=option,headers=headers).text 
		t = json.loads(html)
		print 'option set:',t 

	#停止扫描任务
	def scan_stop(self):
		t = json.loads(requests.get(self.server+'scan/'+self.taskid+'/stop').text)['success']
		print t
	#杀死扫描任务
	def scan_kill(self):
		t = json.loads(requests.get(self.server+'scan/'+self.taskid+'/kill').text)['success']
		print t

	#开始任务
	def run(self):
		if not self.task_new():
			return False 
		self.option_set()
		if not self.scan_start():
			return False 
		while True:
			if self.scan_status() == 'running':
				time.sleep(5)
			elif self.scan_status() == 'terminated':
				break 
			else:
				break 
			print time.time() - self.start_time
			if time.time() - self.start_time > 3000:#防止任务超时
				error = True 
				self.scan_stop()
				self.scan_kill()
				break 
		self.scan_data()
		self.task_delete()
		print time.time() - self.start_time

		# self.option_set()
		# self.scan_start()
		# self.scan_status()
		# time.sleep(5)
		# self.scan_data()

		# if not self.task_delete():
		# 	return False
	#返回数据
	def get_data(self):
		return self.detail
if __name__ == '__main__':
	t = AutoSqli('http://127.0.0.1:8775','http://testphp.vulnweb.com/artists.php?artist=1')
	t.run()
	#test url1:http://testphp.vulnweb.com/artists.php?artist=1
	#test url2:http://192.168.1.108/ctf/sql/sql.php?u=lj