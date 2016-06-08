# swpp-server
Data server app for ScentedWidgetPP chrome extension.

Currently deployed to [Heroku] (https://swpp-server-stage.herokuapp.com/)

Local set up \(recommended with virtualenv+wrapper\). Assuming you have an empty postgresql database named swpp-server\:
  1. `cd` into swpp-server and run the following in terminal
  2. `pip install -r requirements.txt` \(Python-3.5.1\)
  3. `python manage.py db upgrade`
  4. `export APP_SETTINGS="config.DevelopmentConfig"`
  5. `export DATABASE_URL="postgresql://localhost/swpp-server"`
  6. `python app.py' to start the server at '127.0.0.1:5000`

Send a json to `http://localhost:5000/send` (i.e: `curl -H \"Content-type: application/json\" -X POST http://127.0.0.1:5000/send -d \'{"message":"Hello!"}`)

View the last message received at `http://localhost:5000`