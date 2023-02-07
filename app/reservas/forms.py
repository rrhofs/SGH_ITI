from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields import StringField, BooleanField, SelectField, SelectMultipleField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, NumberRange
from app.estrutura_predial.models import Predios, Quartos
from app.reservas.models import DetalhesConta, Conta
from app.clientes.models import Clientes
from datetime import datetime, timedelta

class AdicionarReservaForm(FlaskForm):
	quartos_compartilhados =	SelectMultipleField('Quartos compatilhados', choices=[], coerce=int)
	quartos_privativos = 		SelectMultipleField('Quartos privativos', choices=[], coerce=int)
	dt_inicial =				DateField('Data de entrada')
	dt_final =					DateField('Data de saída')
	nro_pessoas =				IntegerField('Número de pessoas')
	submit =					SubmitField('Adicionar reserva')
	cliente =					None
	conta =						None

	def __init__(self, cliente_id):
		super().__init__()
		if not cliente_id:
			self.cliente =	Clientes.query.get(-1)
		else:
			self.cliente =	Clientes.query.get(cliente_id)

		self.quartos_compartilhados.choices =	list( map(lambda x: (x.id, x.predio_ref.nome + ' - ' + x.numero),
			Quartos.get(ativo=True, compartilhado=True)) )
		self.quartos_privativos.choices =		list( map(lambda x: (x.id, x.predio_ref.nome + ' - ' + x.numero),
			Quartos.get(ativo=True, compartilhado=False)) )
	
	def salvar(self):
		if self.cliente:
			self.conta = Conta.query.filter(Conta.cliente_id==self.cliente.cnpj_cpf, Conta.ativa==True,
				Conta.fechada==False).first()
		if not self.conta:
			self.conta = Conta()
			self.conta.dt_abertura =	datetime.now()
		
		self.conta.ativa =			True
		self.conta.fechada =		False
		self.conta.cliente_id =		self.cliente.cnpj_cpf
		self.conta.criar()
		
		for quarto in self.quartos_privativos.data:
			detalhes_conta = 				DetalhesConta()
			detalhes_conta.conta_id =		self.conta.id
			detalhes_conta.dt_inicial =		self.dt_inicial.data
			detalhes_conta.dt_final =		self.dt_final.data
			detalhes_conta.quarto_id =		quarto
			detalhes_conta.criar()
		
		nro_hospedes = self.nro_pessoas.data or 0
		for quarto in self.quartos_compartilhados.data:
			detalhes_quarto =					DetalhesConta.quartos_info(self.dt_inicial.data, self.dt_final.data, [quarto])
			
			if detalhes_quarto:
				qt_pessoas_no_quarto =			detalhes_quarto[0].vagas_ocupadas or 0
				capacidade_quarto =				detalhes_quarto[0].lotacao or 0
			
			if ((capacidade_quarto - qt_pessoas_no_quarto) - nro_hospedes >= 0):
				detalhes_conta = 				DetalhesConta()
				detalhes_conta.conta_id =		self.conta.id
				detalhes_conta.dt_inicial =		self.dt_inicial.data
				detalhes_conta.dt_final =		self.dt_final.data
				detalhes_conta.quarto_id =		quarto
				if self.conta.id == -1:
					detalhes_conta.nro_pessoas =	capacidade_quarto
				else:
					detalhes_conta.nro_pessoas =	nro_hospedes
				nro_hospedes =					0
			elif ((capacidade_quarto - qt_pessoas_no_quarto) - nro_hospedes <= 0) and (quarto != self.quartos_compartilhados.data[-1]):
				detalhes_conta = 				DetalhesConta()
				detalhes_conta.conta_id =		self.conta.id
				detalhes_conta.dt_inicial =		self.dt_inicial.data
				detalhes_conta.dt_final =		self.dt_final.data
				detalhes_conta.quarto_id =		quarto
				detalhes_conta.nro_pessoas =	capacidade_quarto - qt_pessoas_no_quarto
				nro_hospedes =					nro_hospedes - (capacidade_quarto - qt_pessoas_no_quarto)
			elif ((capacidade_quarto - qt_pessoas_no_quarto) - nro_hospedes <= 0) and (quarto == self.quartos_compartilhados.data[-1]):
				return 'Muitos hóspedes para poucas vagas.'
			elif nro_hospedes == 0:
				break

			detalhes_conta.criar()

		detalhes_conta.set_valor_conta(self.conta.id)
		self.conta.commit()

