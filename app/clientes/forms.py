from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields import StringField, BooleanField, SelectField, EmailField, TelField
from wtforms.validators import DataRequired, Length, Email, NumberRange, Optional
import re
from app.clientes.models import Clientes


class ClientesForm(FlaskForm):
	qual_doc =		SelectField('Qual documento?', choices=[('CNPJ', 'CNPJ'), ('CPF', 'CPF')])
	documento =		StringField('', validators=[DataRequired()])
	nome =			StringField('Nome completo', validators=[DataRequired()])
	cep =			StringField('CEP', validators=[DataRequired()])
	logradouro =	StringField('Logradouro', validators=[DataRequired()])
	numero =		StringField('Número', validators=[DataRequired()])
	complemento =	StringField('complemento', validators=[Optional()])
	telefone =		TelField('Telefone', validators=[DataRequired()])
	email =			EmailField('E-mail', validators=[DataRequired()])
	ativo =			BooleanField('Ativo', default='checked')
	submit =		SubmitField('Salvar')
	novo = False
	cliente = None


	def __init__(self, id):
		super().__init__()
		
		if id:
			self.cliente = Clientes.query.get(id)
			if not self.is_submitted():
				self.qual_doc.data =	'CPF' if len(self.cliente.cnpj_cpf) == 11 else 'CNPJ'

				if self.qual_doc.data == 'CPF':
					doc =	re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})','\g<1>.\g<2>.\g<3>-\g<4>',self.cliente.cnpj_cpf)
				else:
					doc =	re.sub(r'(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})','\g<1>.\g<2>.\g<3>/\g<4>-\g<5>',self.cliente.cnpj_cpf)
				
				if len(self.cliente.telefone) == 11:
					tel =	re.sub(r'(\d{2})(\d{5})(\d{4})','(\g<1>) \g<2>-\g<3>',self.cliente.telefone)
				else:
					tel =	re.sub(r'(\d{2})(\d{4})(\d{4})','(\g<1>) \g<2>-\g<3>',self.cliente.telefone)
				
				cep =	re.sub(r'(\d{5})(\d{3})', '\g<1>-\g<2>', self.cliente.cep)

				self.documento.data =		doc
				self.nome.data =			self.cliente.nome
				self.cep.data =				cep
				self.logradouro.data =		self.cliente.logradouro
				self.numero.data =			self.cliente.numero
				self.complemento.data =		self.cliente.complemento
				self.telefone.data =		tel
				self.email.data =			self.cliente.email
				self.ativo.data =			self.cliente.ativo


	def salvar(self):
		doc =			re.sub(r'\D', '', self.documento.data) ## regex para deixar apenas us números
		nome =			re.sub(r'^\s*|\s*$','', self.nome.data) ## Regex para retirar os espaços do início e fim da palavra
		cep =			re.sub(r'\D', '', self.cep.data)
		logradouro =	re.sub(r'^\s*|\s*$','', self.logradouro.data)
		numero =		re.sub(r'^\s*|\s*$','', self.numero.data)
		complemento =	re.sub(r'^\s*|\s*$','', self.complemento.data)
		telefone =		re.sub(r'\D', '', self.telefone.data)
		email =			re.sub(r'^\s*|\s*$','', self.email.data)
		ativo =			self.ativo.data

		if not self.cliente:
			self.novo =	True
			self.cliente =	Clientes()

		self.cliente.cnpj_cpf =		doc
		self.cliente.nome =			nome
		self.cliente.cep =			cep
		self.cliente.logradouro =	logradouro
		self.cliente.numero =		numero
		self.cliente.complemento =	complemento
		self.cliente.telefone =		telefone
		self.cliente.email =		email
		self.cliente.ativo =		ativo
		
		if self.novo:
			self.cliente.criar()
		self.cliente.commit()


class PesquisaForm(FlaskForm):
	termo =	StringField('Pesquisar')

	def __init__(self):
		super().__init__()
		
