# Flask-python-redis


To use with SQLite uncomment line 16 of __init__.py and comment line 15
Run pip install -r requirements.txt to install all the necessary tools.

I used redis in localhost, since Heroku tools for redis and memcache are free but need of a credit card number registered on the platform.

https://sheltered-beyond-98420.herokuapp.com
This is the api that can be tested with Postgresql.

List of requests and calls accepted.
----------------------------

Welcome message.
Request:
		
		GET http://localhost:5000

Response: Welcome to the API!

Full list of users (cached)
Request 

		GET http://localhost:5000/usersv

Response:

		[
			{
				"email": "rosa@gmail.com",
				"firstname": "Rosa",
				"id": 1,
				"lastname": "Gomez",
				"username": "rosita"
			}
		]
		
User Details:
Request:

		GET http://localhost:5000/user/<id>
		
Response: 
	{
  "email": "rosa@gmail.com",
  "firstname": "Rosa",
  "id": 1,
  "lastname": "Gomez",
  "username": "rosita"
}

Edit User:
Request:

		POST http://localhost:5000/user/1
		Content-Type: application/json

		{
			"email": "rosa_edited@gmail.com",
			"firstname": "Rosa",
			"id": 1,
			"lastname": "Gomez",
			"username": "rosita"
		}

Response: 

		{
			"email": "rosa_edited@gmail.com",
			"firstname": "Rosa",
			"id": 1,
			"lastname": "Gomez",
			"username": "rosita"
		}

Add New User:
Request:

		POST http://localhost:5000/user/add
		Content-Type: application/json

		{
				"firstname":"Segundo",
				"lastname": "Usuario",
				"username":"usuario2",
				"email": "u2@gmail.com",
				"password": "admin1234"
		}	
		
Response:

	{
    "email": "u2@gmail.com",
    "firstname": "Segundo",
    "id": 4,
    "lastname": "Usuario",
    "username": "usuario2"
  }
  
List of users with filter and pagination:
Request:
  
    POST http://localhost:5000/users
    Content-Type: application/json

    {
      "PAGE_NUMBER": 1,
      "ROWS_PER_PAGE": 10
    }
Parameters allowed:

    {
      "PAGE_NUMBER": NUMBER,
      "ROWS_PER_PAGE": NUMBER,
      "username": STRING,
      "firstname": STRING,
      "lastname": STRING,
      "email": STRING
    }

Response:

    [
      {
        "email": "rosa_edited@gmail.com",
        "firstname": "Rosa",
        "id": 1,
        "lastname": "Gomez",
        "username": "rosita"
      },
      {
        "email": "u2@gmail.com",
        "firstname": "Segundo",
        "id": 4,
        "lastname": "Usuario",
        "username": "usuario2"
      }
    ]
    
Change Password:
Request:

    POST http://localhost:5000/user/changepsw/1
    Content-Type: application/json

    {
        "password": "edited second time"
    }

Response: Password Changed

Delete user:
Request

    DELETE http://localhost:5000/user/1

Response: Deleted

# To test it in Heroku

> git init

> git add .

> git commit -m 'initial commit'

> heroku create

> heroku config:set FLASK_APP=users_api

> heroku config:set SECRET_KEY="`< /dev/urandom tr -dc 'a-zA-Z0-9' | head -c16`"

> heroku addons:create heroku-postgresql:hobby-dev
(once you get a free postgress db open the dashboard > Features > Postgres Db and look for the URL, it's important to change the start of the url from postgres:// to postgresql:// when replacing the config url)

> git push heroku master

> heroku ps
(check that the Procfile was recognized correctly, it needs to be at the root folder)

> heroku ps:scale web=1

> heroku open

https://elements.heroku.com/addons/rediscloud
