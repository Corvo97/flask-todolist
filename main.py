# -- interno --
from db.db_tools import get_user
from classes.user_class import User
from session.session import with_session
from controls.user_control import user_add
from exceptions.exceptions import FieldCannotBeEmpty
from controls.task_control import task_create, task_remove
from utilities.utilities import get_task_owner, format_due_date

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
app.config['SECRET_KEY'] = 'palavramuitocomplexaequedevesermantidaemsegredo2025'
app.permanent_session_lifetime = timedelta(seconds = 28800)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager_message_category = 'info'


# Utilizado pelo sistema de login
@login_manager.user_loader
@with_session
def load_user(session: Session, id: int) -> Optional[User]:
    return session.query(User).options(joinedload(User.tasks)).filter_by(id = id).first()


@app.errorhandler(404)
def page_error_404(e: HTTPException) -> Response:
    return redirect('/')


@app.errorhandler(405)
def page_error_405(e: HTTPException) -> Response:
    return redirect('/login')


@app.route('/')
def index() -> Response:
    return render_template('index.html')


@app.route('/system')
@login_required
def system() -> Response:
    return render_template('system.html', user = current_user)


@app.route('/new_task', methods = ['POST'])
@login_required
def new_task() -> Response:
    #try:
    title = request.form['task_title']
    description = request.form['task_description']
    due_date = request.form['task_due_date']
    due_time = request.form['task_due_time']

    # Verificar se os campos obrigatórios estão preenchidos
    if not (title and description and due_date and due_time):
        raise FieldCannotBeEmpty

    # Formatação do prazo
    date_time_due = format_due_date(due_date, due_time)
    task_create(title, description, date_time_due, current_user.id)
    return redirect('/system')
    #except Exception as e:

        #return render_template('error.html', mensagem = str(e))


@app.route('/remove_task/<int:task_id>', methods = ['GET', 'POST'])
@login_required
def remove_task(task_id: int) -> Response:
    if current_user.id == get_task_owner(task_id):
        task_remove(task_id)
        return redirect('/system')


@app.route('/register', methods = ['GET', 'POST'])
async def registro() -> Response:
    if current_user.is_authenticated:
        return redirect('/system')
    if request.method == 'POST':
        user = request.form['user']
        email = request.form['email']
        password = request.form['password'] if request.form['password'] == request.form['repeat_password'] else False
        if not (user and email and password):
            raise FieldCannotBeEmpty
        if password:
            # cadastrar
            await user_add(user.title(), password, email)
            # Carregando usuário
            user = get_user(email)
            #logar
            login_user(user)
            return redirect(url_for('system'))

        return render_template('index.html')

    return render_template('register.html')


@app.route('/login', methods = ['GET', 'POST'])
def login() -> Response:
    if current_user.is_authenticated:
        return redirect('/system')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Carregando usuário
        user = get_user(email)

        if user and bcrypt.check_password_hash(user.password, password):
            # logar
            login_user(user)
            return redirect(url_for('system'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout() -> Response:
    logout_user()
    return redirect(url_for('login'))

