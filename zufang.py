# -*- coding: utf-8 -*-
#19楼租房爬虫
__author__ = 'jaysonhu'
import inspect
import urllib2,urllib,time,MySQLdb
from bs4 import BeautifulSoup

def crawl(url,filename):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
       'Referer':'http://www.19lou.com',
       'Cookie':"bdshare_firstime=1460716669548; checkin__43226029_0520=1_4_6; _Z3nY0d4C_=37XgPK9h-%3D1366-1366-1366-389; checkin__43226029_0521=2_6_8; f8big=r9; _DM_S_=8e43d484d631171931c079d116abbf55; fr_adv_last=bbs_list_essence; fr_adv=; JSESSIONID=45D1F9ACE0B84369445080A7892F6BB8; _dm_tagnames=%5B%7B%22k%22%3A%22%E5%92%8C%E7%9D%A6%E6%96%B0%E6%9D%91%22%2C%22c%22%3A14%7D%2C%7B%22k%22%3A%22%E6%9D%AD%E5%B7%9E%E7%A7%9F%E6%88%BF%E7%BD%91%22%2C%22c%22%3A11%7D%2C%7B%22k%22%3A%22%E9%93%B6%E6%A0%91%E6%B9%BE%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E5%B0%8F%E6%B2%B3%22%2C%22c%22%3A2%7D%2C%7B%22k%22%3A%22%E6%88%91%E8%A6%81%E5%90%88%E7%A7%9F%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E5%B0%8F%E6%B2%B3%E4%BD%B3%E8%8B%91%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E4%B8%89%E5%AE%9D%E9%83%A1%E5%BA%AD%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E6%B5%81%E6%B0%B4%E8%8B%91%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E6%A0%A1%E5%9B%AD%E6%8B%9B%E8%81%98%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%2219%E6%A5%BC%E5%85%AC%E5%8F%B8%E6%8B%9B%E8%81%98%22%2C%22c%22%3A1%7D%5D; _dm_userinfo=%7B%22uid%22%3A%2243226029%22%2C%22category%22%3A%22%E6%88%BF%E4%BA%A7%22%2C%22sex%22%3A%222%22%2C%22frontdomain%22%3A%22www.19lou.com%22%2C%22stage%22%3A%22%22%2C%22ext%22%3A%22%22%2C%22ip%22%3A%2239.182.37.130%22%2C%22city%22%3A%22%E6%B5%99%E6%B1%9F%22%7D; _DM_SID_=046e086262a31ad195d3a872b8548f3e; screen=1903; pm_count=%7B%22pc_hangzhou_cityEnterMouth_advmodel_adv_210x200_2%22%3A2%2C%22pc_hangzhou_cityEnterMouth_advmodel_adv_210x200_1%22%3A2%2C%22pc_hangzhou_cityEnterMouth_advmodel_adv_210x200_4%22%3A2%2C%22pc_hangzhou_cityEnterMouth_advmodel_adv_210x200_3%22%3A2%2C%22pc_hangzhou_cityEnterMouth_advmodel_adv_210x200_6%22%3A2%2C%22pc_hangzhou_cityEnterMouth_advmodel_adv_210x401_1%22%3A2%2C%22pc_hangzhou_cityEnterMouth_advmodel_adv_210x200_7%22%3A2%2C%22pc_hangzhou_cityEnterMouth_advmodel_adv_330x401_3%22%3A2%2C%22pc_hangzhou_cityEnterMouth_advmodel_adv_330x200_1%22%3A2%2C%22pc_hangzhou_cityEnterMouth_advmodel_adv_330x401_1%22%3A2%2C%22pc_hangzhou_cityEnterMouth_advmodel_adv_330x401_2%22%3A2%2C%22pc_hangzhou_forumthread_button_adv_180x180_5%22%3A141%2C%22pc_hangzhou_forumthread_button_adv_180x180_4%22%3A141%2C%22pc_hangzhou_forumthread_button_adv_180x180_3%22%3A141%2C%22pc_hangzhou_forumthread_button_adv_180x180_2%22%3A141%2C%22pc_hangzhou_forumthread_button_adv_180x180_1%22%3A141%7D; dayCount=%5B%7B%22id%22%3A8153%2C%22count%22%3A33%7D%2C%7B%22id%22%3A7119%2C%22count%22%3A33%7D%2C%7B%22id%22%3A8034%2C%22count%22%3A13%7D%2C%7B%22id%22%3A8350%2C%22count%22%3A12%7D%2C%7B%22id%22%3A8354%2C%22count%22%3A6%7D%2C%7B%22id%22%3A8074%2C%22count%22%3A1%7D%2C%7B%22id%22%3A5893%2C%22count%22%3A1%7D%2C%7B%22id%22%3A7959%2C%22count%22%3A1%7D%2C%7B%22id%22%3A4828%2C%22count%22%3A1%7D%2C%7B%22id%22%3A7689%2C%22count%22%3A1%7D%2C%7B%22id%22%3A8338%2C%22count%22%3A1%7D%2C%7B%22id%22%3A8203%2C%22count%22%3A1%7D%2C%7B%22id%22%3A7724%2C%22count%22%3A1%7D%2C%7B%22id%22%3A8097%2C%22count%22%3A1%7D%2C%7B%22id%22%3A8748%2C%22count%22%3A1%7D%2C%7B%22id%22%3A6718%2C%22count%22%3A1%7D%5D; Hm_lvt_5185a335802fb72073721d2bb161cd94=1463313839,1463734304,1463792751,1463801434; Hm_lpvt_5185a335802fb72073721d2bb161cd94=1463819646"}
    try:
        request = urllib2.Request(url,headers=headers)
        response = urllib2.urlopen(request)
    except:
        print 'server connect failed'
        raw_input('Press enter key to exit')
        exit()
    html = response.read()
    soup = BeautifulSoup(html,"html.parser",fromEncoding="gb18030")
    #写入html文件
    write = file('./html/' + str(filename) + '.html','wb+')
    content = u'<!doctype html><html><head><meta charset="UTF-8"/><title>租房</title><script src="http://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script></head><body>'
    num = 0
    #获取子页面
    for child in soup.table.find_all('a'):
        url = child.get('href')
        title = child.get_text().replace('\r','').replace('\n','').replace('  ','')
        try:
            request = urllib2.Request(url,headers=headers)
            response = urllib2.urlopen(request)
        except:
            print 'server conect failed'
            raw_input('Press enter key to exit')
            exit()

        html = response.read()
        soup = BeautifulSoup(html,"html.parser",fromEncoding="gb18030")
        ul = soup.find('ul',{'id':'slide-data'})
        #num += 1
        #content += '<h3><a href='+url+'>'+str(num)+'/'+title+'</a></h3>'
        #筛选出有图片的
        if ul != None:
            #提取信息
            tr = soup.find('table',{'class':'view-table link0'}).find_all('tr')
            hx = tr[2].td.get_text().replace('\r','').replace('\n','').replace('  ','')
            xq = tr[4].td.get_text().replace('\r','').replace('\n','').replace('  ','')
            mj = tr[5].td.get_text().replace('\r','').replace('\n','').replace('  ','')
            money = tr[13].td.get_text().replace('\r','').replace('\n','').replace('  ','')
            #写入标题
            num += 1
            content += '<h3><a href='+url+'>'+str(num)+'/'+title+'</a></h3>'+hx+xq+mj+money+'<br/>'
            for row in ul.find_all('li'):
                image = row.find('a',{'class':'J_login nail'}).img.get('src')
                image_big = row.find('p').img.get('src')
                #print image_big
                content += '<img data-big="'+image_big+'" src="'+image+'" style="margin-right:10px"/>'
        #exit()

    write.write(content.encode('utf-8')+'<img id="big" style="position:fixed;top:0;right:0;z-index:999;display:none" src=""/><script>$("img[id!=big]").mouseover(function(){$("#big").attr("src",$(this).attr("data-big"));$("#big").show(500)});$("img[id!=big]").mouseout(function(){$("#big").hide(500)})</script>')
    
for i in range(1,11):
    url = 'http://www.19lou.com/thread/category/structure/search/result?mf_1831_1=4&mf_1831_2=3&mf_55=2&mf_55_field=18&mf_low_65=2001&mf_high_65=2500&mf_68=0&mf_62=0&mf_Q=%E5%92%8C%E7%9D%A6%E6%96%B0%E6%9D%91&fid=1637&m=10001&page='+str(i)
    filename = i
    crawl(url,filename)
    print i




