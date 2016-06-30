#!/usr/bin/python
#coding=utf-8
import MySQLdb
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def get_abcdef(num):
	typestr = ""
	if num == 2: 
		typestr = "#A" 
	elif num == 3:
		typestr = "#B" 
	elif num == 4:
		typestr = "#C" 
	elif num == 5:
		typestr = "#D" 
	elif num == 6:
		typestr = "#E" 
	elif num == 7:
		typestr = "#F" 
	else:
		typestr = ''
	return typestr


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
* \
FROM \
music_target_tb \
order by music_code asc")
#c=cur.execute("show variables like 'character_set_%'")
fd=open('./target_inten.txt', 'wrb') #只写模式,不是追加w+ ,所以每次会从头写
#取MUSIC	M_9.0 这样放入集合作为索引
index = []
weigth = []
item = []
count = 0
info = cur.fetchall()
for line in info:
	index.append(line[2:10])
	weigth.append(line[11:17])

a="无"
#print a.decode('gb2312')

for line in index:
	for i in range(2,8):
		arg2=''
		item=''
		# 取得了前6列,用对应的#abcd去找意图号
		if line[i] == a.decode('gb2312') or line[i] == None:
			continue
		#	arg1是#ABCD...
		arg1 = get_abcdef(i)
		cur.execute("SELECT \
		music_code  \
		FROM \
		mark_all_view \
		where music_mode = %s and feedBackMark = %s ",(line[0],arg1))
		
		info1 = cur.fetchall()	
		#info1是由MUSIC #E 查询到的意图标号
		if len(info1) > 0:
			for line2 in info1:
				arg2 = arg2+line[0]+' '+line2[0]+','
			item=line[i]+"-:-"+weigth[count][i-2]+'-:-'+arg1+'-:-'+arg2+'\n'
			fd.write(item.encode('gbk'))
			#print item
		else:
			print line[0],arg1,"not find !!"
	count+=1











cur.execute("SELECT \
* \
FROM \
dance_target_tb \
")

index = []
weigth = []
item = []
count = 0
info = cur.fetchall()
for line in info:
	index.append(line[2:9])
	weigth.append(line[10:15])



for line in index:
	for i in range(2,7):
		arg2=''
		item=''
		# 取得了前6列,用对应的#abcd去找意图号
		if line[i] == a.decode('gb2312') or line[i] == None:
			continue
		#	arg1是#ABCD...
		arg1 = get_abcdef(i)
		cur.execute("SELECT \
		music_code  \
		FROM \
		mark_all_view \
		where music_mode = %s and feedBackMark = %s ",(line[0],arg1))
		
		info1 = cur.fetchall()	
		#info1是由MUSIC #E 查询到的意图标号
		if len(info1) > 0:
			for line2 in info1:
				arg2 = arg2+line[0]+' '+line2[0]+','
			item=line[i]+"-:-"+weigth[count][i-2]+'-:-'+arg1+'-:-'+arg2+'\n'
			fd.write(item.encode('gbk'))
		else:
			print line[0],arg1,"not find !!"
	count+=1















cur.close()
#conn.commit() #请注意一定要有conn.commit()这句来提交事务，要不然不能真正的插入数据。
conn.close()
fd.close()


