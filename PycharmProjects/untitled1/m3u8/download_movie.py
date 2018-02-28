# -*- coding: utf-8 -*-

import requests
import requests.packages.urllib3
import os

def download(dict,path):
    requests.packages.urllib3.disable_warnings()
    #设定文件保存地址
    save_path = os.path.dirname(os.path.abspath(__file__))+ path +os.path.basename(dict['Link'])
    print(os.path.abspath(save_path))

    url = dict['Link']
    #获取文件大小，不取文件，直接获取头
    total_length = int(requests.head(url).headers['Content-Length'])

    #以stream为True方式，暂停下载，与下面的chunk联合使用即可
    response = requests.get(url, stream=True)
    #设定chunk大小，以便监督进度
    kilobytes = 1024
    megabytes = kilobytes * 1000
    chunksize = int(1 * megabytes)
    N = int(total_length / chunksize)

    with open(save_path, 'wb') as f:
        i = 0
        #按chunk大小下载，同时更新进度，与前面的request的stream结合使用
        for chunk in response.iter_content(chunk_size=chunksize):
            if chunk:
                f.write(chunk)
                f.flush()
            i += 1
            print("进度:%s/%s"%(i,N))
    f.close()



def m3u8(dict):
    print(dict)
    data = requests.get(dict['Link'])
    print(data.text)
    # print(data.text)
    data = data.text.splitlines()[-1]
    print(data)
    datam3u8 = requests.get("http://zuikzy.wb699.com"+data)
    print(datam3u8)
    # dict['Link'] = r'http://zuikzy.wb699.com'+data
    # strpath = '/downlaod/m3u8/' #+ dict['Name'] +'/'
    # download(dict,strpath)

def other(dict):
    strpath = '/download/other/'
    print(dict,strpath)
    download(dict,strpath)

