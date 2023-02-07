from app import db
from app.models.base import Base

class Predios(db.Model, Base):
	__tablename__ = 'predios'

	id = 	db.Column(db.Integer, primary_key=True)
	nome =	db.Column(db.String(255))
	ativo =	db.Column(db.Boolean)
	
	@classmethod
	def get(cls, ativo=False):
		predios =	cls.query.order_by(cls.ativo.desc(), cls.nome)

		if ativo:
			return predios.filter(cls.ativo==True).all()
		else:
			return predios.all()

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
	predio_ref = 	db.relationship('Predios', backref='quartos_ref')

	@classmethod
	def get(cls, ativo=False, compartilhado=False):
		quartos =	cls.query.join(Predios, Predios.id==cls.predio_id).order_by(cls.ativo.desc(), Predios.nome,
			cls.numero).filter(Predios.ativo==True)
		
		if compartilhado:
			quartos =	quartos.filter(cls.compartilhado==True)
		else:
			quartos =	quartos.filter(cls.compartilhado==False)

		if ativo:
			return quartos.filter(cls.ativo==True).all()
		else:
			return quartos.all()
	
