heroku create sethheightcollector

heroku addons:create heroku-postgresql:hobby-dev -
-app sethheightcollector

heroku config --app sethheightcollector

copy and paste database_url and add "?sslmode=require" to end of database uri string
