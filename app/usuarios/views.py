import app
from app import login_manager
from flask import current_app, url_for, Blueprint, render_template, redirect, session, abort
from flask_login import login_required, logout_user, login_user, current_user
from flask_principal import Identity, AnonymousIdentity, identity_loaded, RoleNeed, UserNeed, identity_changed
from app.usuarios.models import Usuarios, Cargos
from app.usuarios.forms import UsuarioForm, CargoForm
from app import administrador, atendente, gerente, governanca

usuarios_bp = Blueprint('usuarios_bp', __name__, template_folder='templates', static_folder='static', url_prefix='/usuarios')
cargos_bp = Blueprint('cargos_bp', __name__, template_folder='templates', static_folder='static', url_prefix='/cargos')

@usuarios_bp.route('/dashboard', methods=['GET',])
def usuarios():
	
	usuarios =	Usuarios.get()

	return render_template('lista_usuarios.html', title="Usuários", usuarios=usuarios,
		adm=administrador.can(), atendente=atendente.can(), gerente=gerente.can(), governanca=governanca.can(), usuario=current_user)

@usuarios_bp.route('/adicionar', methods=['GET', 'POST'])
@usuarios_bp.route('/editar/<id>', methods=['GET', 'POST'])
def editar_usuarios(id=None):
	
	form =	UsuarioForm(id)
	aviso = None
	if form.validate_on_submit():
		form.salvar()
		if not form.verificacao_senha:
			aviso =	'Senha e Confirmar senha não coincidem. Por favor tente novamente.'
			return render_template('editar_usuarios.html', title='Editar usuário', form=form, aviso=aviso,
				adm=administrador.can(), atendente=atendente.can(), gerente=gerente.can(), governanca=governanca.can(), usuario=current_user)
		
		return redirect( url_for('usuarios_bp.usuarios') )
	
	return render_template('editar_usuarios.html', title='Editar usuário', form=form,
		adm=administrador.can(), atendente=atendente.can(), gerente=gerente.can(), governanca=governanca.can(), usuario=current_user)

@cargos_bp.route('/dashboard', methods=['GET',])
def cargos():
	
	cargos =	Cargos.get()

	return render_template('lista_cargos.html', title="Usuários", cargos=cargos,
		adm=administrador.can(), atendente=atendente.can(), gerente=gerente.can(), governanca=governanca.can(), usuario=current_user)

@cargos_bp.route('/adicionar', methods=['GET', 'POST'])
@cargos_bp.route('/editar/<id>', methods=['GET', 'POST'])
def editar_cargos(id=None):
	
	form =	CargoForm(id)
	
	if form.validate_on_submit():
		form.salvar()
		return redirect( url_for('cargos_bp.cargos') )
	
	return render_template('editar_cargos.html', title='Editar usuário', form=form,
		adm=administrador.can(), atendente=atendente.can(), gerente=gerente.can(), governanca=governanca.can(), usuario=current_user)
