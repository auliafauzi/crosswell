# Crosswell_web_app

Crosswell web app

## Build Setup for front-end

``` bash
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
# for nginx server, copy all items inside ./dist folder to /var/www/html/{your_project_name}

#Copy these into your nginx conf under /etc/nginx/sites-enabled/
location /{your_project_name} {
          root "/var/www/html";
          try_files $uri $uri/ /index.html;
        }

```

## Run backend API
``` bash
#go to backend dir
cd ./back

#run flask app with python3
python3 crosswell_api.py

#or you can run the app backside mad kill the terminal *warning, please know what you do and how to stop the app before execute this
nohup python3 crosswell_api.py
```

``` bash
API url is defined at ./src/utils.js file, on BASE_URL variable
```
