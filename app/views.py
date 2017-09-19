#coding:utf-8
from flask import *
from app import app

import re
import baiduip
import sys
import requests
import cms
from password import PasswdGenerator
from sqlapi import AutoSqli
from struct import s7star

import whois
import skg
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')

@app.route('/',methods=["GET","POST"])
def index():
    return render_template('ip.html')

@app.route('/ip',methods=["GET","POST"])
def BaiduIp():
	if request.method == 'POST':
	    ip = request.form.get("search")
	    addr=ip.strip().split('.')  #切割IP地址为一个列表
	    if len(addr) != 4:
	        return "IP ERROR!"
	    data = baiduip.search()
	    return render_template('ip.html',data=data)
	else:
		return render_template('ip.html')


#CMS在线识别
@app.route('/webdna',methods=["GET","POST"])
def webdna():
    if request.method == 'POST':
        url = request.form.get("search")
        if re.match(r'^https?:/{2}\w.+$', url):
            data = cms.cms(url)
            print data
            if data is False:
                print u"没有找到合适的CMS"
        return render_template('cms.html',data=data,title="CMS识别")
    else:
        return render_template('cms.html',title="CMS识别")

@app.route('/password/',methods=['GET','POST'])
def password_build():
    if request.method == 'POST':
        from flask import make_response
        birthday = request.form.get("birthday","")
        fullname = request.form.get("fullname","")
        nickname = request.form.get("nickname","")
        englishname = request.form.get("englishname","")
        partnername = request.form.get("partnername","")
        phone = request.form.get("phone","")
        qq = request.form.get("qq","")
        company = request.form.get("company","")
        domain = request.form.get("domain","")
        oldpasswd = request.form.get("oldpasswd","")
        keywords = request.form.get("keywords","")
        keynumbers = request.form.get("keynumbers","")
        pwgen = PasswdGenerator(fullname=fullname,nickname=nickname,englishname=englishname,partnername=partnername,phone=phone,qq=qq,company=company,domain=domain,oldpasswd=oldpasswd,keywords=keywords,keynumbers=keynumbers,birthday=birthday)
        wordlist = pwgen.generate()
        content = '\n'.join(wordlist)#让列表成为一个一行的字符串
        print wordlist
        #content = "long text"
        response = make_response(content)
        response.headers["Content-Disposition"] = "attachment; filename=pass.txt"#让用户直接下载pass.txt文件
        return response
        #return render_template('password.html',data=wordlist,title="社工密码生成")
    else:
        return render_template('password.html',title="社工密码生成")

#Whois 在线查询
@app.route('/whois',methods=["GET","POST"])
def whoisa():
    if request.method == 'POST':
        url = request.form.get("search")
        data = whois.whois(url).replace("\n","</br>")
        print data
        return render_template('whois.html',data=data,title="Whois查询")
    else:
        return render_template('whois.html',title="Whois查询")

#社工库查询
@app.route('/pass',methods=['GET','POST'])  
def findpass():
    if request.method == 'POST':
        p = request.form.get('search',"")
        print p 
        data = skg.findpass(p)
        return render_template('skg.html',data=data,title="社工库查询")
    else:
        return render_template('skg.html',title="社工库查询")



#集成wooyun漏洞平台
@app.route('/wooyun',methods=['GET','POST'])
@app.route('/wooyun/<int:pages>',methods=['GET','POST'])
def wooyun(pages=0):
    conn = MySQLdb.connect('localhost','root','root','wooyun',charset='utf8')
    cursor = conn.cursor()
    searchword = request.args.get('key','').strip()
    log_id = request.args.get('id','').strip()
    data = {}
    table = list()
    if log_id:
        cursor.execute(MySQLdb.escape_string("select * from emlog_blog where gid=%s"%log_id))
        results = cursor.fetchone()
        #print results
        data["id"] = results[0]
        data["text"] = results[2]
        data["title"] = results[1]
    if searchword:
        sql = 'select gid,title from emlog_blog where title like"%%%s%%"'%(searchword)
        cursor.execute(sql)
        results = cursor.fetchall()

        for rows in results:
            tdata = {}
            tdata["id"] = rows[0]
            tdata["title"] = rows[1]
            table.append(tdata)
    return render_template("wooyun.html",title="乌云漏洞平台",data=data,table=table)

@app.route('/wooyun1',methods=['GET','POST'])
@app.route('/wooyun1/<int:pages>',methods=['GET','POST'])
def wooyun1(pages=0):
    conn = MySQLdb.connect('localhost','root','root','wooyun',charset='utf8')
    cursor = conn.cursor()
    if pages is None:
        pages = 0
    if pages < 0:
        pages = 0
    sql = 'select gid,title from emlog_blog where content like "%%%s%%" limit %d,%d'%("无影响厂忽略",pages*20,20)
    cursor.execute(sql)
    results = cursor.fetchall()
    table = list()
    for rows in results:
        tdata = {}
        tdata["id"] = rows[0]
        tdata["title"] = rows[1]
        table.append(tdata)
    return render_template("wooyun.html",title="乌云忽略漏洞查询",table=table,next=pages+1,prev = pages-1)


@app.route('/sqlapi',methods=['GET','POST'])
def sqlapi():
    if request.method == 'POST':
        url = request.form.get('search','')
        t = AutoSqli('http://127.0.0.1:8775',url)
        t.run()
        data = t.get_data()
        print data
        return render_template('sqlapi.html',title="注入检测",data=data,url = url)
    else:
        return render_template('sqlapi.html',title="注入检测")

@app.route('/struct',methods=['GET','POST'])
def struct():
    if request.method == 'POST':
        url = request.form.get('search','')
        s = s7star()
        res = s.poc(url)
        html = requests.get(url).content
        url_title = re.findall('<title>(.*?)</title>',html)
        print res
        return render_template('struct.html',title="s2-045漏洞检测",data=res,url = url,url_title=url_title)

    else:
        return render_template('struct.html',title="s2-045漏洞检测")

