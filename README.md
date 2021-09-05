# Crosswell_web_app

Crosswell web app

## Database

```bash
# This CMS using Postgres to run
# database name : crosswell
# database schema : cms
# database table : user,role,content,comment

#     -----------------------------
#    |           user              | 
#    |-----------------------------|
#    |   user_id (varchar)         | 
#    |   user_name (varchar)       | 
#    |   user_role (varchar)       |
#    |   date_created (timestamp)  |
#    |   token (varchar)           |
#    |   last_sign_in (timestamp)  |
#    |   token_expired (timestamp) |
#    |   email (varchar)           |
#    |   password (varchar)        |
#    |   status (varchar)          |
#     -----------------------------

#     ------------------------------
#    |             role             | 
#    |------------------------------|
#    |   role_id (varchar)          | 
#    |   role_description (varchar) | 
#     ------------------------------

#     -----------------------------
#    |          content            | 
#    |-----------------------------|
#    |   content_id (varchar)      | 
#    |   title (varchar)           | 
#    |   content (text)            |
#    |   user_id (varchar)         |
#    |   long (varchar)            |
#    |   lat (varchar)             |
#    |   image_path (varchar)      |
#    |   file (varchar)            |
#    |   date (timestamp)          |
#     -----------------------------

#     -----------------------------
#    |          comment            | 
#    |-----------------------------|
#    |   comment_id (varchar)      | 
#    |   comment (text)            |
#    |   user_id (varchar)         |
#    |   parent_id (varchar)       |
#    |   date (timestamp)          |
#     -----------------------------

# This git contains postgres dump file (contain database and several sample data) that can be used
# Restore the database :
psql crosswell < crosswell.dump 
```

## Build Setup for Front-End

``` bash
# FrontEnd configuration is inside :
./front/src/utils.js
# define Back-End base URL in BASE_URL parameter 

#go to frontend dir
cd ./front

# install dependencies
npm install

# serve with hot reload at localhost:8080 for development sake
npm run serve

#or you can specify your port
npm run serve -- --port=8004

# build for production
npm run build
# The HTML assets are built under dist folder


```


## Run Front-End in nginx server 

```bash
# for nginx server, copy all items inside ./dist folder to /var/www/html/{your_project_name}

#Copy these into your nginx conf under /etc/nginx/sites-enabled/
location /{your_project_name} {
          root "/var/www/html";
          try_files $uri $uri/ /index.html;
        }

#run your nginx server
service nginx start
```

## Back-End API
``` bash
#go to backend dir
cd ./back

#configuration file is inside :
./back/crosswell.cnf
#define/add Front-End URL inside ORIGINS key for enable CORS
#define database credentials in target key
#path key is the path for backend server save the external file from client side in absolute path fashion, you can specify your own path. Please make sure to the directory on this path is exist   

#run flask app with python3
python3 crosswell_api.py

#or you can run the app backside and kill the terminal *warning, please know what you do and how to stop the app before execute this
nohup python3 crosswell_api.py
```

