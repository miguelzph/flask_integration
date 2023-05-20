from flask import render_template, redirect, url_for, flash, request, Response, jsonify
from translate import Translator
from integracao_hotmart import app, database, bcrypt
from integracao_hotmart.forms import FormLogin, FormCriarConta, FormSearch
from integracao_hotmart.models import Usuario
from flask_login import login_user, logout_user, login_required
from flask_paginate import Pagination, get_page_args

from integracao_hotmart.aws_controller import db_get_items, db_put_item, db_get_items_by_query
from uuid import uuid4
from integracao_hotmart.static.constants import ALL_ACTIONS

@app.route('/', methods=['GET', 'POST'])  
def home():
    return render_template('home.html')


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/criarconta', methods=['GET', 'POST'])
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_crypt = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_crypt)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('login'))
    
    return render_template('criarconta.html', form_criarconta=form_criarconta)
        
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    traduzir = Translator(from_lang="English", to_lang="Portuguese")
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no E-mail: {form_login.email.data}', 'alert-success')
            # requests.arg pega todos os parametros da url (onde esse usuário acessou: perfil, usuários, etc)
            par_next = request.args.get('next')
            if par_next:
                return redirect((par_next))
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no Login. E-mail ou Senha Incorreto.', 'alert-danger')
    return render_template('login.html', form_login=form_login, traduzir=traduzir)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout Feito com Sucesso', 'alert-success')
    return redirect(url_for('home'))

@app.route('/reqs/<id_req>', methods=['GET'])
@login_required
def reqs(id_req):
    
    users = db_get_items_by_query('WebhookTable', 'id', id_req)

    return jsonify(users)


@app.route('/acoes', methods=['GET', 'POST'])
@login_required
def acoes():
    
    form_search = FormSearch()
    
    if request.method =='POST':
        search_value = form_search.search_field.data
        return redirect(url_for('acoes', search=search_value))
    
    email_to_search = request.args.get('search')
        
    if email_to_search:
        users = db_get_items_by_query('ActionsTable', 'email', email_to_search)
    else:
        users = db_get_items('ActionsTable')

    def get_users(users, offset=0, per_page=10):
        return users[offset: offset + per_page]
    
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(users)
    pagination_users = get_users(users, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    
    return render_template('acoes.html',
                           users=pagination_users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           form_search=form_search
                           )


def make_a_action(email, id_webook, action):
    
    print(ALL_ACTIONS[action]['message'].format(email=email))
    
    base_id = '{action}-' + id_webook
    
    action = ALL_ACTIONS[action]['name']
    
    official_id = base_id.format(action=action)
    
    action_payload = {
        "code_action-id_requisicao": official_id,
        "id_requisicao":id_webook,
        "email": email,
        "action": action,
        'description': ALL_ACTIONS[action]['description']
    }
    
    db_put_item(action_payload, 'ActionsTable')
    
    return None


def take_actions_from_status(payload):

    email = payload['email']

    if payload['status'] == 'aprovado':
        make_a_action(email, payload['id'], "send_email_welcome")
        make_a_action(email, payload['id'], "access_release")
        
    elif payload['status'] == 'recusado':
        make_a_action(email, payload['id'], "send_email_payment_declined")
        
    elif payload['status'] == 'reembolsado':
        make_a_action(email, payload['id'], "access_revoke")
    
    else:
        make_a_action(email, payload['id'], "unmapped_status")
        
    return None    

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.get_json()
    
    id_webook = str(uuid4())
    
    payload['id'] = id_webook
    
    # saving payload from webhook
    db_put_item(payload, 'WebhookTable')
    
    # take actions based on the payload
    take_actions_from_status(payload)
    
    return Response(status=204)