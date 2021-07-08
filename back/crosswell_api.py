import flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin
import time 
import os
import json
import re
from datetime import datetime, timedelta
# from werkzeug import secure_filename
import util

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_SORT_KEYS'] = False
app.config['UPLOAD_FOLDER'] = './files'

config = {
  'ORIGINS': [
    'http://localhost:8080',  # React
    'http://127.0.0.1:8084',  # React
    'http://localhost:8004', 
  ],

  'SECRET_KEY': '...',
  'targethostname' : 'localhost',
  'targetdatabase' : 'crosswell', 
  'targetusername' : 'auliafauzi',
  'targetpassword' : ''
}


CORS(app, resources={ r'/*': {'origins': config['ORIGINS']}}, supports_credentials=True)
@cross_origin(origin='*')
# CORS(app, resources={ r'/*'}, supports_credentials=True)


@app.route('/api/v1/test', methods=['GET'])
def api_test():
	methods = 'get'
	query = 'select * from cms.content order by date desc'
	result = util.connectToPostgres(methods,config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,query)
	return jsonify({"message":result,"code":200})

@app.route('/api/v1/contentList', methods= ['GET'])
def contentList():
	result = []
	headers = flask.request.headers
	bearer = headers.get('Authorization')    # Bearer YourTokenHere
	token = bearer.split()[1]  # YourTokenHere
	userLess = util.connectToPostgres('get',config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,util.query('user_less',token, None))
	if userLess == []:
		return jsonify({"code":500,"status":"failed","message":"You have no permission to access"})
	contentList = util.connectToPostgres('get',config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,util.query('contentList',None, None))
	for i in contentList :
		zipped = dict(zip(util.data_structure['content'], i))
		result.append(zipped)
	userLess = dict(zip(util.data_structure['userLess'], userLess[0]))
	return jsonify({"message":result,"code":200, "bearer":bearer, "user":userLess})

@app.route('/api/v1/contentDetail/<string:content_id>', methods= ['GET'])
def contentDetail(content_id):
	content_result = util.connectToPostgres('get',config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,util.query('getContent',content_id, None))
	content_result = dict(zip(util.data_structure['content'], content_result[0]))
	return jsonify({"content":content_result,"code":200})

@app.route('/api/v1/contentImage/<string:content_id>', methods= ['GET'])
def contentImage(content_id):
	try :
		image_path = util.connectToPostgres('get',config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,util.query('get_image_path',content_id,None))
		# content_result = dict(zip(util.data_structure['content'], content_result[0]))
		# return jsonify({"image":image_path,"code":200})
		return flask.send_file(image_path[0][0], mimetype='image/jpeg/jpg/png', as_attachment=True)
	except : 
		return jsonify({"message":"failed to get image","code":"x01"})


@app.route('/api/v1/commentList/<string:parent_id>', methods= ['GET'])
def commentList(parent_id):
	comment_list = []
	comment_result = util.connectToPostgres('get',config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,util.query('commentList',parent_id, None))
	for i in comment_result :
		zipped = dict(zip(util.data_structure['comment'], i))
		comment_list.append(zipped)
	return jsonify({"comment":comment_list,"code":200})


@app.route('/api/v1/postContent', methods= ['POST'])
def postContet():
	headers = flask.request.headers
	bearer = headers.get('Authorization')    # Bearer YourTokenHere
	token = bearer.split()[1]  # YourTokenHere
	userLess = util.connectToPostgres('get',config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,util.query('user_less',token, None))
	if userLess == []:
		return jsonify({"code":500,"status":"failed","message":"You have no permission to access"})
	user_id  = userLess[0][0]
	new_content_id = "p" + str(util.connectToPostgres('get',config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,util.query('next_id','content_id','content'))[0][0])
	###
	context = request.get_data()
	title = request.form['title']
	content = request.form['content']
	try :
		longitude = request.form['longitude']
		latitude = request.form['latitude']
	except :
		longitude = ''
		latitude = ''
	try :
		image = request.files['image']
		filename = image.filename
		image_path = os.path.join("uploads", image.filename)
		image.save(image_path)
	except :
		image_path = ''
		image = ''
	try :
		file = request.files['file']
		filename = file.filename
		file_path = os.path.join("uploads", file.filename)
		file.save(file_path)
	except :
		file_path = ''
		file = ''
	new_content = [new_content_id,title,content,user_id,longitude,latitude,image_path,file_path,datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
	query2 = util.insertQuery("cms.content", new_content)
	result_push = util.connectToPostgres("push",config['targethostname'],config['targetdatabase'],config['targetusername'],None,new_content,util.insertQuery("cms.content", new_content))
	return jsonify({"new_content_id":new_content_id,"title":title,"content":content,"new_content":new_content,"result_push":result_push,"code":200})

@app.route('/api/v1/postComment/<string:parent_id>', methods= ['POST'])
def postComment(parent_id):
	headers = flask.request.headers
	bearer = headers.get('Authorization')
	token = bearer.split()[1]
	userLess = util.connectToPostgres('get',config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,util.query('user_less',token, None))
	if userLess == []:
		return jsonify({"code":500,"status":"failed","message":"You have no permission to access"})
	user_id = userLess[0][0]
	comment = request.json['comment']
	print(comment)
	new_coment_id = "c" + str(util.connectToPostgres('get',config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,util.query('next_id','comment_id','comment'))[0][0])
	new_comment = [new_coment_id, comment, user_id, parent_id,datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
	result_push = util.connectToPostgres("push",config['targethostname'],config['targetdatabase'],config['targetusername'],None,new_comment,util.insertQuery("cms.comment", new_comment))
	return jsonify({"new_coment_id":new_coment_id,"comment":comment,"new_comment":new_comment,"result_push":result_push,"code":200})

@app.route('/api/v1/login', methods= ['POST'])
def login():
	# context = request.get_data()
	username = request.json['username']
	password = request.json['password']
	login_result = util.connectToPostgres('get',config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,util.query('login',username,password)) 	#LOGIN, MATCH USERNAME AND PASSWORD, RETURN TOKEN 
	if login_result == [] : 	#NO USERNAME-PASSWORD MATCH
		return jsonify({"code":500,"status":"Failed","rc":102, "message": "Invalid username or password"})
	else :		#FOUND USERNAME-PASSWORD MATCH, LOGIN SUCCESSFULL
		if login_result[0][4] == 'true': #TOKEN NOT EXPIRED YET
			return jsonify({"username":username,"user_role":login_result[0][3],"user_id":login_result[0][2], "token": login_result[0][0]})
		else : 		#TOKEN EXPIRED, UPDATE NEW TOKEN AND TOKEN_EXPIRED DATETIME
			new_token = util.generateToken(login_result[0][2],datetime.now().strftime("%Y%m%d%H%M%S")) #GENERATE NEW TOKEN
			data_to_push = [new_token,(datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")] #PREPARE DATA TO PUSH [NEWTOKEN,NEW-TOKEN-EXPIRED-DATETIME]
			result_push = util.connectToPostgres("push",config['targethostname'],config['targetdatabase'],config['targetusername'],None,data_to_push,util.updateQueryWithColumn("cms.user", data_to_push, ['token', 'token_expired'], "user_id", login_result[0][2]))
			return jsonify({"username":username,"user_role":login_result[0][3], "user_id":login_result[0][2],"token": new_token})

@app.route('/api/v1/editContent', methods= ['POST'])
def editContent():
	headers = flask.request.headers
	bearer = headers.get('Authorization')
	token = bearer.split()[1]
	content_id = request.json['content_id']
	content = request.json['content']
	checkAuth = util.connectToPostgres('get',config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,util.query('checkAuthority',[token,content_id,'content_id','content'],None))
	if checkAuth == [] :
		return jsonify({"code":500,"status":"failed","message":"You have no permission to access this content"})
	else :
		data_to_push = [content]
		result_push = util.connectToPostgres("push",config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,util.updateQueryWithColumn('cms.content', data_to_push, ['content'],'content_id',content_id))
		return jsonify({"code":200,"status":"success","content_id":content_id,"content":content,"message":"Update content is success","message2":result_push})

@app.route('/api/v1/deleteContent', methods= ['DELETE'])
def deleteContent():
	headers = flask.request.headers
	bearer = headers.get('Authorization')
	token = bearer.split()[1]
	content_id = request.json['content_id']
	checkAuth = util.connectToPostgres('get',config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,util.query('checkAuthority',[token,content_id,'content_id','content'],None))
	if checkAuth == [] :
		return jsonify({"code":500,"status":"failed","message":"You have no permission to access this content"})
	else :
		result_delete = util.connectToPostgres("delete",config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,util.query('delete_data',['cms.content','content_id',content_id],None))
		return jsonify({"code":200,"status":"success","content_id":content_id,"message":"Delete content is success","message2":result_delete})

@app.route('/api/v1/editComment', methods= ['POST'])
def editComment():
	headers = flask.request.headers
	bearer = headers.get('Authorization')
	token = bearer.split()[1]
	comment_id = request.json['comment_id']
	comment = request.json['comment']
	checkAuth = util.connectToPostgres('get',config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,util.query('checkAuthority',[token,comment_id,'comment_id','comment'],None))
	if checkAuth == [] :
		return jsonify({"code":500,"status":"failed","message":"You have no permission to access this comment"})
	else :
		data_to_push = [comment]
		result_push = util.connectToPostgres("push",config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,util.updateQueryWithColumn('cms.comment', data_to_push, ['comment'],'comment_id',comment_id))
		return jsonify({"code":200,"status":"success","comment_id":comment_id,"comment":comment,"message":"Update comment is success","message2":result_push})

@app.route('/api/v1/deleteComment', methods= ['DELETE'])
def deleteComment():
	headers = flask.request.headers
	bearer = headers.get('Authorization')
	token = bearer.split()[1]
	comment_id = request.json['comment_id']
	checkAuth = util.connectToPostgres('get',config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,util.query('checkAuthority',[token,comment_id,'comment_id','comment'],None))
	if checkAuth == [] :
		return jsonify({"code":500,"status":"failed","message":"You have no permission to access this comment"})
	else :
		result_delete = util.connectToPostgres("delete",config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,util.query('delete_data',['cms.comment','comment_id',comment_id],None))
		return jsonify({"code":200,"status":"success","comment_id":comment_id,"message":"Delete comment is success","message2":result_delete})

app.run()