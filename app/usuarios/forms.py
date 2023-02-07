from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields import StringField, PasswordField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, Length, Optional
from app.usuarios.models import Usuarios, Cargos, UsuariosCargos
from werkzeug.security import generate_password_hash

class LoginForm(FlaskForm):
	usuario = 	StringField('Usuário', [DataRequired(message='Usuário é obrigatório')])
	senha = 	PasswordField('Senha', [DataRequired(message='Senha é obrigatória')])
	submit = 	SubmitField('Entrar')


class UsuarioForm(FlaskForm):
	nome =				StringField('Usuário', [DataRequired(message='Nome de usuário obrigatório')])
	senha =				PasswordField('Senha', [DataRequired(message='Nome de usuário obrigatório')])
	confirmar_senha =	PasswordField('Confirmar senha', [DataRequired(message='Nome de usuário obrigatório')])
	cargos =			SelectMultipleField('Cargos', choices=[], coerce=int)
	ativo =				BooleanField('Ativo', default='checked')
	submit =			SubmitField('Enviar')
	usuario =			None
	verificacao_senha =	True

	def __init__(self, id=None):
		super().__init__()
		self.cargos.choices =	list( map(lambda x: (x.id, x.descricao), Cargos.get_ativos()) )
		if id:
			self.usuario =			Usuarios.query.get(id)
			if not self.is_submitted():
				self.nome.data =		self.usuario.nome
				self.ativo.data =		self.usuario.ativo
				cargos_atuais = 		[]
				for cargo in self.usuario.usuarios_cargos_ref:
					cargos_atuais.append(cargo.cargos_ref.id)
				self.cargos.data =	cargos_atuais
	
	def salvar(self):
		if not self.usuario:
			self.usuario = Usuarios()
		self.usuario.nome =		self.nome.data
		self.usuario.ativo =	self.ativo.data
		if self.senha.data and self.senha.data == self.confirmar_senha.data:
			self.usuario.senha =	generate_password_hash(self.senha.data)
		else:
			self.verificacao_senha =	False
		if self.verificacao_senha:	
			if not self.usuario.id:
				self.usuario.criar()
			if self.cargos.data:
				usuario_cargos =	UsuariosCargos.query.filter(UsuariosCargos.usuarios_id==self.usuario.id).all()
				for cargo in usuario_cargos:
					cargo.deletar()
				for cargo in self.cargos.data:
					usuario_cargos =				UsuariosCargos()
					usuario_cargos.usuarios_id =	self.usuario.id
					usuario_cargos.cargos_id =		cargo
					usuario_cargos.criar()
			self.usuario.commit()


class CargoForm(FlaskForm):
	descricao =		StringField('Descrição', [DataRequired(message='Descrição do cargo obrigatória')])
	ativo =			BooleanField('Ativo', default='checked')
	submit =		SubmitField('Enviar')
	cargo = None

	def __init__(self, id=None):
		super().__init__()
		if id:
			self.cargo = 			Cargos.query.get(id)
			if not self.is_submitted():
				self.descricao.data =	self.cargo.descricao
				self.ativo.data =		self.cargo.ativo

	def salvar(self):
		if not self.cargo:
			self.cargo = Cargos()
		self.cargo.descricao =	self.descricao.data
		self.cargo.ativo =		self.ativo.data
		if not self.cargo.id:
			self.cargo.criar()
		self.cargo.commit()
