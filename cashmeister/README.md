Cash Meister
============ 



# 0. Introduction

This project adapts the flask microblog approach developed in: 

Grinberg, Miguel (2024), [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)


## Setup Virtual Environment 

Setup virtual environment: 

```
python -m venv .venv
```


Apply a Powershell execution policy: 

```
Set-ExecutionPolicy Unrestricted -Scope Process
``` 

Activate the virtual environment in PowerShell by running: 

```
.venv\Scripts\Activate.ps1
```

Optional: relaunch from inside the virtual environment: 
```
code .
```



# 3. Database 

This section utilises: 

Grinberg, Miguel (2024), [Flask Mega-Tutorial, Part IV: Database](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database)


### Add flask extensions to requirements: 
- flask-sqlalchemy: a flask wrapper for the SQLAlchemy orm.
- flask-migrate: a flask wrapper for Alembic, a database migration framework for SQLAlchemy

```
#requirements/common.txt 
(venv) $ pip install flask-sqlalchemy 
(venv) $ pip install flask-migrate
```


### Upgrade the Config Class: 

An empty database file was created as `cashmeister.sqlite`. 
The .env file SQLALCHEMY_DATABASE_URI concatenated 'sqlite///' + the full filepath. 

```python
"""config.py"""
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
```

### Initialise flask-sqlalchemy and flask-migrate: 

Added objects: 
- `db`: represents the database engine
- `migrate`: represents the database migration engine 

```python
"""app/__init__.py"""
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
``` 

### Define a users table: 

Represents users stored in the database
The username and email fields are defined as strings. 
User passwords are not stored as plain text bust as hashes. 

```python 
"""app/models.py"""
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)
```

The `sqlalchemy` module provides database functions and classes while `sqlalchemy.orm` supports models.
The db instance and the Optional typing hint are also imported. 

_Grinsberg:_ 

    Fields are assigned a type using Python type hints, wrapped with SQLAlchemy's so.Mapped generic type. 
    - A type declaration such as so.Mapped[int] or so.Mapped[str] defines the type of the column, and also makes values required, or non-nullable in database terms. 
    - To define a column that is allowed to be empty or nullable, the Optional helper from Python is also added, as password_hash demonstrates.
    - In most cases defining a table column requires more than the column type. SQLAlchemy uses a so.mapped_column() function call assigned to each column to provide this additional configuration.
    - The __repr__ method tells Python how to print objects of this class


### Define a directories table: 

This was modified from the `posts` table given in the reference. 

```python 
"""app/models.py"""
from datetime import datetime, timezone 
# ... 
class Directories(db.Model): 
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # ... 
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),index=True)
    author: so.Mapped[User] = so.relationship(back_populates='directories')

    def __repr__(self): 
        return f"Directory {self.financial_year}:{self.category}>" 
``` 

_Grinsberg:_ 

    - The timestamp field is defined with a datetime type hint and is configured to be indexed (to efficiently retrieve posts in chronological order), and a default argument passing a lambda function that returns the current time in the UTC timezone. 
    - The user_id field was initialized as a foreign key to User.id, which means that it references values from the id column in the users table.
    - The User class has a new posts field, that is initialized with so.relationship(). This is not an actual database field, but a high-level view of the relationship between users and posts, and for that reason it isn't in the database diagram. 
    - the Post class has an author field that is also initialized as a relationship. 


## Database Migrations 

Initialise the migrations directory: 
```
(venv) $ flask db init
```

Generate the migration scripts: 
```
(venv) $ flask db migrate -m "users table"
```

Apply the changes to the database: 
```
(venv) $ flask db upgrade
```


## Database Checking 

Quick checks to ensure the database is working: 

```python 
import sqlalchemy as sa

from app import app, db
from app.models import User, Directories

# access the application concept 
app.app_context().push() 


# post a user
u = User(username='john', email='john@example.com')
db.session.add(u) 
db.session.commit() 

u = User(username='susan', email='susan@example.com')
db.session.add(u) 
db.session.commit() 


# query using a results iterator 
qry = sa.select(User)
users = db.session.scalars(qry).all()

for u in users: 
    print(u.user_id, u.username) 


# retrieve a user from their id 
u = db.session.get(User, 1)
print(u)


# post directories  
u = db.session.get(User, 1) 
d = Directories(
    financial_year= '2004', 
    category='banking',
    description='bank statements',
    filepath='/b2024', 
    author=u
) 
db.session.add(d) 
db.session.commit()
 

d = Directories(
    financial_year= '2004', 
    category='payables',
    description='Accounts Payable',
    filepath='p2024', 
    author=u
)
db.session.add(d) 
db.session.commit() 


d = Directories(
    financial_year= '2004', 
    category='receivables',
    description='Accounts Receivable',
    filepath='r2024', 
    author=u
)
db.session.add(d) 
db.session.commit()

```

## Database Cleanup 

