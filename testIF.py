# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 09:26:02 2018

@author: XAYQ-WangChenxi
"""

#########测试==========

#####放在11.41库
import pymongo
#import pandas as pd
#import numpy as np
import jieba
import os
import SimHash as sh

os.chdir('/home/nlp/model')
#os.chdir('E:\\NLP\\深圳局\\InternetFinace')

####加载停用词表
jieba.analyse.set_stop_words('/home/nlp/stopwords/stopwords.txt')
#jieba.analyse.set_stop_words('F:\\pythonfoot\\nlp\\stopwords.txt')

connection = pymongo.MongoClient('172.22.11.11', 27017)
db = connection['article']
#a = db.datapos.find(({"lable":1}))
i = 0
#####策略2 svm分类
from sklearn.externals import joblib
clf = joblib.load("model.m")
vec = joblib.load("vec.m")
transformer = joblib.load("tfidf.m")
ch2 = joblib.load("ch2.m")        
j = 0    
####设置哈希值储存表
haxi = []
###存储标题

haxiT = []
####设置距离表
dis1 = []
disT1 = []
####循环获取文本
for u in db.data2018.find(no_cursor_timeout=True):#.skip(3000): ####超时处理 从第3000篇开始
    i +=1
    print (i)
    if ('guba' in u['url']) or ('直播答题' in u['text']):
            continue
    else:        
        print (u['text'])
        
        ####获取文本
        text = u['text']
        ###获取标题
        title = u['title']
        ####分词
        word_cut = jieba.lcut(text.strip(), cut_all = False)
        ####换空格
        news1 = []
        news1.append(' '.join(word_cut))
        
        ####建立测试集的vsm矩阵         
        x_test11 = vec.transform(news1)
        print ('测试集稀疏矩阵维度:' + repr(x_test11.shape))
        ###查看vsm模型矩阵
        x_test21 = transformer.transform(x_test11)
        #print (x_test1.toarray())                  
        ####卡方化
        X_test1 = ch2.transform(x_test21)
        print ('测试卡方矩阵维度:' + repr(X_test1.shape))
        print ('将测试集转化为卡方矩阵')
        #在测试集上测试最优的模型的泛化能力.   
        y1 = clf.predict(X_test1)  
        #y1[0] == 1
        if y1[0] == 1:
            #####转换成哈希
            SimHashNum = sh.simhash(text)
            SimHashNumT = sh.string_hash(title)
            ####储存哈希值
            if len(haxi) == 0:
                print (1)
                ####存哈希值
                haxi.append(SimHashNum)
                haxiT.append(SimHashNumT)
                j+=1
                ####插入表
                db['InterFinTest2'].insert_one({'url':u['url'],
                                                'title':u['title'],
                                                'text':text,
                                                 'correct':0,
                                                 'confirm':0})
            else:
                for HaxiNum in haxi:
                    ###计算哈希距离
                    dis = sh.hammingDis(SimHashNum,HaxiNum)
                    ####存储距离值
                    dis1.append(dis)
                for HaxiNumT in haxiT:
                    disT = sh.hammingDis(SimHashNumT,HaxiNumT)
                    disT1.append(disT)
                ####海明距离在10以内    
                if 0 in dis1 or 1 in dis1 or 2 in dis1 or 3 in dis1 or 4 in dis1 or 5 in dis1 or 6 in dis1 or 7 in dis1 or 8 in dis1 or  9 in dis1 or 10 in dis1 or\
                0 in disT1 or 1 in disT1 or 2 in disT1 or 3 in disT1 or 4 in disT1 or 5 in disT1 or 6 in disT1 or 7 in disT1 or 8 in disT1 or  9 in disT1 or 10 in disT1:
                    print (3)
                    dis1 = []
                    disT1 = []
                else:
                    print (2)
                    dis1 = []
                    disT1 = []
                    haxi.append(SimHashNum) ####储存哈希值
                    haxiT.append(SimHashNumT)
                    j+=1
                    ####插入表
                    db['InterFinTest2'].insert_one({'url':u['url'],
                                                    'title':u['title'],
                                                    'text':text,
                                                     'correct':0,
                                                     'confirm':0})
    print (j)
    if i >251374:
        break
    
