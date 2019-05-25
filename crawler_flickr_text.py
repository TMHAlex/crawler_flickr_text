#%%
import requests
import numpy as np  
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import re #抓圖片
from urllib.request import urlretrieve #存照片
import os #為了建立資料夾
import sys #控制抓取文章頁數 system的縮寫
import threading
import time
import csv

with open('train_img.txt','r') as fp:
    img = fp.read().splitlines()

information = open("image_information.txt", "a")

outNum = 0

def func(url,i):
    global outNum
    lock.acquire()
    time.sleep(0.01)

    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text,"html.parser")
        view = soup.find_all(class_ = 'view-count-label')
        view = view[0].get_text()
        view = re.sub('\s',"",view)
        view = view.replace(',','')
        favorite = soup.find_all(class_ = 'fave-count-label')
        favorite = favorite[0].get_text()
        favorite = re.sub('\s',"",favorite)
        favorite = favorite.replace(',','')
        message = soup.find_all(class_ = 'comment-count-label')
        message = message[0].get_text()
        message = re.sub('\s',"",message)
        message = message.replace(',','')
        name = url.split('/')[-1]

        information.writelines(str(name)+","+str(view)+","+str(favorite)+","+str(message)+"\n")
        
        outNum = outNum +1
        print("Successful process {} urls ".format(outNum))
        
    except Exception as e:
        print("Fail process {} urls ".format(i+1))
        print(url)
        print(e)
    lock.release()

threads = []

lock = threading.BoundedSemaphore(10)
for i in range(298512, len(img)):
    # print("process {} urls ".format(i+1))
    # errf.writelines(str(i)+'\n')
    url = img[i]    
    t = threading.Thread(target=func,args=(url, i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Finish")

#%%