from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields import StringField, BooleanField
from wtforms.validators import DataRequired, Length, Email, NumberRange
from app.estrutura_predial.models import Predios

class EditarForm(FlaskForm):
	nome = StringField('Prédio', validators=[Length(max=255)])
	ativo = BooleanField('Ativo', default='checked')
	submit = SubmitField('Salvar')

	def __init__(self, id):
		super().__init__()
		if id:
			predio = Predios.query.get(id)

			self.nome.data = predio.nome
			self.ativo.data = predio.ativo
		else:
			predio = Predios()

		
