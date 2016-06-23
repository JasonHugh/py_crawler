# -*- coding: utf-8 -*-
#豌豆荚爬虫，获取APP对应的类别
__author__ = 'jaysonhu'
import urllib2,urllib,time,MySQLdb,csv,threading
from bs4 import BeautifulSoup

def crawl(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
       'Referer':'http://www.wandoujia.com/apps/',
       'Cookie':'bdshare_firstime=1459930131567; _ga=GA1.2.1736073316.1459930131; Hm_lvt_c680f6745efe87a8fabe78e376c4b5f9=1464490976,1464531053,1464607446,1464757006; Hm_lpvt_c680f6745efe87a8fabe78e376c4b5f9=1464759857'}
    try:
        request = urllib2.Request(url,headers=headers)
        response = urllib2.urlopen(request)
    except:
        print 'server connect failed'
        exit()
    
    return parse(response)
    
def parse(response):
    html = response.read()
    if response.url == 'https://www.wandoujia.com/':
        return 0,0
    soup = BeautifulSoup(html,"html.parser",fromEncoding="gb18030")
    title = soup.find('span',{'class':'title'})
    try:
        cates = soup.find('dd',{'class':'tag-box'}).find_all('a')
    except:
        return title.get_text(),0
    arr = []
    for cate in cates:
        arr.append(cate.get_text())
    return title.get_text(),arr
 
def itempipline(response):
    pass

fp = open('../wandoujia/pack_path.csv','rb')
packs = fp.readlines()
packs = packs[0:20000]
#设置线程数量，分割数据
thread_num = 4
per = len(packs) / thread_num
pack_split = []
for i in range(0,thread_num):
    pack_split.append(packs[per*i:per*(i+1)])

class myThread(threading.Thread):
    def __init__(self,thread_id,packs):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.packs = packs
    def run(self):
        print "Starting " + self.name
        pack_deal(self.thread_id,self.packs)
        print "Exiting " + self.name


def pack_deal(thread_id,packs):
    app_not_found = []
    app_not_cate = []
    app_good = []
    for i,pack in enumerate(packs):
        pack = pack.replace('\n','')
        url = 'http://www.wandoujia.com/apps/' + pack
        title,cates = crawl(url)
        if cates == 0:
            if title == 0:
                app_not_found.append(pack)
            else:
                app_not_cate.append([pack,title])
        else:
            app_good.append([pack,title,cates])
        if (i+1) % 10 == 0:
            print thread_id#len(app_not_found),len(app_not_cate),len(app_good)
    print thread_id,len(app_not_found),len(app_not_cate),len(app_good)
    writer = open('app_not_found.csv','ab+')
    for app in app_not_found:
        writer.write(app+'\n')

#开启线程
threads = []
for i in range(0,thread_num):
    threads.append(myThread(i,pack_split[i]))
    threads[i].start()





