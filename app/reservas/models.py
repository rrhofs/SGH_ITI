from app import db
from app.models.base import Base
from app.estrutura_predial.models import Quartos, Predios
from app.clientes.models import Clientes
from datetime import datetime, timedelta


class Conta(db.Model, Base):
	__tablename__ = 'conta'
	
	id =				db.Column(db.Integer, primary_key=True)
	valor =				db.Column(db.Float)
	desconto =			db.Column(db.Float)
	ativa =				db.Column(db.Boolean)
	fechada =			db.Column(db.Boolean)
	dt_abertura =		db.Column(db.DateTime)
	dt_fechamento =		db.Column(db.DateTime)
	cliente_id =		db.Column(db.ForeignKey(Clientes.cnpj_cpf))
	cliente_ref =		db.relationship(Clientes)

	@classmethod
	def em_aberto(cls, cliente_id=None):
		if cliente_id:
			return cls.query.filter(cls.fechada==False, cls.cliente_id==cliente_id)
		return cls.query.filter(cls.fechada==False)


class DetalhesConta(db.Model, Base):
	__tablename__ = 'detalhes_conta'

	id = 			db.Column(db.Integer, primary_key=True)
	conta_id =		db.Column(db.ForeignKey(Conta.id))
	quarto_id =		db.Column(db.ForeignKey(Quartos.id))
	dt_inicial =	db.Column(db.DateTime)
	dt_final =		db.Column(db.DateTime)
	nro_pessoas =	db.Column(db.Integer)
	quarto_ref =	db.relationship(Quartos)
	conta_ref =		db.relationship(Conta)


	@classmethod
	def remover_governanca(cls, governanca_id):
		detalhes_conta =	cls.query.get(governanca_id)
		if detalhes_conta:
			detalhes_conta.deletar()
			detalhes_conta.commit()
		

	@classmethod
	def remover_reserva(cls, reserva_id):
		detalhes_conta =	cls.query.get(reserva_id)
		if detalhes_conta:
			conta_id =		detalhes_conta.conta_id
			detalhes_conta.deletar()
			cls.set_valor_conta(conta_id)
			detalhes_conta.commit()
		

	@classmethod
	def get_governanca(cls):
		return cls.query.filter(cls.dt_inicial>=datetime.today(), cls.conta_id=='-1').all()

	@classmethod
	def get_reservas(cls):
		return cls.query.filter(cls.dt_inicial>=datetime.today(), cls.conta_id!='-1').all()

	@classmethod
	def quartos_ocupados(cls, dt_inicial, dt_final, quartos, nro_pessoas):
		sub =	cls.query.filter(db.or_(db.and_(cls.dt_inicial <= dt_inicial, cls.dt_final >= dt_inicial), 
			db.and_(cls.dt_inicial <= dt_final,cls.dt_final >= dt_final))).subquery()

		return Quartos.query.with_entities(Quartos.id, Predios.nome, Quartos.numero, Quartos.lotacao,
			Quartos.compartilhado, db.func.sum(cls.nro_pessoas).label('vagas_ocupadas')).join(sub,
			sub.c.quarto_id==Quartos.id, isouter=True).join(Conta, Conta.id==sub.c.conta_id, isouter=True).join(Predios,
			Predios.id==Quartos.predio_id).filter(Quartos.id.in_(quartos), Conta.ativa==True).group_by(Predios.nome,
			Quartos.numero, Quartos.lotacao, Quartos.id, Quartos.compartilhado).all()
	
	
	@classmethod
	def set_valor_conta(cls, conta_id):
		valor_detalhes =	cls.query.join(Quartos, Quartos.id==cls.quarto_id).with_entities(
			db.func.sum(Quartos.custo)).filter(cls.conta_id==conta_id).scalar()
		conta = 			Conta.query.get(conta_id)
		conta.valor =		valor_detalhes


	@classmethod
	def quartos_info(cls, dt_inicial, dt_final, quartos):
		sub =	cls.query.filter(db.or_(db.and_(cls.dt_inicial <= dt_inicial,cls.dt_final >= dt_inicial), 
			db.and_(cls.dt_inicial <= dt_final,cls.dt_final >= dt_final),
			db.and_(cls.dt_inicial >= dt_inicial, cls.dt_final <= dt_final))).subquery()
		return Quartos.query.with_entities(Quartos.id, Predios.nome, Quartos.numero, Quartos.lotacao, Quartos.qt_banheiros,
			Quartos.cozinha, Quartos.compartilhado, Quartos.custo, db.func.sum(sub.c.nro_pessoas).label('vagas_ocupadas')).join(
			sub, sub.c.quarto_id==Quartos.id, isouter=True).join(Conta, Conta.id==sub.c.conta_id, isouter=True).join(Predios,
			Predios.id==Quartos.predio_id).filter(Quartos.id.in_(quartos), Quartos.ativo==True).group_by(Quartos.id,
			Predios.nome, Quartos.numero, Quartos.lotacao, Quartos.qt_banheiros, Quartos.cozinha, Quartos.compartilhado,
			Quartos.custo).order_by(Predios.nome, Quartos.numero).all()

