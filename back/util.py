
import psycopg2
import re
import string
import secrets

data_structure = {
	'content' : ['content_id', 'title', 'content', 'user_id','long','lat','image_path','file_path', 'date', 'count_comment'],
	'comment' : ['comment_id', 'comment', 'user_id', 'parent_id','date'],
	'userLess' : ['user_id', 'user_name', 'role_id', 'token_expired' ]
} 

def query(param1, param2,param3) :
	if param1 == "contentList" :
		 return "select content_id, title, concat(left(content, 350), '...'), cont.user_id, long, lat, image_path, file_path , cont.date, com.counting from cms.content cont left join (select parent_id , count(comment_id) as counting from cms.comment group by parent_id) as com on cont.content_id = com.parent_id  order by date desc;"
	elif param1 == "getContent" :
		return "select content_id, title, content, user_id, long, lat, image_path, file_path, date  from cms.content where content_id ='"+param2+"' order by date desc"
	elif param1 == 'commentList' :
		return "select * from cms.comment where parent_id ='"+param2+"' order by date asc"
	elif param1 == 'next_id' :
		return "select max(NULLIF(regexp_replace("+param2+", '\D','','g'), '')::numeric) +1 from cms."+param3
	elif param1 == 'count_comment' :
		return "select count(comment_id) from cms.comment where parent_id = " + param2
	elif param1 == 'get_image_path' :
		return "select image_path from cms.content where content_id = '" + param2 + "';"
	elif param1 == 'user_less' :
		return "select user_id, user_name, user_role, token_expired from cms.user where token = '" + param2 + "';"
	elif param1 == 'login':
		return "select token, token_expired, user_id, user_role, case when now() < token_expired then 'true' else 'false' end as status from cms.user where user_name ='"+param2+"' and password ='"+param3+"';"
	elif param1 == 'push_new_token':
		return 'a'
	else :
		return

def connectToPostgres(methods, targethostname, targetdatabase, targetusername, targetpassword,data,query) :
	body = None
	try :
		conn = None
		conn = psycopg2.connect(host=targethostname, database=targetdatabase, user= targetusername)
		cur = conn.cursor()
		if methods == 'get':
			cur.execute(query)
			body = cur.fetchall()
		if methods == 'get_one':
			cur.execute(query)
			body = cur.fetch()
		elif methods =='push':
			cur.execute(query,data)
			body = "- push to data warehouse is succsess \n"
		elif methods == 'pushmany':
			cur.executemany(quer,data)
		conn.commit()
		cur.close()
	except : 
		body =  "- failed to connect the data into database"
	finally:
		if conn is not None:
			conn.close()
	return body

def getMax(listString):
	# try :
	int_only = []
	for i in listString :
		int_only.append(re.findall('\d+', str(i)))
	result = max(int_only)
	# except :
	# 	result : "failed to get max number"
	return result

def insertQuery(tablename, data):
	# col,_,_ = readColumn(data)
	query = "INSERT INTO %s VALUES (" % tablename
	for i in range(len(data)) :
		if i == len(data)-1 :
			query = query + "%s);"
		else :
			query = query + "%s,"
	return query

def insertQueryWithColumn(tablename, data, targetcol):
	query = "INSERT INTO %s (" % tablename
	for i in range(len(targetcol)) :
		if i == len(targetcol)-1 :
			query = query + targetcol[i] + ") "
		else :
			query = query + targetcol[i] + ","
	query = query + "VALUES ("
	for i in range(len(targetcol)) :
		if i == len(targetcol)-1 :
			query = query + "%s);"
		else :
			query = query + "%s,"
	return query

def updateQueryWithColumn(tablename, data, targetcol, targetrow, value_target):
	query = "UPDATE %s SET " % tablename
	for i in range(len(targetcol)) :
		if i == len(targetcol)-1 :
			query = query + targetcol[i] + " = '" + data[i] + "' "
		else :
			query = query + targetcol[i] + " = '" + data[i] + "',"
	# query = query + "VALUES ("
	# for i in range(len(targetcol)) :
	# 	if i == len(targetcol)-1 :
	# 		query = query + "%s);"
	# 	else :
	# 		query = query + "%s,"
	query = query + "where " + targetrow + " = '" + value_target + "';"
	return query

def generateToken(user_id, date):
	token = secrets.token_hex(16)
	token = token + user_id + date
	return token



# print(ConnectToPostgres(methods,targethostname,targetdatabase,targetusername,None,None,query))