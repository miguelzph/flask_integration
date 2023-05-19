from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from integracao_hotmart.models import Usuario

import os
from dotenv import load_dotenv
load_dotenv()


class FormCriarConta(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    token = StringField('Token', validators=[DataRequired(), Length(6, 20)])
    botao_submit_criarconta = SubmitField('Criar Conta')

    #cria uma função com validate_ porque quando ele rodar o validate_on_submit() no routes também roda essa
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar.')
    
    def validate_token(self, token):
        if token.data != os.getenv("TOKEN_TO_CREATE_ACCOUNT"):
            raise ValidationError('Token inválido. Tente novamente, ou mande mensagem para o e-mail disponível na página de contato.')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login = SubmitField('Fazer Login')


class FormSearch(FlaskForm):
    search_field = StringField('E-mail')
    botao_submit_query = SubmitField('Pesquisar')