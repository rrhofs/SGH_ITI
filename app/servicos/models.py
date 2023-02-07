from app import db
from app.models.base import Base

class Servicos(db.Models, Base):
	id = 			db.Column(db.Integer, primary_key=True)
	descricao = 	db.Column(db.Text)
	custo =			db.Column(db.Float)
	desconto =		db.Column(db.Float)
	ativo =			db.Column(db.Boolean)

