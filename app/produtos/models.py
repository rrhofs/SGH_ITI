from app import db
from app.models.base import Base

class Predios(db.Model, Base):
	__tablename__ = 'predios'

	id = 	db.Column(db.Integer, primary_key=True)
	nome =	db.Column(db.String(255))
	ativo =	db.Column(db.Boolean)
	
	@classmethod
	def get(cls):
		return cls.query.all()

class Quartos(db.Model, Base):
	__tablename__ = 'quartos'
	
	id =			db.Column(db.Integer, primary_key=True)
	numero =		db.Column(db.String(255))
	predio_id =		db.Column(db.ForeignKey(Predios.id))
	qt_banheiros =	db.Column(db.Integer)
	lotacao =		db.Column(db.Integer)
	cozinha =		db.Column(db.Boolean)
	custo =			db.Column(db.Float)
	compartilhado =	db.Column(db.Boolean)
	ativo =			db.Column(db.Boolean)
	predio_ref = 	db.relationship('Predios')

