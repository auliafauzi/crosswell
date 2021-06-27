import flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin
import time 
import os
import json
import re
from datetime import datetime
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
	contentList = util.connectToPostgres('get',config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,util.query('contentList',None, None))
	for i in contentList :
		zipped = dict(zip(util.data_structure['content'], i))
		result.append(zipped)
	return jsonify({"message":result,"code":200})

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


@app.route('/api/v1/postContent/<string:user_id>', methods= ['POST'])
def postContet(user_id):
	# methods1 = 'get'
	# query1 = "select content_id from cms.content"
	# maxnum = util.getMax(util.connectToPostgres(methods1,config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,query1))
	# new_content_id = "p" + str(int(maxnum[0])+1)
	new_content_id = "p" + str(util.connectToPostgres('get',config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,util.query('next_id','content_id','content'))[0][0])
	###
	context = request.get_data()
	title = request.form['title']
	content = request.form['content']
	longitude = request.form['longitude']
	latitude = request.form['latitude']
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

@app.route('/api/v1/postComment/<string:user_id>/<string:parent_id>', methods= ['POST'])
def postComment(user_id, parent_id):
	# context = request.get_data()
	# comment = request.form['comment']
	comment = request.json['comment']
	print(comment)
	new_coment_id = "c" + str(util.connectToPostgres('get',config['targethostname'],config['targetdatabase'],config['targetusername'],None,None,util.query('next_id','comment_id','comment'))[0][0])
	new_comment = [new_coment_id, comment, user_id, parent_id,datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
	result_push = util.connectToPostgres("push",config['targethostname'],config['targetdatabase'],config['targetusername'],None,new_comment,util.insertQuery("cms.comment", new_comment))
	return jsonify({"new_coment_id":new_coment_id,"comment":comment,"new_comment":new_comment,"result_push":result_push,"code":200})



app.run()