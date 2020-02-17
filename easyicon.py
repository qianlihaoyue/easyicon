#简介
#https://www.easyicon.net/ 爬虫
#流程：检测剪切板变化-》如果变化-》检测是否为url-》为url-》提取ico链接及名字-》下载-》使用PythonMagick转为ico（可省略）
#使用方法：运行-》复制图片链接即可-》python会在本文件夹自动创建ico文件夹，并下载


##################################################################################
def is_url(url):  #检测链接是否为url
    import re
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$',
        re.IGNORECASE)
    if re.match(regex, url) != None:
        return 1
    else:
        return 0


def pngtoico(filename):  #png转ico
    from PythonMagick import Image  # https://www.lfd.uci.edu/~gohlke/pythonlibs/#pythonmagick
    img = Image(filename)
    # 这里要设置一下尺寸，不然会报ico尺寸异常错误
    img.sample('128x128')
    img.write(filename.split('.')[0] + '.ico')


#####################################爬虫部分#############################################

import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}


def urltoname(link):  #从链接网址中提取name
    temp = (link.split('/')[-1:])[0]
    # print(temp, type(temp))
    temp2 = (temp.split('-')[-1:])[0]
    temp = temp2.split('.')[0]
    # print(temp, type(temp))
    name = 'ico/' + temp + '.png'
    print(name)
    return name


def get_imgurl(link):  #从链接网址中提取图片地址
    global i
    links = requests.get(link, headers=headers)
    soup = BeautifulSoup(links.text, 'html.parser')
    img_url = (soup.find_all('div', class_='icon_img_one')[0])
    for i in img_url:
        url = "https://www.easyicon.net/" + str(i.find('img')['src'])
        print(url)
        return url


def download(url, filename):  #下载单个图片
    response = requests.get(url, headers=headers)
    img = response.content
    with open(filename, 'wb') as f:
        f.write(img)


#################################主程序#################################################

import pyperclip
import time
import os

def main():
    if not os.path.exists('ico'):  #如果不存在ico文件夹，创建
        os.mkdir('ico')

    #检测剪切板变化
    last_string = pyperclip.paste()
    while True:
        time.sleep(0.2)  # 检测频率
        string = pyperclip.paste()  #获取字符串
        if string != last_string and string != '':  #如果两次不同
            last_string = string  #更新
            if is_url(string):  #检测是否为url
                img_url = get_imgurl(string)  #从链接网址中提取url
                img_name = urltoname(string)  #从链接网址中提取name
                download(img_url, img_name)  #爬虫下载
                pngtoico(img_name)  #转为ico

main()                                                        ######使用UI版需要注释该行代码
##################################################################################
