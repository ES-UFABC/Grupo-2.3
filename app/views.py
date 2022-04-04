from flask import url_for, redirect, render_template, flash, g, session
from flask_login import login_user, logout_user, current_user, login_required
from app import app, login_manager
from app.forms import CreateUserForm, LoginForm
from app.models import User
from app import db, bcrypt
from app.scripts.adicionar_hotel import adicionar_hotel, listar_hoteis, editar_hotel, deletar_hotel
from app.scripts.ocupacao_quartos import adicionar_quarto, ocupacao_quartos, editar_quarto, deletar_quarto


@app.route('/')
def pagina_inicial():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('lista_hotel'))
    return render_template('index.html')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# @app.route('/list/')
# def posts():
# 	return render_template('list.html')


@app.route('/new/')
@login_required
def new():
	form = CreateUserForm()
	return render_template('new.html', form=form)


@app.route('/save/', methods = ['GET','POST'])
#@login_required
def save():
    form = CreateUserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('E-mail já possui cadastrado.', 'danger')
            return redirect('/new')
        else:
            name = form.name.data
            email = form.email.data
            pwd = bcrypt.generate_password_hash(form.password.data)
            admin = User(name=name, password=pwd, profile='admin', email=email, password_confirmation=pwd)
            db.session.add(admin)
            db.session.commit()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect('/new')

    return render_template('new.html', form=form)


# @app.route('/view/<id>/')
# def view(id):
# 	return render_template('view.html')

# # === User login methods ===

@app.before_request
def before_request():
    g.user = current_user

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('new'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for("lista_hotel"))
            else:
                flash('Senha inválida. Tente novamente', 'danger')
                return redirect('/login')
        else:
            flash('E-mail não encontrado.', 'danger')
            return redirect('/login')

    return render_template('login.html', 
        title = 'Sign In',
        form = form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('pagina_inicial'))


@app.route('/adicionar-hotel/', methods=['GET', 'POST'])
@login_required
def adicionar_hotel_endpoint():
    user_id = g.user.get_id()
    return adicionar_hotel(user_id)


@app.route('/lista-hotel/')
@login_required
def lista_hotel():
    user_id = g.user.get_id()
    return listar_hoteis(user_id)


@app.route('/editar-hotel/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_hotel_endpoint(id):
    user_id = g.user.get_id()
    return editar_hotel(id, user_id)


@app.route('/deletar-hotel/<int:id>')
@login_required
def deletar_hotel_endpoint(id):
    user_id = g.user.get_id()
    return deletar_hotel(id, user_id)


@app.route('/adicionar-quarto/', methods=['GET', 'POST'])
@login_required
def adicionar_quarto_endpoint():
    user_id = g.user.get_id()
    return adicionar_quarto(user_id)


@app.route('/ocupacao-quartos/<int:id>')
@login_required
def ocupacao_quartos_endpoint(id):
    user_id = g.user.get_id()
    return ocupacao_quartos(id, user_id)


@app.route('/deletar-quarto/<int:id>')
@login_required
def deletar_quarto_endpoint(id):
    user_id = g.user.get_id()
    return deletar_quarto(id, user_id)


@app.route('/editar-quarto/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_quarto_endpoint(id):
    user_id = g.user.get_id()
    return editar_quarto(id, user_id)

@app.route('/adicionar-reserva/', methods=['GET', 'POST'])
@login_required
def adicionar_reserva_endpoint():
    user_id = g.user.get_id()
    return adicionar_quarto(user_id)
