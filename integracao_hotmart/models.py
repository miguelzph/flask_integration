from integracao_hotmart import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader  #diz que essa função é a função que carrega(encontra) o usuário
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))  #pode usar o get porque o id é a chave primária


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)  # primary_key --> cria automaticamente um id
    username = database.Column(database.String, nullable=False)  # nullable --> esse campo não pode estar vazio
    email = database.Column(database.String, nullable=False, unique=True)  # unique --> o email só pode ser cadastrado uma vez
    senha = database.Column(database.String, nullable=False)
