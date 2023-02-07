from app import db
from app.models.base import Base
from werkzeug.security import check_password_hash
from flask_login import UserMixin


class Usuarios(db.Model, Base, UserMixin):
	__tablename__ = 'usuarios'
	
	id =		db.Column(db.Integer, primary_key=True)
	nome =		db.Column(db.String(255))
	senha =		db.Column(db.Text)
	ativo =		db.Column(db.Boolean)
	
	@classmethod
	def check_senha(cls, senha_db, senha):
		return check_password_hash(senha_db, senha)
	
	@classmethod
	def get(cls):
		return cls.query.order_by(cls.nome).all()


class Cargos(db.Model, Base):
	id =			db.Column(db.Integer, primary_key=True)
	descricao =		db.Column(db.Text)
	ativo =			db.Column(db.Boolean)
	
	@classmethod
	def get_ativos(cls):
		return cls.query.filter(cls.ativo==True).order_by(cls.descricao).all()
	
	@classmethod
	def get(cls):
		return cls.query.order_by(cls.descricao).all()


class UsuariosCargos(db.Model, Base):
	usuarios_id =	db.Column(db.ForeignKey(Usuarios.id), primary_key=True)
	cargos_id =		db.Column(db.ForeignKey(Cargos.id), primary_key=True)
	usuarios_ref =	db.relationship(Usuarios, backref='usuarios_cargos_ref')
	cargos_ref = 	db.relationship(Cargos, backref='usuarios_cargos_ref')

