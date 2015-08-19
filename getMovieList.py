# -*- coding: utf-8 -*-    
#获取一夫天下电影列表
import urllib2,urllib,re,time,thread

class Spider_iftx:
    def __init__(self):
        self.page = 1
        self.pages = []
        self.enable = False

    def getPage(self,page):
        url = "http://10.61.2.222/video_list.asp?action=desc&page="+str(page)
        user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0";
        headers = {'User_Agent':user_agent}
        req = urllib2.Request(url,headers = headers)
        res = urllib2.urlopen(req).read()
        res = res.decode("gbk")
        #return res
        contents = re.findall('<td width="70%">.*?<a.*?href=\'(.*?)\'>.*?<b>.*?<font.*?color="#0066CC">(.*?)</font>.*?</b>.*?</A>.*?</td>.*?</tr>.*?<tr>.*?<td>.*?<img src=\'.*?\' border=0 align=absmiddle>&nbsp;&nbsp;<br>(.*?)</td>.*?</tr>',res,re.S)
        items = []
        for item in contents:
            items.append([item[1].replace('\n',''),item[2].replace('\n','').replace(' ',''),item[0].replace('\n','')])
        return items
        
    def loadPage(self):
        while(self.enable):
            if len(self.pages)<2 :
                try:
                    items = self.getPage(self.page)
                    self.page += 1
                    self.pages.append(items)
                except:
                    print u'服务器链接出错'
                time.sleep(5)
            else:
                time.sleep(2)

    def showPage(self,now_page,page):
        i = 0
        for items in now_page:
            print u'第' + str(page) + u'页'+items[0]+u'\n电影:'+items[1]+u'\n链接:'+' http://10.61.2.222/'+items[2]+'\n'
            i += 1
            if i % 5 == 0 :
                if raw_input() == 'quit':
                    self.enable = False
                    break

    def start(self):
        self.enable = True
        page = self.page

        thread.start_new_thread(self.loadPage,())

        while self.enable:
            if self.pages:
                now_page = self.pages[0]
                del self.pages[0]
                self.showPage(now_page,page)
                page+=1

print u'电影查询系统'
spider = Spider_iftx()
spider.start()

