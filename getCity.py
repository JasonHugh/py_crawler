# -*- coding: utf-8 -*-
#获取搜房网所有的城市区域名称
__author__ = 'jaysonhu'
import inspect
import urllib2,urllib,time,MySQLdb
from bs4 import BeautifulSoup

def crawl(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
       'Referer':'http://hz.sofang.com'}
    try:
        request = urllib2.Request(url,headers=headers)
        response = urllib2.urlopen(request)
    except:
        print 'server connect failed'
        exit()
    
    return parse(response)
    
def parse(response):
    html = response.read()
    soup = BeautifulSoup(html,"html.parser",fromEncoding="gb18030")
    a = soup.find('div',{'class':'all all1'}).find_all('a')
    city = {}
    for i,e in enumerate(a):
        name = e.get_text()
        url = e.get('href') + '/esfsale'
        print url
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
        except:
            print 'server connect failed'
            exit()
        region = itempipline(response)
        city[name] = region
        #if i == 2:
        #    break
    return city
 
def itempipline(response):
    html = response.read()
    soup = BeautifulSoup(html,"html.parser",fromEncoding="gb18030")
    a = soup.find('div',{'class':'list_term'}).find('dd').find_all('a')
    region = []
    for t in  a:
        region.append(t.get_text())
    del region[0]
    return region


try:
    conn=MySQLdb.connect(host="localhost",user="root",passwd="root",db="90zufang",charset="utf8")  
    cursor = conn.cursor()
    url = 'http://hz.sofang.com/city/citysList'
    citys = crawl(url)
    sql = 'insert into city(name,parent) values(%s,0)'
    param = ()
    for city in citys:
        print city
        param += ((city),)
    cursor.executemany(sql,param)
    print '--------------------------------------'
    sql = 'insert into city(name,parent) values(%s,%s)'
    param = ()
    for i,city in enumerate(citys):
        print city
        for region in citys[city]:
            param += ((region,i+1),)
    cursor.executemany(sql,param)
except:
    print 'mysql connect failed'




