from flask import url_for, Blueprint, render_template, redirect, session, jsonify, request, Response, abort
from flask_login import login_required, current_user
import app, requests
from app.estrutura_predial.models import Predios, Quartos
from app.reservas.forms import AdicionarReservaForm
from app.reservas.models import DetalhesConta
from app import administrador, atendente, gerente, governanca

reservas_bp = Blueprint('reservas_bp', __name__, template_folder='templates', static_folder='static', url_prefix='/reservas')

@reservas_bp.route('/', methods=['GET',])
def dashboard():
	if not (administrador.can() or gerente.can() or atendente.can()):
		abort(403)

	reservas = DetalhesConta.get_reservas()

	return render_template('lista_reservas.html', reservas=reservas, title='Reservas',
		adm=administrador.can(), atendente=atendente.can(), gerente=gerente.can(), governanca=governanca.can(), usuario=current_user)

@reservas_bp.route('/remover_reserva/<reserva_id>', methods=['GET',])
def remover_reserva(reserva_id):
	if not (administrador.can() or gerente.can() or atendente.can()):
		abort(403)
	
	DetalhesConta.remover_reserva(reserva_id)

	return redirect( url_for('reservas_bp.dashboard') )


@reservas_bp.route('/adicionar_reserva', methods=['GET', 'POST'])
@reservas_bp.route('/adicionar_reserva/<cliente_id>', methods=['GET', 'POST'])
@login_required
def adicionar_reservas(cliente_id=None):
	if not (administrador.can() or atendente.can() or gerente.can()):
		abort(403)

	form = AdicionarReservaForm(cliente_id)

	if form.is_submitted() and form.submit.data:
		msg = form.salvar()
		if msg:
			return render_template('adicionar_reserva.html', form=form, msg=msg, title='Criar reservas',
				adm=administrador.can(), atendente=atendente.can(), gerente=gerente.can(), governanca=governanca.can(), usuario=current_user)
		else:
			return redirect( url_for('login_bp.index') )

	return render_template('adicionar_reserva.html', form=form, title='Criar reservas',
		adm=administrador.can(), atendente=atendente.can(), gerente=gerente.can(), governanca=governanca.can(), usuario=current_user)

@reservas_bp.route('/escolher_datas', methods=['GET', 'POST'])
@login_required
def escolher_datas():
	if not (administrador.can() or gerente.can() or atendente.can()):
		abort(403)

	dt_inicial =	request.form.get('dt_inicial')
	dt_final =		request.form.get('dt_final')
	quartos =		list( map(lambda x: int(x), request.form.get('quartos').split(',')) )
	nro_pessoas =	request.form.get('nro_pessoas')
	resultado =		DetalhesConta.quartos_ocupados(dt_inicial, dt_final, quartos, nro_pessoas)
	algum_lotado =	[]
	
	if resultado:
		if len(resultado) == 1:
			msg =		'O quarto '
			plural =	False
		else:
			msg =		'Os quartos '
			plural =	True

		for r in resultado:
			lotado =	False
			if not r.compartilhado:
				lotado =	True
			elif r.lotacao - r.vagas_ocupadas <= 0:
				lotado =	True
			else:
				lotado = False
			
			if lotado:
				if not r == resultado[-1]:
					msg +=	r.nome + ' - ' + r.numero + ', '
				else:
					msg +=	r.nome + ' - ' + r.numero
				algum_lotado.append(1)
			
		if plural:
			msg +=	' estão ocupados nas datas escolhidas.'
		else:
			msg +=	' está ocupado nas datas escolhidas.'
	
	if algum_lotado:
		return jsonify({'sucesso':False, 'msg':msg})
	
	return jsonify({'sucesso':True})

@reservas_bp.route('/quartos_info', methods=['GET', 'POST'])
@login_required
def quartos_info():
	if not (administrador.can() or gerente.can() or atendente.can()):
		return jsonify({'sucesso':False})

	dt_inicial =	request.form.get('dt_inicial')
	dt_final =		request.form.get('dt_final')
	quartos =		list( map(lambda x: int(x), request.form.get('quartos').split(',')) )
	quartos_info = 	DetalhesConta.quartos_info(dt_inicial, dt_final, quartos)
	
	quartos_vet =	[]
	for qi in quartos_info:
		quarto =		qi.nome + ' - ' + qi.numero
		if qi.compartilhado:
			lotacao =		str(qi.vagas_ocupadas if qi.vagas_ocupadas else 0) + '/' + str(qi.lotacao)
		else:
			lotacao =		str(qi.lotacao)
		qt_banheiros =	qi.qt_banheiros
		cozinha =		'Sim' if qi.cozinha else 'Não'
		diaria =		qi.custo
		compartilhado =	'Compartilhado' if qi.compartilhado else 'Privativo'

		quarto_dict =	{'quarto': quarto, 'lotacao': lotacao, 'qt_banheiros': qt_banheiros, 'cozinha': cozinha,
			'diaria': diaria, 'compartilhado': compartilhado}
		quartos_vet.append(quarto_dict)
	
	return jsonify({'sucesso':True, 'dados':quartos_vet})
