# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 16:36:20 2018

@author: XAYQ-WangChenxi
"""

from __future__ import unicode_literals

#from flask_restful import reqparse,Api, Resource
from flask_restful import Api
from flask import Flask,request

#from flask import abort
#from flask import make_response,Response  
import json
#import time
import re
#####放在11.41库
import jieba
import os
import jieba.analyse
import configparser


test_content = '我是测试文章'
jieba.lcut(test_content.strip(), cut_all = False)

def abspath(filename):
    basedir = '/home/nlp/model'
#    basedir = 'E:/NLP/深圳局/NegInf'
    return os.path.join(basedir, filename)

print ('IFFile is loading ......')
from sklearn.externals import joblib
IFclf = joblib.load(abspath("IF/model.m"))
IFvec = joblib.load(abspath("IF/vec.m"))
IFtransformer = joblib.load(abspath("IF/tfidf.m"))
IFch2 = joblib.load(abspath("IF/ch2.m"))
print ('IFFile loading successful')

adclf = joblib.load(abspath("admin/model.m"))
advec = joblib.load(abspath("admin/vec.m"))
adtransformer = joblib.load(abspath("admin/tfidf.m"))
adch2 = joblib.load(abspath("admin/ch2.m"))
print ('admin File loading successful')

asclf = joblib.load(abspath("assure/model.m"))
asvec = joblib.load(abspath("assure/vec.m"))
astransformer = joblib.load(abspath("assure/tfidf.m"))
asch2 = joblib.load(abspath("assure/ch2.m"))
print ('assure File loading successful')

creclf = joblib.load(abspath("credit/model.m"))
crevec = joblib.load(abspath("credit/vec.m"))
cretransformer = joblib.load(abspath("credit/tfidf.m"))
crech2 = joblib.load(abspath("credit/ch2.m"))
print ('credit File loading successful')

finclf = joblib.load(abspath("finance/model.m"))
finvec = joblib.load(abspath("finance/vec.m"))
fintransformer = joblib.load(abspath("finance/tfidf.m"))
finch2 = joblib.load(abspath("finance/ch2.m"))
print ('finance File loading successful')

manclf = joblib.load(abspath("manage/model.m"))
manvec = joblib.load(abspath("manage/vec.m"))
mantransformer = joblib.load(abspath("manage/tfidf.m"))
manch2 = joblib.load(abspath("manage/ch2.m"))
print ('manage File loading successful')

marclf = joblib.load(abspath("market/model.m"))
marvec = joblib.load(abspath("market/vec.m"))
martransformer = joblib.load(abspath("market/tfidf.m"))
march2 = joblib.load(abspath("market/ch2.m"))
print ('market File loading successful')

proclf = joblib.load(abspath("product/model.m"))
provec = joblib.load(abspath("product/vec.m"))
protransformer = joblib.load(abspath("product/tfidf.m"))
proch2 = joblib.load(abspath("product/ch2.m"))
print ('product File loading successful')

projclf = joblib.load(abspath("project/model.m"))
projvec = joblib.load(abspath("project/vec.m"))
projtransformer = joblib.load(abspath("project/tfidf.m"))
projch2 = joblib.load(abspath("project/ch2.m"))
print ('project File loading successful')

regclf = joblib.load(abspath("regulate/model.m"))
regvec = joblib.load(abspath("regulate/vec.m"))
regtransformer = joblib.load(abspath("regulate/tfidf.m"))
regch2 = joblib.load(abspath("regulate/ch2.m"))
print ('regulate File loading successful')

unfclf = joblib.load(abspath("unforce/model.m"))
unfvec = joblib.load(abspath("unforce/vec.m"))
unftransformer = joblib.load(abspath("unforce/tfidf.m"))
unfch2 = joblib.load(abspath("unforce/ch2.m"))
print ('unforce File loading successful')

othclf = joblib.load(abspath("other/model.m"))
othvec = joblib.load(abspath("other/vec.m"))
othtransformer = joblib.load(abspath("other/tfidf.m"))
othch2 = joblib.load(abspath("other/ch2.m"))
print ('other File loading successful')

pnclf = joblib.load(abspath("posneg/model.m"))
pnvec = joblib.load(abspath("posneg/vec.m"))
pntransformer = joblib.load(abspath("posneg/tfidf.m"))
pnch2 = joblib.load(abspath("posneg/ch2.m"))
print ('posorneg File loading successful')

pn1clf = joblib.load(abspath("posneg1/model.m"))
pn1vec = joblib.load(abspath("posneg1/vec.m"))
pn1transformer = joblib.load(abspath("posneg1/tfidf.m"))
pn1ch2 = joblib.load(abspath("posneg1/ch2.m"))
print ('posorneg1 File loading successful')

oneclf = joblib.load(abspath("onesvm/model.m"))
onevec = joblib.load(abspath("onesvm/vec.m"))
onetransformer = joblib.load(abspath("onesvm/tfidf.m"))
print ('onesvm File loading successful')

##加载负面词典

with open(abspath("neg_word/neg1.txt"),"r",encoding = 'utf-8') as neg1_txt:
    neg1 = neg1_txt.read().encode('utf-8').decode('utf-8-sig')
    neg1 = neg1.replace(',','|')
with open(abspath("neg_word/neg2.txt"),"r",encoding = 'utf-8') as neg2_txt:
    neg2 = neg2_txt.read().encode('utf-8').decode('utf-8-sig')
    neg2 = neg2.replace(',','|')
with open(abspath("neg_word/unneg.txt"),"r",encoding = 'utf-8') as unneg_txt:
    unneg = unneg_txt.read().encode('utf-8').decode('utf-8-sig')
    unneg = unneg.replace(',','|') 
with open(abspath("neg_word/org.txt"),"r",encoding = 'utf-8') as org_txt:
    org = org_txt.read().encode('utf-8').decode('utf-8-sig')
    org = org.split(',')
print ('neg dict loading successful')        

#### 加载现有有关文本分类的配置文件
conf = configparser.ConfigParser()
conf.read(abspath('config/keyword.ini'),encoding = 'utf-8')

print ('IFkeyword is loading ......')
IF_keywords = re.compile(conf.get('config', 'IF_keywords'))
IF_not_keywords = re.compile(conf.get('config', 'IF_not_keywords'))
print ('IFkeyword loading successful')

ad_keywords = re.compile(conf.get('config','ad_keywords'))
not_ad_keywords = re.compile(conf.get('config','not_ad_keywords'))
ad1_keywords = re.compile(conf.get('config','ad1_keywords'))
not_ad1_keywords = re.compile(conf.get('config','not_ad1_keywords'))
ad2_keywords = re.compile(conf.get('config','ad2_keywords'))
not_ad2_keywords = re.compile(conf.get('config','not_ad2_keywords'))
ad3_keywords = re.compile(conf.get('config','ad3_keywords'))
not_ad3_keywords = re.compile(conf.get('config','not_ad3_keywords'))
ad4_keywords = re.compile(conf.get('config','ad4_keywords'))
not_ad4_keywords = re.compile(conf.get('config','not_ad4_keywords'))
ad5_keywords = re.compile(conf.get('config','ad5_keywords'))
not_ad5_keywords = re.compile(conf.get('config','not_ad5_keywords'))
print ('ad_keywords loading successful')

ass_keywords = re.compile(conf.get('config','ass_keywords'))
not_ass_keywords = re.compile(conf.get('config','not_ass_keywords'))
ass1_keywords = re.compile(conf.get('config','ass1_keywords'))
not_ass1_keywords = re.compile(conf.get('config','not_ass1_keywords'))
ass2_keywords = re.compile(conf.get('config','ass2_keywords'))
print ('assure_keywords loading successful')

credit_keywords = re.compile(conf.get('config','credit_keywords'))
not_credit_keywords = re.compile(conf.get('config','not_credit_keywords'))
cre1_keywords = re.compile(conf.get('config','cre1_keywords'))
not_cre1_keywords = re.compile(conf.get('config','not_cre1_keywords'))
cre2_keywords = re.compile(conf.get('config','cre2_keywords'))
not_cre2_keywords = re.compile(conf.get('config','not_cre2_keywords'))
cre3_keywords = re.compile(conf.get('config','cre3_keywords'))
not_cre3_keywords = re.compile(conf.get('config','not_cre3_keywords'))
cre4_keywords = re.compile(conf.get('config','cre4_keywords'))
not_cre4_keywords = re.compile(conf.get('config','not_cre4_keywords'))
cre5_keywords = re.compile(conf.get('config','cre5_keywords'))
not_cre5_keywords = re.compile(conf.get('config','not_cre5_keywords'))
cre6_keywords = re.compile(conf.get('config','cre6_keywords'))
not_cre6_keywords = re.compile(conf.get('config','not_cre6_keywords'))
print ('credit_keywords loading successful')

fin_keywords = re.compile(conf.get('config','fin_keywords'))
not_fin_keywords = re.compile(conf.get('config','not_fin_keywords'))
not_fin_keywords1 = re.compile(conf.get('config','not_fin_keywords1'))
not_fin_keywords2 = re.compile(conf.get('config','not_fin_keywords2'))
fin1_keywords = re.compile(conf.get('config','fin1_keywords'))
not_fin1_keywords = re.compile(conf.get('config','not_fin1_keywords'))
fin2_keywords = re.compile(conf.get('config','fin2_keywords'))
not_fin2_keywords = re.compile(conf.get('config','not_fin2_keywords'))
fin3_keywords = re.compile(conf.get('config','fin3_keywords'))
not_fin3_keywords = re.compile(conf.get('config','not_fin3_keywords'))
fin4_keywords = re.compile(conf.get('config','fin4_keywords'))
not_fin4_keywords = re.compile(conf.get('config','not_fin4_keywords'))
fin5_keywords = re.compile(conf.get('config','fin5_keywords'))
not_fin5_keywords = re.compile(conf.get('config','not_fin5_keywords'))
print ('finance_keywords loading successful')

manage_keywords = re.compile(conf.get('config','manage_keywords'))
not_man_keywords = re.compile(conf.get('config','not_man_keywords'))
man1_keywords = re.compile(conf.get('config','man1_keywords'))
not_man1_keywords = re.compile(conf.get('config','not_man1_keywords'))
man2_keywords = re.compile(conf.get('config','man2_keywords'))
not_man2_keywords = re.compile(conf.get('config','not_man2_keywords'))
man3_keywords = re.compile(conf.get('config','man3_keywords'))
not_man3_keywords = re.compile(conf.get('config','not_man3_keywords'))
man4_keywords = re.compile(conf.get('config','man4_keywords'))
man5_keywords = re.compile(conf.get('config','man5_keywords'))
not_man5_keywords = re.compile(conf.get('config','not_man5_keywords'))
man6_keywords = re.compile(conf.get('config','man6_keywords'))
man7_keywords = re.compile(conf.get('config','man7_keywords'))
not_man7_keywords = re.compile(conf.get('config','not_man7_keywords'))
man8_keywords = re.compile(conf.get('config','man8_keywords'))
not_man8_keywords = re.compile(conf.get('config','not_man8_keywords'))
man9_keywords = re.compile(conf.get('config','man9_keywords'))
man10_keywords = re.compile(conf.get('config','man10_keywords'))
not_man10_keywords = re.compile(conf.get('config','not_man10_keywords'))
man11_keywords = re.compile(conf.get('config','man11_keywords'))
man12_keywords = re.compile(conf.get('config','man12_keywords'))
man13_keywords = re.compile(conf.get('config','man13_keywords'))
not_man13_keywords = re.compile(conf.get('config','not_man13_keywords'))
man14_keywords = re.compile(conf.get('config','man14_keywords'))
man15_keywords = re.compile(conf.get('config','man15_keywords'))
print ('manage_keywords loading successful')


mar_keywords = re.compile(conf.get('config','mar_keywords'))
not_mar_keywords = re.compile(conf.get('config','not_mar_keywords'))
mar1_keywords = re.compile(conf.get('config','mar1_keywords'))
not_mar1_keywords = re.compile(conf.get('config','not_mar1_keywords'))
mar2_keywords = re.compile(conf.get('config','mar2_keywords'))
not_mar2_keywords = re.compile(conf.get('config','not_mar2_keywords'))
mar3_keywords = re.compile(conf.get('config','mar3_keywords'))
not_mar3_keywords = re.compile(conf.get('config','not_mar3_keywords'))
mar4_keywords = re.compile(conf.get('config','mar4_keywords'))
not_mar4_keywords = re.compile(conf.get('config','not_mar4_keywords'))
mar5_keywords = re.compile(conf.get('config','mar5_keywords'))
not_mar5_keywords = re.compile(conf.get('config','not_mar5_keywords'))
print ('market_keywords loading successful')

pro_keywords = re.compile(conf.get('config','pro_keywords'))
not_pro_keywords = re.compile(conf.get('config','not_pro_keywords'))
pro1_keywords = re.compile(conf.get('config','pro1_keywords'))
pro2_keywords = re.compile(conf.get('config','pro2_keywords'))
print ('product_keywords loading sucessful')

proj_keywords = re.compile(conf.get('config','proj_keywords'))
not_proj_keywords = re.compile(conf.get('config','not_proj_keywords'))
proj1_keywords = re.compile(conf.get('config','proj1_keywords'))
not_proj1_keywords = re.compile(conf.get('config','not_proj1_keywords'))
proj2_keywords = re.compile(conf.get('config','proj2_keywords'))
proj3_keywords = re.compile(conf.get('config','proj3_keywords'))
print ('project_keywords loading sucessful')

reg_keywords = re.compile(conf.get('config','reg_keywords'))
not_reg_keywords = re.compile(conf.get('config','not_reg_keywords'))
reg1_keywords = re.compile(conf.get('config','reg1_keywords'))
not_reg_keywords1 = re.compile(conf.get('config','not_reg1_keywords'))
reg2_keywords = re.compile(conf.get('config','reg2_keywords'))
reg3_keywords = re.compile(conf.get('config','reg3_keywords'))
reg4_keywords = re.compile(conf.get('config','reg4_keywords'))
reg5_keywords = re.compile(conf.get('config','reg5_keywords'))
not_reg5_keywords = re.compile(conf.get('config','not_reg5_keywords'))
print ('regulate_keywords loading successful')

unf_keywords = re.compile(conf.get('config','unf_keywords'))
not_unf_keywords = re.compile(conf.get('config','not_unf_keywords'))
print ('unforce_keywords loading successful')

oth_keywords = re.compile(conf.get('config','oth_keywords'))
print ('other_keywords loading successful')

#####不参与分类文章的关键词
title_keywords = re.compile(conf.get('config','title_keywords'))
con_keywords = re.compile(conf.get('config','con_keywords'))
url_keywords = re.compile(conf.get('config','url_keywords'))


####提取二级市场专项关键词
market_TK = re.compile(conf.get('config','market_TK'))
#####提取公告关键词
announcement_TK = re.compile(conf.get('config','announcement_TK'))
not_announcement_TK = re.compile(conf.get('config','not_announcement_TK'))
####提取研报关键词
research_report_TK = re.compile(conf.get('config','research_report_TK'))
not_research_report_TK = re.compile(conf.get('config','not_research_report_TK'))

app = Flask(__name__)
app.debug = True
app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
api = Api(app)

@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/SVM_TextSort/', methods=['POST'])
def add_task():
    #time_start=time.time()
    
    #url = request.form.get('siteDomain')
    #entitylist = request.form.get('entityList')
    #entitylist = request.form.getlist('entityList')
    #text = request.form.get('content')
    #title = request.form.get('title')

    url = request.json['siteDomain']    
    entitylist = request.json['entityList']
    text = request.json['content']
    title = request.json['title']
    content = title + text
    #print (content)
    '''
    ###########情感判断=====
    neg1_entity_list = []
    neg1_word_list = []
    neg2_entity_list = []
    neg2_word_list = []
    if entitylist and title and text:
        for entity in entitylist:
            try:
                float(entity)
                continue
            except:
                if entity in title and entity not in org:
                    unneg_word = re.search(unneg,title)
                    if not unneg_word:
                        neg1_word = re.findall(neg1,title)
                        neg2_word = re.findall(neg2,title)
                        if neg1_word:
                            neg1_entity_list.append(entity)
                            neg1_word_list.extend(neg1_word)
                        if neg2_word:
                            neg2_entity_list.append(entity)
                            neg2_word_list.extend(neg2_word)                          
    ###########情感判断结束=====
    '''         
    ###########文本分类开始判断===== 
    lable = ''
    #title = '2017证券从业《金融市场基础》知识：基金与股票'
    #url = 'http%3A%2F%2Firm.cninfo.com.cn%2Fircs%2Finteraction%2FviewQuestionForSzse.do%3FquestionId%3D6126764'
    not_tit = title_keywords.search(title)
    #not2_tit = re.search(not_title_keywords,title)
    not_con = con_keywords.search(content)
    not_url = url_keywords.search(url)
    
    ####判断是否属于研报
    
    RRTK = research_report_TK.search(title)
    not_RRTK = not_research_report_TK.search(title)
    
    
    if RRTK and not not_RRTK:
        lable = '研报'
    '''
    #####判断是否属于公告
    ATK = announcement_TK.search(title)
    not_ATK = not_announcement_TK.search(title)
    if ATK and not not_ATK:
        if lable == '':
            lable = '公告'
        else:
            lable = lable +','+ '公告'
            
    ####判断是否属于二级市场专项
    MTK = re.search(market_TK,title)
    if MTK:
        if lable =='':
            lable = '二级市场专项'
        else:
            lable = lable +','+'二级市场专项'
    '''
    
    #print ('svm data receive successful')

    word_cut = jieba.lcut(content.strip(), cut_all = False)
    news1 = []
    news1.append(' '.join(word_cut))

    #print ('===IF judge====')
    vec_testif = IFvec.transform(news1)
    tf_testif = IFtransformer.transform(vec_testif)
    ch2_testif = IFch2.transform(tf_testif)
    yif = IFclf.predict(ch2_testif)
    #print ('svm model judge successful')
    if yif[0] == 0:
        IF = IF_keywords.search(title)
        not_IF = IF_not_keywords.search(content)
        if IF and not not_IF:
            if lable == '':
                lable =  '互联网金融'
            else:
                lable =  lable +','+ '互联网金融'
    else:
        if lable == '':
            lable =  '互联网金融'
        else:
            lable =  lable +','+ '互联网金融'
            
    #print ('====im IF rules====')
    #######文本分类(区分正负面)
    if not_con or not_url or not_tit or len(content) < 120:
        
        print ('dont svm')
    else:
        ######judge entity
        if len(entitylist) != 0:
            #print ('entityList exist')
            
            vec_testpn = pn1vec.transform(news1)
            tf_testpn = pn1transformer.transform(vec_testpn)
            ch2_testpn = pn1ch2.transform(tf_testpn)
            ypn = pn1clf.predict(ch2_testpn)
            if ypn[0] == 1:
                #print ('its neg')
                #print ('====admin judge====') 
                vec_testad = advec.transform(news1)
                tf_testad = adtransformer.transform(vec_testad)
                ch2_testad = adch2.transform(tf_testad)
                yad = adclf.predict(ch2_testad)
                ad_key = ad_keywords.search(content)
                not_ad_key = not_ad_keywords.search(content)
                if yad[0] == 1 and ad_key and not not_ad_key:
                    if lable == '':
                        lable =  '高管股东类预警'
                    else:
                        lable = lable +','+ '高管股东类预警'
                    ad_flag = True
                    ad1_key = ad1_keywords.search(content)
                    not_ad1_key = not_ad1_keywords.search(content)
                    ad2_key = ad2_keywords.search(content)
                    not_ad2_key = not_ad2_keywords.search(content)
                    ad3_key = ad3_keywords.search(content)
                    not_ad3_key = not_ad3_keywords.search(content)
                    ad4_key = ad4_keywords.search(content)
                    not_ad4_key = not_ad4_keywords.search(content)
                    ad5_key = ad5_keywords.search(content)
                    not_ad5_key = not_ad5_keywords.search(content)
                    if ad1_key and not not_ad1_key:
                        lable = lable + ','+'失职或股份转让问题'
                        ad_flag = False
                    if ad2_key and not not_ad2_key:
                        lable = lable +',' + '涉及违法违规'
                        ad_flag = False
                    if ad3_key and not not_ad3_key:
                        lable = lable + ',' + '高管或公司出现重大变动'
                        ad_flag = False
                    if ad4_key and not not_ad4_key:
                        lable = lable + ',' + '高管股东之间问题'
                        ad_flag = False
                    if ad5_key:
                        lable = lable + ',' + '涉及员工的问题'
                        ad_flag = False
                    if ad_flag and not not_ad5_key:
                        lable = lable + ',' + '高管或公司其它类'
                #print ('====im admin rules====')
                
                #print ('====assure judge====')
                vec_testas = asvec.transform(news1)
                tf_testas = astransformer.transform(vec_testas)
                ch2_testas = asch2.transform(tf_testas)
                yas = asclf.predict(ch2_testas)
                ass_ = ass_keywords.search(content)
                not_ass = not_ass_keywords.search(content)
                if yas[0] ==1 and ass_ and not not_ass:
                    if lable == '':
                        lable =  '担保类预警'
                    else:
                        lable = lable +','+ '担保类预警'
                    ass_flag = True
                    ass1_key = ass1_keywords.search(content)
                    ass2_key = ass2_keywords.search(content)
                    not_ass1_key = not_ass1_keywords.search(content)
                    if ass1_key and not not_ass1_key:
                        lable = lable +','+'担保方问题或违规担保'
                        ass_flag = False
                    if ass2_key:
                        lable = lable + ',' + '对外担保过多'
                        ass_flag = False
                    if ass_flag:
                        lable = lable + ',' + '担保其它类'
                #print ('====im assre rules====')
                
                #print ('====credit judge====')     
                vec_testcre = crevec.transform(news1)
                tf_testcre = cretransformer.transform(vec_testcre)
                ch2_testcre = crech2.transform(tf_testcre)
                ycre = creclf.predict(ch2_testcre)
                cre_key = credit_keywords.search(content)
                not_cre_key = not_credit_keywords.search(content)
                if ycre[0] == 1 and cre_key and not not_cre_key:
                    if lable == '':
                        lable =  '信用类预警'
                    else:
                        lable = lable +','+ '信用类预警'
                    cre_flag = True
                    cre1_key = cre1_keywords.search(content)
                    not_cre1_key = not_cre1_keywords.search(content)
                    cre2_key = cre2_keywords.search(content)
                    not_cre2_key = not_cre2_keywords.search(content)
                    cre3_key = cre3_keywords.search(content)
                    not_cre3_key = not_cre3_keywords.search(content)
                    cre4_key = cre4_keywords.search(content)
                    not_cre4_key = not_cre4_keywords.search(content)
                    cre5_key = cre5_keywords.search(content)
                    not_cre5_key = not_cre5_keywords.search(content)
                    cre6_key = cre6_keywords.search(content)
                    not_cre6_key = not_cre6_keywords.search(content)
                    if cre1_key and not not_cre1_key:
                        lable = lable + ',' + '失信问题'
                        cre_flag = False
                    if cre2_key and not not_cre2_key:
                        lable = lable + ',' + '挪占用资金或改变用途'
                        cre_flag = False
                    if cre3_key and not not_cre3_key:
                        lable = lable + ',' + '评级下调推迟或负面'
                        cre_flag = False
                    if cre4_key and not not_cre4_key:
                        lable = lable + ',' + '虚假宣传或造假'
                        cre_flag = False
                    if cre5_key and not not_cre5_key:
                        lable = lable + ',' + '经营异常或负债高'
                        cre_flag = False
                    if cre6_key and not not_cre6_key:
                        lable = lable + ',' + '违约或逾期'
                        cre_flag = False
                    if cre_flag:
                        lable = lable + ',' + '信用其它类'
                    
               # print ('====im credit rules====')
                
                #print ('======== finance judge====')  
                vec_testfin = finvec.transform(news1)
                tf_testfin = fintransformer.transform(vec_testfin)
                ch2_testfin = finch2.transform(tf_testfin)
                yfin = finclf.predict(ch2_testfin)
                
                fin_ = fin_keywords.search(content)
                not_fin = not_fin_keywords.search(content)
                not_fin1 = not_fin_keywords1.search(content)
                not_fin2 = not_fin_keywords2.search(content)
                if yfin[0] == 1 and fin_ and not not_fin:
                    if not_fin1:
                        if not_fin2:
                            if lable == '':
                                lable =  '财务类预警'
                            else:
                                lable = lable +','+ '财务类预警'
                            fin_flag = True
                            fin1_key = fin1_keywords.search(content)
                            fin2_key = fin2_keywords.search(content)
                            fin3_key = fin3_keywords.search(content)
                            fin4_key = fin4_keywords.search(content)
                            fin5_key = fin5_keywords.search(content)
                            not_fin1_key = not_fin1_keywords.search(content)
                            not_fin2_key = not_fin2_keywords.search(content)
                            not_fin3_key = not_fin3_keywords.search(content)
                            not_fin4_key = not_fin4_keywords.search(content)
                            not_fin5_key = not_fin5_keywords.search(content)
                            if fin1_key and not not_fin1_key:
                                lable = lable + ',' + '财务造假'
                                fin_flag = False
                            if fin2_key and not not_fin2_key:
                                lable = lable + ',' + '财务亏损或指标下降'
                                fin_flag = False
                            if fin3_key and not not_fin3_key:
                                lable = lable + ',' + '有关会计所问题'
                                fin_flag = False
                            if fin4_key and not not_fin4_key:
                                lable = lable + ',' + '债务问题'
                                fin_flag = False
                            if fin5_key and not not_fin5_key:
                                lable = lable + ',' + '资金问题'
                                fin_flag = False
                            if fin_flag:
                                lable = lable + ',' + '财务其它类'
                    else:
                        if lable == '':
                            lable =  '财务类预警'
                        else:
                            lable = lable +','+ '财务类预警'
                        fin_flag = True
                        fin1_key = fin1_keywords.search(content)
                        fin2_key = fin2_keywords.search(content)
                        fin3_key = fin3_keywords.search(content)
                        fin4_key = fin4_keywords.search(content)
                        fin5_key = fin5_keywords.search(content)
                        not_fin1_key = not_fin1_keywords.search(content)
                        not_fin2_key = not_fin2_keywords.search(content)
                        not_fin3_key = not_fin3_keywords.search(content)
                        not_fin4_key = not_fin4_keywords.search(content)
                        not_fin5_key = not_fin5_keywords.search(content)
                        if fin1_key and not not_fin1_key:
                            lable = lable + ',' + '财务造假'
                            fin_flag = False
                        if fin2_key and not not_fin2_key:
                            lable = lable + ',' + '财务亏损或指标下降'
                            fin_flag = False
                        if fin3_key and not not_fin3_key:
                            lable = lable + ',' + '有关会计所问题'
                            fin_flag = False
                        if fin4_key and not not_fin4_key:
                            lable = lable + ',' + '债务问题'
                            fin_flag = False
                        if fin5_key and not not_fin5_key:
                            lable = lable + ',' + '资金问题'
                            fin_flag = False
                        if fin_flag:
                            lable = lable + ',' + '财务其它类'

                    
                #print ('====im finance rules====')        
                        
                #print ('======== manage judge====')       
                vec_testman = manvec.transform(news1)
                tf_testman = mantransformer.transform(vec_testman)
                ch2_testman = manch2.transform(tf_testman)
                yman = manclf.predict(ch2_testman)
                man_ = re.search(manage_keywords,content)
                not_man = re.search(not_man_keywords,content)
                if yman[0] == 1 and man_ and not not_man:
                    if lable == '':
                        lable =  '经营管理类预警'
                    else:
                        lable = lable +','+ '经营管理类预警'
                    man_flag = True
                    man1_key = man1_keywords.search(content)
                    man2_key = man2_keywords.search(content)
                    man3_key = man3_keywords.search(content)
                    man4_key = man4_keywords.search(content)
                    man5_key = man5_keywords.search(content)
                    man6_key = man6_keywords.search(content)
                    man7_key = man7_keywords.search(content)
                    man8_key = man8_keywords.search(content)
                    man9_key = man9_keywords.search(content)
                    man10_key = man10_keywords.search(content)
                    man11_key = man11_keywords.search(content)
                    man12_key = man12_keywords.search(content)
                    man13_key = man13_keywords.search(content)
                    man14_key = man14_keywords.search(content)
                    man15_key = man15_keywords.search(content)
                    not_man1_key = not_man1_keywords.search(content)
                    not_man2_key = not_man2_keywords.search(content)
                    not_man3_key = not_man3_keywords.search(content)
                    not_man5_key = not_man5_keywords.search(content)
                    not_man7_key = not_man7_keywords.search(content)
                    not_man8_key = not_man8_keywords.search(content)
                    not_man10_key = not_man10_keywords.search(content)
                    not_man13_key = not_man13_keywords.search(content)
                    if man1_key and not not_man1_key:
                        lable = lable + ',' + '减资合并破产等'
                        man_flag = False
                    if man2_key and not not_man2_key:
                        lable = lable + ',' + '合作方或环保问题'
                        man_flag = False
                    if man3_key and not not_man3_key:
                        lable = lable + ',' + '盲目扩张或生产问题'
                        man_flag = False
                    if man4_key:
                        lable = lable + ',' + '对外借款过多'
                        man_flag = False
                    if man5_key and not not_man5_key:
                        lable = lable + ',' + '出售或收购问题'
                        man_flag = False
                    if man6_key:
                        lable = lable + ',' + '资产查封扣押冻结'
                        man_flag = False
                    if man7_key and not not_man7_key:
                        lable = lable + ',' + '市场份额或收入下降'
                        man_flag = False
                    if man8_key and not not_man8_key:
                        lable = lable + ',' + '发送亏损或投资失误'
                        man_flag = False
                    if man9_key:
                        lable = lable + ',' + '事故生产问题'
                        man_flag = False
                    if man10_key and not not_man10_key:
                        lable = lable + ',' + '经营活动环境变化'
                        man_flag = False
                    if man11_key:
                        lable = lable + ',' + '融资失败'
                        man_flag = False
                    if man12_key:
                        lable = lable + ',' + '资产转让或重组'
                        man_flag = False
                    if man13_key and not not_man13_key:
                        lable = lable + ',' + '资金周转困难'
                        man_flag = False
                    if man14_key:
                        lable = lable + ',' + '资金回收风险'
                        man_flag = False
                    if man15_key:
                        lable = lable + ',' + '涉法问题'
                        man_flag = False
                    if man_flag:
                        lable = lable + ',' + '经营管理其它类'
                #print ('====im manage rules====')
                
                #print ('======== market judge====')       
                vec_testmar = marvec.transform(news1)
                tf_testmar = martransformer.transform(vec_testmar)
                ch2_testmar = march2.transform(tf_testmar)
                ymar = marclf.predict(ch2_testmar)
                not_mar = not_mar_keywords.search(content)
                mar_ = mar_keywords.search(content)
                if ymar[0] == 1 and mar_ and not not_mar:
                    if lable == '':
                        lable =  '市场类预警'
                    else:
                        lable = lable +','+ '市场类预警'
                    
                    mar_flag = True
                    mar1_key = mar1_keywords.search(content)
                    mar2_key = mar2_keywords.search(content)
                    mar3_key = mar3_keywords.search(content)
                    mar4_key = mar4_keywords.search(content)
                    mar5_key = mar5_keywords.search(content)
                    not_mar1_key = not_mar1_keywords.search(content)
                    not_mar2_key = not_mar2_keywords.search(content)
                    not_mar3_key = not_mar3_keywords.search(content)
                    not_mar4_key = not_mar4_keywords.search(content)
                    not_mar5_key = not_mar5_keywords.search(content)
                    if mar1_key and not not_mar1_key:
                        lable = lable + ',' + '股份资产转让减持减少'
                        mar_flag = False
                    if mar2_key and not not_mar2_key:
                        lable = lable + ',' + '股权问题'
                        mar_flag = False
                    if mar3_key and not not_mar3_key:
                        lable = lable + ',' + '暂停交易发行或面临警示'
                        mar_flag = False
                    if mar4_key and not not_mar4_key:
                        lable = lable + ',' + '证券价格异常波动'
                        mar_flag = False
                    if mar5_key and not not_mar5_key:
                        lable = lable + ',' + '做空股价报告'
                        mar_flag = False
                    if mar_flag:
                        lable = lable + ',' + '市场其它类'
                    
                #print ('====im market rules====')
                
               # print ('======== product judge====')
                vec_testpro = provec.transform(news1)
                tf_testpro = protransformer.transform(vec_testpro)
                ch2_testpro = proch2.transform(tf_testpro)
                ypro = proclf.predict(ch2_testpro)
                pro_ = pro_keywords.search(content)
                not_pro = not_pro_keywords.search(content)
                #print ('产品：'+ str(ypro[0]))
                if ypro[0] == 1 and pro_ and not not_pro:
                    if lable == '':
                        lable =  '产品类预警'
                    else:
                        lable = lable +','+ '产品类预警'
                    
                    pro_flag = True
                    pro1_key = pro1_keywords.search(content)
                    pro2_key = pro2_keywords.search(content)
                    if pro1_key:
                        lable = lable + ',' + '产品设计或生产问题'
                        pro_flag = False
                    if pro2_key:
                        lable = lable + ',' + '产品侵权'
                        pro_flag = False
                    if pro_flag:
                        lable = lable + ',' + '产品其它类'
                    
                #print ('====im product rules====')
                
                #print ('======== project judge====')
                #vec_testproj = projvec.transform(news1)
                #tf_testproj = projtransformer.transform(vec_testproj)
                #ch2_testproj = projch2.transform(tf_testproj)
                #yproj = projclf.predict(ch2_testproj)
                proj_ = proj_keywords.search(content)
                not_proj = not_proj_keywords.search(content)
                if proj_ and not not_proj:
                    if lable == '':
                        lable =  '项目类预警'
                    else:
                        lable = lable +','+ '项目类预警'
                    
                    proj_flag = True
                    proj1_key = proj1_keywords.search(content)
                    proj2_key = proj2_keywords.search(content)
                    proj3_key = proj3_keywords.search(content)
                    not_proj1_key = not_proj1_keywords.search(content)
                    if proj1_key and not not_proj1_key:
                        lable = lable + ',' + '项目停建或延期'
                        proj_flag = False
                    if proj2_key:
                        lable = lable + ',' + '项目审批问题'
                        proj_flag = False
                    if proj3_key:
                        lable = lable + ',' + '项目投产产能问题'
                        proj_flag = False
                    if proj_flag:
                        lable = lable + ',' + '项目其它类'
                    
                #print ('====im project rules====')
                
                #print ('======== regulate judge====')       
                vec_testreg = regvec.transform(news1)
                tf_testreg = regtransformer.transform(vec_testreg)
                ch2_testreg = regch2.transform(tf_testreg)
                yreg = regclf.predict(ch2_testreg)
                reg_ = reg_keywords.search(content)
                not_reg = not_reg_keywords.search(content)
                if yreg[0] == 1 and reg_ and not not_reg:
                    if lable == '':
                        lable =  '监管类预警'
                    else:
                        lable = lable +','+ '监管类预警'
                    
                    reg_flag = True
                    reg1_key = reg1_keywords.search(content)
                    reg2_key = reg2_keywords.search(content)
                    reg3_key = reg3_keywords.search(content)
                    reg4_key = reg4_keywords.search(content)
                    reg5_key = reg5_keywords.search(content)
                    not_reg1_key = not_reg_keywords1.search(content)
                    not_reg5_key = not_reg5_keywords.search(content)
                    if reg1_key and not not_reg1_key:
                        lable = lable + ',' + '行政处罚'
                        reg_flag = False
                    if reg2_key:
                        lable = lable + ',' + '监管措施'
                        reg_flag = False
                    if reg3_key:
                        lable = lable + ',' + '业务管理措施'
                        reg_flag = False
                    if reg4_key:
                        lable = lable + ',' + '审批问题'
                        reg_flag = False
                    if reg5_key and not not_reg5_key:
                        lable = lable + ',' + '监管问询或关注'
                        reg_flag = False
                    if reg_flag:
                        lable = lable + ',' + '监管其它类'
                    
               # print ('====im regulate rules====')
                
                #print ('======== unforce judge====')   
                vec_testunf = unfvec.transform(news1)
                tf_testunf = unftransformer.transform(vec_testunf)
                ch2_testunf = unfch2.transform(tf_testunf)
                yunf = unfclf.predict(ch2_testunf)
                unf_ = unf_keywords.search(content)
                not_unf = not_unf_keywords.search(content)
                if yunf[0] == 1 and unf_ and not not_unf:
                    if lable == '':
                        lable =  '不可抗力预警'
                    else:
                        lable = lable +','+ '不可抗力预警'
                #print ('====im unforce rules====')
                
                #print ('======== other judge====')
                #vec_testoth = othvec.transform(news1)
                #tf_testoth = othtransformer.transform(vec_testoth)
                #ch2_testoth = othch2.transform(tf_testoth)
                #yoth = othclf.predict(ch2_testoth)       
                #if yoth[0] == 1:
                #not_oth = oth_keywords.search(content)
                if lable == '':
                    lable =  '其它类预警'
                #else:
                    #lable = lable +','+ '其它类预警'
                #print ('====im other rules====')
    #rt = {'SVM_TextSort':lable,'neg1_entity':neg1_entity_list,'neg1_word':neg1_word_list,
          #'neg2_entity':neg2_entity_list,'neg2_word':neg2_word_list}
    rt = {'SVM_TextSort':lable}
    #print ('svm change json successful')
    #time_end=time.time()
    #print ('svm totally cost',time_end-time_start)
    #print (rt)
    return json.dumps(rt)


@app.route('/SVM_ShortText/', methods=['POST'])
def SVM_ShortText():
    #time_start=time.time()
    
    #url = request.form.get('siteDomain')
    #text = request.form.get('content')
    #title = request.form.get('title')
    
    #url = request.json['siteDomain']    
    text = request.json['content']
    #title = request.json['title']
    
    lable = ''
    neg_word = ''
    content = text
    neg1_text = re.findall(neg1,content)
    neg2_text = re.findall(neg2,content)
    
    if len(neg1_text)>1:
        #no_neg1_text = re.search('('+no+').{0,5}'+neg1_text.group(),content)
        #if not no_neg1_text:
        lable = '-1'
        neg_word = neg1_text[0]
    if len(neg2_text)>1:
        #no_neg2_text = re.search('('+no+').{0,5}'+neg2_text.group(),content)
        #if not no_neg2_text:
        lable = '-2'
        neg_word = neg2_text[0]
    if lable == '':
        lable = '0'
    
    rt = {'SVM_ShortText':lable,'neg_word':neg_word}
    #print ('svm change json successful')
    #time_end=time.time()
    #print ('svm totally cost',time_end-time_start)
    #print (rt)
    return json.dumps(rt)


if __name__ == '__main__':
    app.run(host = '0.0.0.0')
    
    

