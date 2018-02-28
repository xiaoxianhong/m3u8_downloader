# -*- coding: utf-8 -*-

import os
import sys


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(base_dir)
sys.path.append(base_dir)

from Movie_Web_Wechat import WeiDuYinDan_Scrapy

def origin():
#创建可爬网站菜单
    menu = u'''
    ------- 爬取网站清单 ---------
    \033[32;1m1.  未读影单
    2.  退出
    \033[0m'''
    print(menu)
    user_option = input('>>>>>>:').strip()
    if user_option == '': origin()
    if user_option == '1': WeiDuYinDan_Scrapy.run()
    if user_option == '2': os._exit(0)
    if user_option not in ['1','2'] :origin()

origin()


