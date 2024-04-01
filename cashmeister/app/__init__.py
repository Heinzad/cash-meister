"""init
-- Flask Application Instance 
""" 

from flask import Flask


app = Flask(__name__)


# avoid circular imports by placing at end of script
from app import routes
