# -*- coding: utf-8 -*-

import requests
import progressbar
import requests.packages.urllib3
import os
from  m3u8 import multiThreadDownload

def download(dict,path):
    requests.packages.urllib3.disable_warnings()

    url = dict['Link']

    total_length = int(requests.head(url).headers['Content-Length'])

    # response = requests.request("GET", url, stream=True, data=None, headers=None)
    response = requests.get(url, stream=True)

    save_path = os.path.dirname(os.path.abspath(__file__))+ path +os.path.basename(dict['Link'])
    print(os.path.abspath(save_path))

    # response = requests.get(url)
    # with open(save_path, "wb") as code:
    #     code.write(response.content)

    kilobytes = 1024
    megabytes = kilobytes * 1000
    chunksize = int(1 * megabytes)
    N = int(total_length / chunksize)

    with open(save_path, 'wb') as f:
        i = 0
        for chunk in response.iter_content(chunk_size=chunksize):
            if chunk:
                f.write(chunk)
                f.flush()
            i += 1
            print("进度:%s/%s"%(i,N))
    f.close()


    # with open(save_path, 'wb') as f:
    #     widgets = ['Progress: ', progressbar.Percentage(), ' ',
    #                progressbar.Bar(marker='#', left='[', right=']'),
    #                ' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
    #     pbar = progressbar.ProgressBar(widgets=widgets, maxval=int(total_length/chunksize)).start()
    #     for chunk in response.iter_content(chunk_size=chunksize):
    #         if chunk:
    #             f.write(chunk)
    #             f.flush()
    #         pbar.update(len(chunk) + 1)
    #     pbar.finish()



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
    # print(dict['Link'])
    # multiThreadDownload.main(dict['Link'])
    download(dict,strpath)

