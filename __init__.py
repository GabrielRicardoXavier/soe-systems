### importar ###
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

### App e/ou Site ###
app = Flask(__name__)

app.config['SECRET_KEY'] = '014e2b358d00cda36c9ac55e8c979eeb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///saie.db'
app.config['UPLOAD_FOLDER'] = 'C:/Users/USER/PycharmProjects/MeuSite/saie/static/foto_alunos'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Faça Login ou Crie uma Conta para Acessar essa Página'
login_manager.login_message_category = 'alert-info'

