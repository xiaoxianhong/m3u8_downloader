# -*- coding: utf-8 -*-

import os
import requests
import urllib.parse
from bs4 import BeautifulSoup
from m3u8 import download_movie

strUrl = 'http://wap.precn.cn'

def get_m3u8(m3u8):
    print(m3u8)
    DataM3U8 = requests.get(strUrl+m3u8['Link']).text
    DataM3U8_Cut = DataM3U8.split('unescape(')[1]
    DataM3U8_Cut = DataM3U8_Cut.split(')')[0]
    #url解码，对java的escape格式解码，原码为%Uxxxx，先换为\uxxxx，然后转换为bytes，然后解码为escape格式
    DataM3U8_Cut = DataM3U8_Cut.replace('%u','\\u')
    DataM3U8_Cut = urllib.parse.unquote_to_bytes(DataM3U8_Cut).decode('unicode-escape')
    print(DataM3U8_Cut)
    #对于拥有两个以下下载源的，创建下载清单
    downList = []
    i = 0
    downList_str = ''
    downList_source = DataM3U8_Cut.strip('\'').split('#')
    for item in downList_source:
        i += 1
        downList.append(({'NO':str(i),'Name':str(item).split('$')[0],'Link':str(item).split('$')[1],'Format':os.path.splitext(str(item).split('$')[1])[1][1:]}))
        downList_str += ('\n' + str(i) + '.    ' + str(item).split('$')[0] + '     ' + os.path.splitext(str(item).split('$')[1])[1][1:])
    dwmenu = u'''
        ------- 下载格式 ---------
    \033[32;1m
    '''+downList_str+'''\033[0m'''
    #打印菜单
    print(dwmenu)
    user_option = input(">>>>>>:").strip()
    if user_option == '': get_m3u8(m3u8)
    if int(user_option) <= len(downList) :
        # 判断格式，启动不同下载路径
        if downList[int(user_option) - 1]['Format'] == 'm3u8': download_movie.m3u8(downList[int(user_option) - 1])
        else: download_movie.other(downList[int(user_option) - 1])
    else:
        print("\033[31;1m选择不存在!\033[0m")
        get_m3u8(m3u8)


def get_movie_m3u8(gethref):
    # 获取电影详单
    Data = requests.get(gethref['Link']).text
    soupData = BeautifulSoup(Data)
    ulsoupData = soupData.find('ul',attrs={'class':'Drama autoHeight'})
    #列示电影格式选项
    ullist = []
    i = 0
    ulStr =''
    for li in ulsoupData.find_all('li'):
        i += 1
        ullist.append({'NO':str(i),'Name':gethref['Name']+li.span.string,'Link':li.a['href']})
        ulStr += '\n' + str(i) +'.    ' +  gethref['Name']+li.span.string
    # print(ullist)
    #此处应增加一个返回控制，增加一项back，然后调用run
    #run()
    #建立菜单
    ulmenu = u'''
        ------- 电影格式 ---------
    \033[32;1m
    '''+ulStr+'''\033[0m'''
    #打印菜单
    print(ulmenu)
    user_option = input(">>>>>>:").strip()
    # 挑出选的电影
    if user_option == '': get_movie_m3u8(gethref)
    if int(user_option) <= len(ullist) :
        # 爬m3u8出来，并写入文件夹与文件，另开def
        get_m3u8(ullist[int(user_option) - 1])
    else:
        print("\033[31;1m选择不存在!\033[0m")
        get_movie_m3u8(gethref)


def listMovie(list):
    # 列出列表以供选择
    movieStr =''
    for item in list:
        # print(index,item['Name'],item['Link'])
        movieStr += '\n'+item['NO']+'.   '+item['Name']
    # print(movieStr)
    #建立菜单
    menu = u'''
        ------- 最新电影 ---------
    \033[32;1m
    '''+movieStr+'''\033[0m'''
    # 显示菜单
    print(menu)
    user_option = input(">>>>>>:").strip()
    # 挑出选的电影
    if user_option == '': listMovie(list)
    if int(user_option) <= len(list) :
        #爬m3u8出来，并写入文件夹与文件，另开def
        get_movie_m3u8(list[int(user_option)-1])
    else:
        print("\033[31;1m选择不存在!\033[0m")
    return

def movie_list(url):
    #获取数据
    data = requests.get(url)
    #BeautifulSoup格式化
    soup = BeautifulSoup(data.text)
    #查找所有tag为span的文件
    chooseTag = None
    span = soup.find_all('span')
    for child in span:
        if child.string == '最新电影':
            chooseTag = child
            break
    #判断有无值
    if chooseTag == None:
        print('未取到电影列表')
        #退出程序
        os._exit(0)
    #获取到父节点的兄弟节点，并获取所有li
    chooseTag = chooseTag.parent.next_sibling
    #为字典符值
    movie = [{'NO':'1','Name':'搜索电影[暂未开发]','Link':'http://wap.precn.cn/index.php?m=vod-search'}]
    i = 1
    for li in chooseTag.find_all('li'):
        # print(li)
        i += 1
        movie.append({'NO':str(i),'Name':li.find('a',attrs={'class':'txtA'}).string,'Link':strUrl + li.find('a', attrs={'class': 'ImgA'})['href']})
    # print(movie)
    #列出列表，用于选择
    listMovie(movie)
    return

def run():
    #获取网页地址
    str_url = input('请输入网页链接地址')
    #暂时先将地址预设，使用简单输入判断
    if str_url == 'a':
        str_url = strUrl+'/?a=1'
    #此处应有是否为网页判断，暂无
    #列出电影项目以供选择
    movie_list(str_url)

if __name__ == '__main__':
    run()
