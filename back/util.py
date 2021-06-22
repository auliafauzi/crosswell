
import psycopg2
import re

data_structure = {
	'content' : ['content_id', 'title', 'content', 'user_id','long','lat','image_path','file_path', 'date'],
	'comment' : ['comment_id', 'comment', 'user_id', 'parent_id','date']
} 

def query(param1, param2) :
	if param1 == "contentList" :
		 return "select content_id, title, concat(left(content, 350), '...'), user_id, long, lat, image_path, file_path , date from cms.content order by date desc;"
	elif param1 == "getContent" :
		return "select content_id, title, content, user_id, long, lat, image_path, file_path, date  from cms.content where content_id ='"+param2+"' order by date desc"
	elif param1 == 'commentList' :
		return "select * from cms.comment where parent_id ='"+param2+"' order by date asc"
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


# print(ConnectToPostgres(methods,targethostname,targetdatabase,targetusername,None,None,query))