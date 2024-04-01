"""init
-- Flask Application Instance 

""" 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 

from config import Config 

#Create the application object as an instance of class Flask 
#imported from the flask package

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# avoid circular imports by placing at end of script
from app import routes, models
