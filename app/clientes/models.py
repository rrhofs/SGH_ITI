from app import db
from app.models.base import Base
from app.estrutura_predial.models import Quartos


class Clientes(db.Model, Base):
	__tablename__ = 'clientes'

	cnpj_cpf =		db.Column(db.String(14), primary_key=True)
	nome =			db.Column(db.String(255))
	cep =			db.Column(db.String(8))
	logradouro =	db.Column(db.Text)
	numero =		db.Column(db.Text)
	complemento =	db.Column(db.Text)
	telefone =		db.Column(db.String(11))
	email =			db.Column(db.Text)
	ativo =			db.Column(db.Boolean)
	
	@classmethod
	def get(cls, ativo=False, termo=None):
		if ativo and termo:
			return cls.query.filter(cls.ativo==True, cls.nome.ilike(termo+'%'), cls.cnpj_cpf!='-1').all()
		elif ativo and not termo:
			return cls.query.filter(cls.ativo==True, cls.cnpj_cpf!='-1').all()
		elif not ativo and termo:
			return cls.query.filter(cls.nome.ilike(termo+'%'), cls.cnpj_cpf!='-1').all()
		else:
			return cls.query.filter(cls.cnpj_cpf!='-1').all()
			
