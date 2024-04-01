"""routes module
-- Home page route
"""

from flask import render_template, flash, redirect, url_for
from app import app 
from app.forms import LoginForm

# decorator modifying the function that follows it 
# used to register functions as callbacks for particular events
# creating an association between url given as an argument and the function 
# when a web browser requests any of these urls, flask will invoke the function 
# and pass its value back to the browser as a response.

# index view function 

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Adminator'}
    directories = [
        {
            'financial_year': 2004,
            'category': 'banking', 
            'description': 'bank statements',
            'filepath': '/cash_meister/banking/b2024'
        }, 
        {
            'financial_year': 2024,
            'category': 'receivables', 
            'description': 'accounts receivable',
            'filepath': '/cash_meister/receivables/r2024'
        }, 
        {
            'financial_year': 2024,
            'category': 'payables', 
            'description': 'accounts payable', 
            'filepath': '/cash_meister/payables/p2024'
        }
    ]
    return render_template('index.html', title='Home', user=user, directories=directories)

# login view function 

@app.route('/login', methods=['GET', 'POST'])
def login(): 
    form = LoginForm()
    if form.validate_on_submit(): 
        flash(f"Login requested for user {form.username.data}, remember_me={form.remember_me.data}")
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form) 
