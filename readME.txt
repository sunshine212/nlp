testIF 文件为判断文本是否为互联网金融并且去重复
SimHash 文件为将文本转换为哈希值并计算海明距离的方法
stockPriceVolatility 文件为验证模型 涉及到四个模型vsm tfidf chi svm
InterFin 文件为读取idx文件
RFIF.py  文件 为通过restful 设置一个API接口
RFIFL.py  为linux服务器上的代码
tab.py   为添加人物信息标签

预警类文章不仅仅是负面文章，还包括一些重大事项的文章（如并购、重组、回购、转型、转让股份或股权、收购资产或股份或公司、
质押高、贷款率高、拆分、出售股权或股份、IPO、布局新产业、合并、增资、高管的任命、大宗交易、对外投资）

11111

svm_chanel 文本二三级分类标签
SENTIMENT  短文本情感签

ad1_keywords = 高管股东企业接班人问题
ad2_keywords = 高管涉及违法违规
ad3_keywords = 高管出现重大变动
ad4_keywords = 高管股东之间出现矛盾
ad5_keywords = 与员工之间的问题
ad6_keywords = 高管其它类

ass1_keywords = 违规担保或担保一方出现问题
ass2_keywords = 对外担保过多

cre1_keywords = 相关人士或企业失信
cre2_keywords = 挪用或占用资金改变用途
cre3_keywords = 评级关注及下调或列入负面观察或推迟评级
cre4_keywords = 欺诈或虚假宣传或造假
cre5_keywords = 企业失联列入经营异常或负债过高
cre6_keywords = 企业相关人士或本身违约或信贷逾期

fin1_keywords = 财务造假
fin2_keywords = 发生亏损下跌或财务指标下降
fin3_keywords = 会计所问题
fin4_keywords = 资不抵债或负债高
fin5_keywords = 资金不足或来源不明

mar1_keywords = 股份资产转让或减持或减少
mar2_keywords = 股权质押或冻结或爆仓
mar3_keywords = 暂停交易或上市发行、面临风险警示
mar4_keywords = 证券价格异常波动
mar5_keywords = 做空股价报告(包括但不限于券商报告)

pro1_keywords = 产品设计或生产缺陷或属于淘汰类
pro2_keywords = 产品侵权
pro3_keywords = 其它产品类预警

proj1_keywords = 项目出现停建或延期
proj2_keywords = 项目审批手续不完备
proj3_keywords = 项目投产后产能与预期存在差距
proj4_keywords = 其它项目类预警

man1_keywords = 减资或合并或重组或破产等
man2_keywords = 与合作方的问题或环保问题
man3_keywords = 主业不突出或盲目扩张或资金或生产问题
man4_keywords = 对外借款过多
man5_keywords = 出售或收购公司主营资产
man6_keywords = 资产转让与资产查封或扣押冻结问题
man7_keywords = 市场份额或竞争力或收入净利下降
man8_keywords = 发生亏损或投资决策失误
man9_keywords = 事故或生产问题或停产
man10_keywords = 经营活动或环境发生变化
man11_keywords = 融资失败或取消
man12_keywords = 资产转让或重组有关问题
man13_keywords = 资金周转困难
man14_keywords = 资金回收风险
man15_keywords = 法律或司法相关问题或经济纠纷
man16_keywords = 经营管理其它类

reg1_keywords = 行政处罚
reg2_keywords = 监管措施
reg3_keywords = 监管机构对某类业务采取更为严格的管理措施
reg4_keywords = 审批不通过或监管叫停
reg5_keywords = 问询或关注

cd test
git status 看到On branch master,这个说明已经在master分之上了
更新后使用git add * --代表更新全部
git commit -m "更新说明”
git push origin master

命令删除 远程仓库不存在的分支
git remote prune origin
git branch -a 命令查看所有本地分支  

删除远程仓库的文件
git rm -r --cached 2.txt                    // 删除a目录下的2.txt文件 
git commit -m  "删除a目录下的2.txt文件"  // commit
git push 


回退版本
git log:可以查看最近到最远的提交日志。如果嫌输出信息太多，看得眼花缭乱的，可以试试加上--pretty=oneline参数,
使用git log --pretty=oneline
git reset --hard 一段commit_id的缩写：重回对应的版本，不需要全部的commit_id,只要前几位可以区分就行。
嫌麻烦的话，可以git reset --hard HEAD~num，例如 git reset --hard HEAD~100回退到前100个版本。