import datetime
from datetime import datetime as dt
from sqlalchemy import Column, Integer, DateTime
from flask import Flask, render_template, url_for, redirect, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import select

import operator



from werkzeug.utils import secure_filename
import os



# see http://bootswatch.com/3/ for available swatches
app = Flask(__name__, static_folder='static') 
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

login_manager = LoginManager(app)

bcrypt = Bcrypt(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\267473\\DB Browser for SQLite\\site.db'

app.config['SECRET_KEY'] = 'this is a secret key'

app.config['SQLALCHEMY_ECHO'] = True

# end of new line
admin = Admin()
db = SQLAlchemy(app)

admin.init_app(app)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class User(db.Model, UserMixin):

   __tablename__ = "user"

   id = db.Column(db.Integer, primary_key=True)

   username = db.Column(db.String(50))

   email = db.Column(db.String(120), unique=True, nullable=False)

   password = db.Column(db.String(100), nullable=False)

   def __repr__(self):

       return f'<User {self.username}>'

class Client(db.Model, UserMixin):

   __tablename__ = "client"

   id = db.Column(db.Integer, primary_key=True)

   username = db.Column(db.String(20), unique=True, nullable=False)

   email = db.Column(db.String(80), nullable=False)

   password = db.Column(db.String(80), nullable=False)

   def __str__(self):

       return self.username

@login_manager.user_loader

def load_user(user_id):

   return User.query.get(int(user_id))

class Menu(db.Model):

   __tablename__ = "menu"

   menu_id = db.Column(db.Integer, primary_key=True)

   menu_name = db.Column(db.Unicode(64))

   menu_price = db.Column(db.Numeric(10, 2), nullable=False)

   menu_type = db.Column(db.String(30), nullable=False)

   path = db.Column(db.Unicode(128))

   basket = relationship("Basket", back_populates="menu")

   def __unicode__(self):

       return f'<Menu {self.menu_name}>'

@login_manager.user_loader

def load_menu(menu_id):

   return Menu.query.get(int(menu_id))

class Basket(db.Model):

   __tablename__ = 'basket'

   basket_id = db.Column(db.Integer, primary_key=True)

   basket_name = db.Column(db.String(20), nullable=False)

   quantity = db.Column(db.Integer, nullable=False)

   menu_id = db.Column(db.Integer, db.ForeignKey('menu.menu_id'), nullable=False)

   menu = relationship("Menu", back_populates="basket")  # 2nd backpopulates method

   def __unicode__(self):

       return f'<BasketItem {self.basket_name}>'

if __name__ == '__main__':

   with app.app_context():

       db.create_all()

   app.run(debug=True)