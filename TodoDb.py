from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/todos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 1. pip3 install Flask-Migrate
# 2. Add the folloing line to python file first
# 3. When setting up project for the first time, run "flask db init" in project folder to init necessary migration files
migrate = Migrate(app, db)