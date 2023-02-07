from app import db
#from sqlalchemy.ext.declarative import declared_att
from contextlib import contextmanager
from sqlalchemy import text, bindparam
from sqlalchemy.orm.exc import StaleDataError

@contextmanager
def session_scope():
	""" Contexto para commits das funções da tabela """

	try:
		yield db.session
		db.session.flush()
	except Exception as e:
		db.session.rollback()
		raise(e)

class Base(object):
	""" Base para criação do CRUD das models do banco """
	
	def criar(self):
		with session_scope() as s:
			s.add(self)

	def atualizar(self):
		with session_scope() as s:
			return

	def deletar(self):
		with session_scope() as s:
			s.delete(self)

	@classmethod
	def commit(cls):
		try:
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			raise(e)

	@classmethod
	def rollback(cls):
		db.session.rollback()

