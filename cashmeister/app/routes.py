"""routes module
-- Home page route
"""

from app import app 

# decorator modifying the function that follows it 
# used to register functions as callbacks for particular events
# creating an association between url given as an argument and the function 
# when a web browser requests any of these urls, flask will invoke the function 
# and pass its value back to the browser as a response.

@app.route('/')
@app.route('/index')
def index(): 
    return "Hello, World" 

