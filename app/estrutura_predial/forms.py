from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields import StringField, BooleanField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length, Email, NumberRange, Optional
from app.estrutura_predial.models import Predios, Quartos


class AtivoForm(FlaskForm):
	ativo = BooleanField('Exibir somente ativos')
	
	def __init__(self):
		super().__init__()
		if not self.is_submitted():
			self.ativo.data = 'checked'
		

class PredioForm(FlaskForm):
	nome =			StringField('Prédio', validators=[Length(max=255)])
	ativo =			BooleanField('Ativo', default='checked')
	submit =		SubmitField('Salvar')
	predio =		None

	def __init__(self, id):
		super().__init__()

		if id:
			self.predio = Predios.query.get(id)
			if not self.is_submitted():
				self.nome.data = self.predio.nome
				self.ativo.data = self.predio.ativo
	
	def salvar(self):
		if not self.predio:
			self.predio =	Predios()
		
		self.predio.nome =	self.nome.data
		self.predio.ativo =	self.ativo.data
		if not self.predio.id:
			self.predio.criar()
		self.predio.commit()


class QuartoForm(FlaskForm):
	numero =		StringField('Quarto', validators=[Length(max=255)])
	predio =		SelectField('Prédio', choices=[], coerce=int, validators=[Optional()])
	qt_banheiros =	IntegerField('Qtde de banheiros')
	lotacao =		IntegerField('Lotação máxima')
	custo =			DecimalField('Valor da diária')
	cozinha =		SelectField('Possui cozinha', choices=[(1, 'Sim'), (0, 'Não')], coerce=int)
	compartilhado =	SelectField('Quarto compartilhado', choices=[(1, 'Sim'), (0, 'Não')], coerce=int)
	ativo =			BooleanField('Ativo', default='checked')
	submit =		SubmitField('Salvar')
	quarto =		None

	def __init__(self, id):
		super().__init__()
		
		predios = Predios.query.with_entities(Predios.id, Predios.nome).filter(
			Predios.ativo==True).order_by(Predios.nome).all()
		escolhas_predios = list( map(lambda x: (x.id, x.nome), predios) )
		self.predio.choices = escolhas_predios

		if id:
			self.quarto =	Quartos.query.get(id)
			if not self.is_submitted():
				self.numero.data =			self.quarto.numero
				self.predio.data =			self.quarto.predio_id
				self.qt_banheiros.data =	self.quarto.qt_banheiros
				self.lotacao.data =			self.quarto.lotacao
				self.custo.data =			self.quarto.custo
				self.cozinha.data =			self.quarto.cozinha
				self.compartilhado.data =	self.quarto.compartilhado
				self.ativo.data =			self.quarto.ativo
	
	def salvar(self):
		if not self.quarto:
			self.quarto =	Quartos()

		self.quarto.numero =		self.numero.data
		self.quarto.qt_banheiros =	self.qt_banheiros.data
		self.quarto.lotacao =		self.lotacao.data
		self.quarto.cozinha =		True if self.cozinha.data else False
		self.quarto.custo =			self.custo.data
		self.quarto.compartilhado =	True if self.compartilhado.data else False
		self.quarto.ativo =			self.ativo.data

		if self.predio.data:
			self.quarto.predio_id =	self.predio.data

		if not self.quarto.id:
			self.quarto.criar()
		self.quarto.commit()

