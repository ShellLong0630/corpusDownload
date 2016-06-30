#!/usr/bin/python
#coding=utf-8
import MySQLdb
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def get_abcdef(num):
	typestr = 0
	if num == "#A": 
		typestr = 4  
	elif num == "#B":
		typestr =  5
	elif num == "#C" :
		typestr = 6
	elif num == "#D" :
		typestr = 7
	elif num == "#E":
		typestr =  8
	elif num == "#F":
		typestr =  9
	else:
		typestr = None
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

cur.execute("SELECT \
* \
FROM \
music_target_tb \
")
tagmusicdb = list(cur.fetchall())
cur.execute("SELECT \
* \
FROM \
dance_target_tb \
")
tagdancedb = list(cur.fetchall())
targetdb = []
targetdb.extend(tagmusicdb)
targetdb.extend(tagdancedb)

#a=cur.execute("show tables")
cur.execute("SELECT \
music_mode,music_code \
FROM \
mark_all_view \
")
#c=cur.execute("show variables like 'character_set_%'")
fd=open('./word_relation.txt', 'wrb') #只写模式,不是追加w+ ,所以每次会从头写


info = cur.fetchall()
index = list(info)
index = set(index)
#取MUSIC	M_9.0 这样放入集合作为索引
a="无"
#print a.decode('gb2312')

for line in index:	#line----- MUSIC	M_9.0
	cur.execute("SELECT \
		feedBackMark  \
		FROM \
		mark_all_view \
		where music_mode = %s and music_code = %s ",(line[0],line[1]))
	info1 = cur.fetchall()
	if len(info1) < 2 :
		continue
	# 取得了MUSIC 10 的#A #B 组合
	findnull = 0
	for line1 in targetdb: # 遍历line1  target的全部数据条目
		if line1[2] != line[0]:
			continue
		findnull = 0
		item = ''
		arg1= ''

		for line2 in info1: # #A #B
			if line2[0] == '':
				findnull = 1
				break
			if line2[0] == None:
				continue
			if line1[get_abcdef(line2[0])] == None or line1[get_abcdef(line2[0])] == a.decode('gb2312'):
				findnull = 1
				break
			arg1 = arg1+line2[0]
			item = item+line1[get_abcdef(line2[0])]+"####"
		item = item+'-:-'+line[0]+'-:-'+line[1]+'-:-'+arg1+'\n'
		if findnull != 1:			
			fd.write(item.encode('gbk'))
			#print get_abcdef(line2[0])
			#print line2[0],get_abcdef(line2[0])
			#if get_abcdef(line2[0]) == None
			#item=item+line1(get_abcdef(line2[0]))



		
'''	
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
			item=line[i]+"-:-"+weigth[count][i-2]+'-:-'+arg1+'-:-'+arg2
			fd.write(item)
			fd.write('\n')
			#print item
		else:
			print line[0],arg1,"not find !!"
	count+=1






'''











cur.close()
#conn.commit() #请注意一定要有conn.commit()这句来提交事务，要不然不能真正的插入数据。
conn.close()
fd.close()


