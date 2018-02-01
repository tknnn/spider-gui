#encoding:utf-8
from Tkinter import *
from ScrolledText import ScrolledText #文本滚动条
import urllib, requests
import re
import threading
import timeit
import sys

url_name = []
a = 1
def get():
    global a
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    url = 'http://www.budejie.com/video/'+str(a)
    var.set('已经获取第%s页的视频' %(a))
    html = requests.get(url,headers=header).text
    url_content = re.compile(r'(<div class="j-r-list-c">.*?</div>.*?</div>)',re.S) # re.S 匹配换行符
    url_contents = re.findall(url_content,html)
    for i in url_contents:
        url_reg = r'data-mp4="(.*?)">'
        url_items = re.findall(url_reg,i)
        if url_items:
            name_reg = re.compile(r'<a href="/detail-.{8}?.html">(.*?)</a>', re.S)
            name_items = re.findall(name_reg,i)
            for i,k in zip(name_items,url_items):
                url_name.append([i,k])
    return url_name

id = 1
def write():
    global id
    while id<10:
        url_name = get()
        for i in url_name:
            urllib.urlretrieve(i[1], filename='/Users/Alex/PycharmProjects/spider-gui/video/%s.mp4' %i[0]) #下载
            text.insert(END, str(id)+'.'+i[1]+'\n'+i[0]+'\n')
            url_name.pop(0) #删除
            id += 1
    var.set('视频链接和视频抓取完毕')

def start():
    th = threading.Thread(target=write)
    th.start()

root = Tk()
root.title('爬虫 GUI')
text = ScrolledText(root, font=('微软雅黑',10))
text.grid() #实现布局
button = Button(root, text='开始爬取', font=('微软雅黑',10), command = start)
button.grid()
var = StringVar() #通过tk方法绑定一个变量
label = Label(root, font=('微软雅黑',10), fg='red', textvariable = var)
label.grid()
label.setvar('熊猫已准备...')
root.mainloop() #创建窗口