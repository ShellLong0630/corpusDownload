#!/usr/bin/python
#coding=utf-8
import MySQLdb
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

conn= MySQLdb.connect(
        host='rdssva8w61o860246h8x.mysql.rds.aliyuncs.com',
        port = 3306,
        user='weixin_test',
        passwd='weixin',
        db ='robot_corpus_db',
        charset="utf8",
        )
cur = conn.cursor()
#a=cur.execute("show tables")
cur.execute("SELECT \
music_mode, \
music_code \
FROM \
corpus_all_view \
order by music_code desc")
#c=cur.execute("show variables like 'character_set_%'")

#取MUSIC	9.0 这样放入集合作为索引
index = []
item = []
info = cur.fetchall()

fd=open('./feedback.txt', 'wrb') #只写模式,不是追加w+ ,所以每次会从头写


index = list(info)
index = set(index)
#tmp = sorted(tmp, key=lambda tmp: tmp[1])


#index 中是索引, 得到了musci M_7.0 这样的序号对儿  ,然后根据序号去取各种数据
#首先取得复数的 替换实体后的第一优先级的映射对比语料,同一场景和意图会有多种说法,所以是复数,但其反馈都要一样的.
#对每个line = (u'D_5.0', u'DANCE') 去取值
for line in index:
	arg1 = line[0]
	arg2 = line[1]
	arg3 = ""
	#取得第一字段,复数个的输入匹配语料 给我跳个#E舞
	cur.execute("SELECT \
	music_corpus \
	FROM \
	corpus_all_view \
	where music_mode = %s and music_code = %s ",(arg1,arg2))
	info1 = cur.fetchall()

	
	#取得反馈 E-Y 好的，那小胖给您跳个Ran（E,1）
	cur.execute("SELECT \
	feedBackMark, \
	music_feedback \
	FROM \
	feedback_all_view \
	where music_mode = %s and music_code = %s ",(arg1,arg2))
	info2 = cur.fetchall()
	for sub1 in info2:
		if sub1[0] == None:
			arg3 = arg3+"none"+"-##-"+sub1[1]+"-:-"
		else:
			arg3 = arg3+sub1[0]+"-##-"+sub1[1]+"-:-"
	#把多种反馈都连接成一个字串	
	#对复数的前3字段,把后一字段复制并缀上	

	#对每种映射字段 加上后面的字段
	for sub0 in info1:
		sentence=sub0[0]+'\t'+arg1+'\t'+arg2+'\t'+arg3+'\n'
		#item.append([sub0[0],arg1,arg2,arg3])
		fd.write(sentence.encode('gbk'))  

	#print info
#print item

#for item in xuhao:
	






cur.close()
#conn.commit() #请注意一定要有conn.commit()这句来提交事务，要不然不能真正的插入数据。
conn.close()
'''
fd.write(subline)
fd.write('\n')
feedBackMark
#SELECT corpus_all_view.music_code, corpus_all_view.music_mode, corpus_all_view.music_corpus FROM corpus_all_view;
'''
