
import psycopg2


command = 'get'
targethostname = 'localhost'
targetdatabase = 'crosswell'
targetusername = 'auliafauzi'
targetpassword = ''
query = 'select * from cms.content'



def ConnectToPostgres(command, targethostname, targetdatabase, targetusername, targetpassword,data,query) :

	body = None
	try :
		conn = None
		conn = psycopg2.connect(host=targethostname, database=targetdatabase, user= targetusername)
		cur = conn.cursor()
		if command == 'get':
			cur.execute(query)
		elif command =='push':
			cur.execute(query,data)
		elif command == 'pushmany':
			cur.executemany(quer,data)
		conn.commit()
		body = cur.fetchall()
		cur.close()
	except : 
		body =  "- failed to connect the data into database"
	finally:
		if conn is not None:
			conn.close()
	# return result, pushToDBError
	return body

print(ConnectToPostgres(command,targethostname,targetdatabase,targetusername,None,None,query))