import app
from app import login_manager
from flask import current_app, url_for, Blueprint, render_template, redirect, session, abort
from flask_login import login_required, logout_user, login_user, current_user
from flask_principal import Identity, AnonymousIdentity, identity_loaded, RoleNeed, UserNeed, identity_changed
from app.usuarios.models import Usuarios
from app.usuarios.forms import LoginForm
from app import administrador, atendente, gerente, governanca

login_bp = Blueprint('login_bp', __name__, template_folder='templates', static_folder='static')

@login_bp.route('/', methods=['GET'])
def home():
	return redirect(url_for('login_bp.login'))

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
	try:
		if hasattr(current_user, "id"):
			return redirect(url_for('login_bp.index'))
	except Exception as e:
		raise(e)
	
	form = LoginForm()
	if form.validate_on_submit():
		usuario = 	form.usuario.data
		senha = 	form.senha.data
		user =		Usuarios.query.filter(Usuarios.nome==usuario).first()
		if not user:
			return render_template('login.html', title="Login", form=form, erro="Usuário inválido.")
		
		if not user.ativo:
			return render_template('login.html', title="Login", form=form, erro="Usuário inativo.")

		if Usuarios.check_senha(user.senha, senha):
			login_user(user)
			identity_changed.send(current_app._get_current_object(), identity=Identity(user.nome))
			return redirect( url_for('login_bp.index') )
		else:
			return render_template('login.html', title="Login", form=form, erro="Senha inválida.")
	return render_template('login.html', title="Login", form=form)

@login_bp.route('/logout', methods=['GET',])
@login_required
def logout():
	logout_user()
	identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
	return redirect( url_for('login_bp.login') )

@login_manager.user_loader
def load_user(user_id):
	if user_id:
		return Usuarios.query.get(user_id)
	return None

@identity_loaded.connect
def on_identity_loaded(sender, identity):
	identity_user =	current_user
	if hasattr(current_user, "nome"):
		identity.provides.add(UserNeed(current_user.nome))
		for cargo in current_user.usuarios_cargos_ref:
			identity.provides.add(RoleNeed(cargo.cargos_ref.descricao))
		session['nome'] = current_user.nome

@login_bp.route('/index', methods=['GET', ])
@login_required
def index():
	return render_template('dashboard.html',
		adm=administrador.can(), atendente=atendente.can(), gerente=gerente.can(), governanca=governanca.can(), usuario=current_user)

