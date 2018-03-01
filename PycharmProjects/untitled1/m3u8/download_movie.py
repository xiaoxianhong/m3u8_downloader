# -*- coding: utf-8 -*-

import requests
import requests.packages.urllib3
import os

def download(dict,path):
    requests.packages.urllib3.disable_warnings()
    #设定文件保存地址
    save_path = os.path.dirname(os.path.abspath(__file__))+ path +os.path.basename(dict['Link'])
    print(os.path.abspath(save_path))
    #获取上载地址
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
    return



def m3u8(dict):
    print(dict)
    data = requests.get(dict['Link'])
    print(data.text)
    # print(data.text)
    data = data.text.splitlines()[-1]
    print(data)
    datam3u8 = requests.get("http://zuikzy.wb699.com"+data)
    ospath = os.path.dirname(os.path.abspath(__file__))+'/downlaod/m3u8/' + dict['Name']
    #筛选内容，生成字典，供下载使用
    m3u8List = []
    for line in str(datam3u8.text).splitlines():
        if '.ts' in line:
            m3u8List.append({'Name':dict['Name'],'Link':"http://zuikzy.wb699.com"+line})
        else:
            continue
    print(m3u8List)

    strpath = '/download/m3u8/' #+ dict['Name'] +'/'
    # 按字典分件下载
    for item in m3u8List:
        download(item,strpath)
    print('下载完成，开始合并')
    #使用shell的cat 1.ts 2.ts > combine.ts语句合并ts
    #os.system
    tmp =[]
    for item in m3u8List:
        tmp.append(os.path.basename(item['Link']))
    # 合并ts文件
    os.chdir(os.path.dirname(__file__)+'/download/m3u8/')
    shell_str = ' '.join(tmp)
    shell_str = 'cat '+ shell_str + '>1' + dict['Name']+'.ddt'
    print(shell_str)
    os.system(shell_str)
    # 删除ts和m3u8文件
    os.system('del /Q *.ts')
    #重命名ddt为ts
    os.renames(dict['Name']+'.ddt',dict['Name']+'.ts')

def other(dict):
    strpath = '/download/other/'
    print(dict,strpath)
    download(dict,strpath)

