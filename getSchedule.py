# -*- coding: utf-8 -*-
#获取城院学生课程表
import inspect
import urllib2,urllib,time,MySQLdb
from bs4 import BeautifulSoup

class GetKeBiao:
    def __init__(self):
        self.id = ''
        self.pwd = ''
        self.name = ''
        self.cookie_code = ''
        self.mode = True  #False为内网模式
        self.url = 'http://124.160.104.166/'
        print u"正在检查网络状况..."
        try:
            conn=MySQLdb.connect(host="dghyg.gotoip55.com",user="dghyg",passwd="dghyg2013",db="dghyg",charset="utf8")  
            self.cursor = conn.cursor()
        except:
            self.url = 'http://10.61.5.11/'
            try:
                urllib2.urlopen(self.url)
            except:
                print u'无网络访问'
                raw_input('Press enter key to exit')
                exit()
            else:
                print(u'内网模式启动\n................................')
                self.mode = False

    def get_mode(self):
        return self.mode
    
    def login(self,username,password):
        self.id = username
        self.pwd = password
        #获取重定向后真实url
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
           'Referer':'*****'}
        try:
            request = urllib2.Request(self.url,headers=headers)
            response = urllib2.urlopen(request)
        except:
            print u'服务器连接失败'
            raw_input('Press enter key to exit')
            exit()
    	real_url = response.geturl()
    	self.cookie_code = real_url.split('/')[3]
    	#登录数据
    	view_state = 'dDwyODE2NTM0OTg7Oz7UFj95aDg+Sm/3WGJfY6ru0eRH6g=='
    	captcha = '' #验证码
    	role = '学生'
    	post_data = {'__VIEWSTATE':view_state,
    				 'txtUserName':self.id,'TextBox2':self.pwd,
    				 'txtSecretCode':captcha,
    				 'RadioButtonList1':role,
    				 'Button1':'','lbLanguage':'','hidPdrs':'','hidsc':''}
    	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
    			   'Referer':real_url}
    	#开始登录
    	request = urllib2.Request(real_url,urllib.urlencode(post_data),headers)
    	response = urllib2.urlopen(request)

    	#return response.geturl()
    	#登录成功
    	if response.getcode() == 200 and response.geturl() != real_url:
    		if self.mode:
    			try:
    				#获取姓名
    				html = response.read()
    				soup = BeautifulSoup(html,from_encoding="utf-8")
    				self.name = soup.find(id="xhxm").contents[0].replace("'","").replace(u'同学','')
    				n = self.add_user()
    			except Exception:
    				print "服务器出错"
    				raw_input('Press enter key to exit')
    		return True
    	else:
    		return False

    def get_ke(self):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                   'Referer':self.url+self.cookie_code+'/xskbcx.aspx'+'?xh='+self.id}
        url = self.url+self.cookie_code+'/xskbcx.aspx'+'?xh='+self.id+'&xm=&gnmkdm=N121603'

        request = urllib2.Request(url,headers=headers)
        response = urllib2.urlopen(request)
        text = response.read()
        '''
        f = open('./kebiao/'+self.id+'.html','w')
        f.write(text)
        f.close
        '''
        if response.getcode() == 200:
            return text
        else:
            return False

    def add_user(self):
        sql = 'insert into students(username,passwd,name) values(%s,%s,%s)'
        param = (self.id,self.pwd,self.name)
        return self.cursor.execute(sql,param)

    def get_user_from_db(self,idORname):
        print u'查询中...'
        sql = 'select * from students where username=%s or name=%s'
        idORname = unicode(idORname,'gbk').encode('utf-8')
        param = (idORname,idORname)
        self.cursor.execute(sql,param)
        results = self.cursor.fetchall()
        user = []
        for row in results:
            user.append(row[1])
            user.append(row[2])
        return user

class ParseKeBiao:
    def __init__(self,html):
        soup = BeautifulSoup(html,from_encoding="utf-8")
        self.table = soup.find(id='Table1')

    def parse(self):
        for i in range(1,8):
            week = self.week_parse(i)
            print '\n'+week.decode('utf-8')+':\n'
            for j in (1,3,6,8,10):
                tr = self.table.contents[j+2]
                if j in (1,6,10):
                    td = tr.contents[3+i-1]
                else:
                    td = tr.contents[2+i-1]
                if len(td.contents) == 1:
                    continue
                name = td.contents[0].replace("'","")  #去掉字符串中的'
                other = str(td.contents[1]).replace('</br></br></br>','').split('<br>')
                time = other[1].replace(week,'').decode('utf-8')
                teacher = other[2].decode('utf-8')
                position = other[3].decode('utf-8')
                print name
                print time
                print teacher
                print position+'\n'

    def week_parse(self,week):
        str = ''
        if week == 1:
            str = '周一'
        elif week == 2:
            str = '周二'
        elif week == 3:
            str = '周三'
        elif week == 4:
            str = '周四'
        elif week == 5:
            str = '周五'
        elif week == 6:
            str = '周六'
        elif week == 7:
            str = '周日'
        return str

print u'通过本系统可以查看课表\n................................'
print u'正方教务管理系统账号登录\n................................'
print u'登录后不仅可以查看自己课表，还有机会查看到其他人的课表\n................................'
get = GetKeBiao()
chk = True

while chk:
    print u'请输入学号(回车确认):'
    id = raw_input()
    print u'请输入密码(回车确认):'
    pwd = raw_input()
    print u'登录中...'
    chk = not get.login(id,pwd)
    if chk:
        print u'学号或密码错误,请重新登录'
    else:
        print u'登录成功'
print u'我的课表:'
html = get.get_ke()
kebiao = ParseKeBiao(html)
kebiao.parse()

if(get.get_mode()):
    while 1:
        print u'请输入学号或姓名查询课表(回车确认):'
        idORname = raw_input()
        if idORname == 'exit':
            break
        user = get.get_user_from_db(idORname)
        if user == []:
            print u'该同学课表还未加入，赶快邀请TA使用吧'
        else:
            get.login(user[0],user[1])
            html = get.get_ke()
            kebiao = ParseKeBiao(html)
            kebiao.parse()

raw_input('Press enter key to exit')
    





