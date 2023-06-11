from flask import Flask
from flask_bcrypt import Bcrypt

MAX_CONTENT_LENGTH = 2048 * 2048

app = Flask(__name__)
app.secret_key = '432bhg432@3bh$'

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '4g3uyg42YUG43'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

from routes import *

from models import Users

from models import Products

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
