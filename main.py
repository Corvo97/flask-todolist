# -- interno --
from telegram.telegram import sendBroadcast
from excecoes.excecoes import CampoEmBranco
from session.sessioncontrol import with_session
from gerenciadores.contas import cadastrar_usuario
from utilitarios.localizacao import get_city_from_ip
from gerenciadores.tarefas import adicionar_tarefa, deletar_tarefa
from utilitarios.utilitarios import trazer_usuario, trazer_dono_tarefa, formatar_prazo, Usuario

# -- externo --
import asyncio
from typing import Optional
from datetime import timedelta
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import Session, joinedload
from werkzeug.exceptions import HTTPException
from flask import Flask, render_template, redirect, url_for, request, Response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


# Configurações do Flask
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'palavrasupersecreta'
app.permanent_session_lifetime = timedelta(seconds = 28800)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager_message_category = 'info'


# Utilizado pelo sistema de login
@login_manager.user_loader
@with_session
def carregar_usuario(session: Session, id: int) -> Optional[Usuario]:
    return session.query(Usuario).options(joinedload(Usuario.tarefas)).filter_by(id = id).first()


@app.errorhandler(404)
def page_error_404(e: HTTPException) -> Response:
    return redirect('/')


@app.errorhandler(405)
def page_error_405(e: HTTPException) -> Response:
    return redirect('/login')


# Telegram webhook
@app.route('/webhook', methods = ['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode('utf-8'))])
    return '', 200


@app.route('/')
def index() -> Response:
    return render_template('index.html')


@app.route('/sistema')
@login_required
def sistema() -> Response:
    return render_template('sistema.html', user = current_user)


@app.route('/nova_tarefa', methods = ['POST'])
@login_required
def nova_tarefa() -> Response:
    try:
        titulo = request.form['titulo_tarefa']
        descricao = request.form['descricao_tarefa']
        data_prazo = request.form['prazo_data_tarefa']
        horario_prazo = request.form['prazo_horario_tarefa']

        # Verificar se os campos obrigatórios estão preenchidos
        if not (titulo and descricao and data_prazo and horario_prazo):
            raise CampoEmBranco

        # Formatação do prazo
        data_hora_prazo = formatar_prazo(data_prazo, horario_prazo)

        adicionar_tarefa(titulo, descricao, data_hora_prazo, current_user.id)
        return redirect('/sistema')
    except Exception as e:

        return render_template('erro.html', mensagem = str(e))


@app.route('/remover_tarefa/<int:tarefa_id>', methods = ['GET', 'POST'])
@login_required
def remover_tarefa(tarefa_id: int) -> Response:
    if current_user.id == trazer_dono_tarefa(tarefa_id):
        deletar_tarefa(tarefa_id)
        return redirect('/sistema')


@app.route('/registro', methods = ['GET', 'POST'])
async def registro() -> Response:
    if current_user.is_authenticated:
        return redirect('/sistema')
    if request.method == 'POST':
        usuario = request.form['usuario']
        email = request.form['email']
        senha = request.form['senha'] if request.form['senha'] == request.form['repetir_senha'] else False
        if not (usuario and email and senha):
            raise CampoEmBranco
        if senha:
            # cadastrar
            await cadastrar_usuario(usuario, senha, email)
            sendBroadcast(f'🟧 {usuario} acabou de se registrar! ({get_city_from_ip()}).')
            # Carregando usuário
            user = trazer_usuario(usuario)
            #logar
            login_user(user)
            return redirect(url_for('sistema'))

        return render_template('index.html')

    return render_template('registro.html')


@app.route('/login', methods = ['GET', 'POST'])
def login() -> Response:
    if current_user.is_authenticated:
        return redirect('/sistema')
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        # Carregando usuário
        user = trazer_usuario(usuario)

        if user and bcrypt.check_password_hash(user.senha, senha):
            # logar
            login_user(user)
            sendBroadcast(f'🟩 {usuario} acabou de fazer login no sistema ({get_city_from_ip()}).')
            return redirect(url_for('sistema'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout() -> Response:
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = '8000', debug = True)

