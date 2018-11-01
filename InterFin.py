# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 16:51:11 2018

@author: XAYQ-WangChenxi
"""


import pymongo
import urllib.parse
import os



connection = pymongo.MongoClient('172.22.11.11', 27017)
db = connection['article']
#from pymongo import MongoClient
os.chdir('E:\\NLP\\深圳局\\InternetFinace')
news_single = ''
file = open('E:\\NLP\\深圳局\\InternetFinace\\互联网金融.txt', 'r',encoding='utf-8',errors='ignore')
####剔除多余的字符
def replace(x):
    a = '''<section data-tools="135编辑器" data-id="708" data-color="rgb(245, 245, 244)" data-custom="rgb(245, 245, 244)" helvetica="" sans="" border-box="" break-word="" style="word-wrap: break-word; padding: 0px; margin: 0px; font-family: Tahoma, 'Microsoft Yahei', Simsun; line-height: 25.2px; max-width: 100%; color: rgb(62, 62, 62);"><section style="word-wrap: break-word !important; padding: 35px; margin: 0px; max-width: 100%; border-color: rgb(245, 245, 244); color: rgb(123, 123, 111); box-sizing: border-box !important; background-color: rgb(245, 245, 244);"><section style="word-wrap: break-word !important; padding: 0px; margin: 0px auto; max-width: 100%; box-sizing: border-box !important;">'''
    b = '</section></section></section>'
    c = '''<section label="Copyright Reserved by ipaiban.com." donone="shifuMouseDown('shifu_t_013')" helvetica="" sans="" border-box="" break-word="" style="word-wrap: break-word; padding: 10px; margin: 5px 0px 0px; font-family: Tahoma, 'Microsoft Yahei', Simsun; line-height: 25.2px; max-width: 100%; color: rgb(62, 62, 62);"><section style="word-wrap: break-word !important; padding: 0.5em; margin: 0px; max-width: 100%; display: inline-block; font-size: 1em; border-bottom-width: 3px; border-bottom-style: solid; border-color: rgb(0, 122, 170); color: rgb(0, 122, 170); box-sizing: border-box !important;">'''
    d= '</section></section>'
    y1 = x.replace(a,'')
    y2 = y1.replace(b,'')
    y3 = y2.replace(c,'')
    y = y3.replace(d,'')
    return y


i = 0
j = 0
for line in file.readlines():
    if '<DREREFERENCE>' in line:
        i = 1
        continue
    if i ==1:
        url = urllib.parse.unquote(line.strip())
        i =0
        print (url)
    if '<DRETITLE>' in line:
        title = line.split('<DRETITLE>')[1].split('</DRETITLE>')[0]
        print (title)
    if '<DRECONTENT>' in line:
        j=1
        continue
    if j ==1:
        if  '</DRECONTENT>' in line:
            
            db['InterFin'].insert_one({'url':url,
                                          'title':title,
                                          'text':news_single,
                                          'lable':0,
                                          'confirm':0})
            
            j =0 
            news_single = ''
            continue
        else:
            news_single = news_single + '\n' + replace(line.strip())
            print (news_single)
        

