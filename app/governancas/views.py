from flask import url_for, Blueprint, render_template, redirect, session, jsonify, request, Response, abort
from flask_login import login_required, current_user
import app, requests
from app.estrutura_predial.models import Predios, Quartos
from app.reservas.forms import AdicionarReservaForm
from app.reservas.models import DetalhesConta
from app import administrador, atendente, gerente, governanca

governanca_bp = Blueprint('governanca_bp', __name__, template_folder='templates', static_folder='static', url_prefix='/governanca')

@governanca_bp.route('/', methods=['GET',])
def dashboard():
	if not (administrador.can() or gerente.can() or governanca.can()):
		abort(403)

	governanca_lista =	DetalhesConta.get_governanca()

	return render_template('lista_governanca.html', governanca_lista=governanca_lista, title='Governança',
		adm=administrador.can(), atendente=atendente.can(), gerente=gerente.can(), governanca=governanca.can(), usuario=current_user)

@governanca_bp.route('/remover_governanca/<governanca_id>', methods=['GET',])
def remover_governanca(governanca_id):
	if not (administrador.can() or gerente.can() or governanca.can()):
		abort(403)
	
	DetalhesConta.remover_governanca(governanca_id)

	return redirect( url_for('governanca_bp.dashboard') )


@governanca_bp.route('/adicionar_governança', methods=['GET', 'POST'])
@login_required
def adicionar_governanca():
	if not (administrador.can() or gerente.can() or governanca.can()):
		abort(403)

	form = AdicionarReservaForm('-1')

	if form.is_submitted() and form.submit.data:
		form.salvar()
		return redirect( url_for('governanca_bp.dashboard') )

	return render_template('adicionar_reserva.html', form=form, title='Criar governança',
		adm=administrador.can(), atendente=atendente.can(), gerente=gerente.can(), governanca=governanca.can(), usuario=current_user)

