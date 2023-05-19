from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('MY_FLASK_SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_app.db'
	

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
# Quando o cara entrar em uma página que precisa estar logado ele será direcionado para o login (nome da função)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor faça login para acessar a página.'
login_manager.login_message_category = 'alert-info'


from integracao_hotmart import routes
