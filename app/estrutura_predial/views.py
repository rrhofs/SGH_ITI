from flask import url_for, Blueprint, render_template, redirect, session, jsonify, request, Response, abort
from flask_login import login_required, current_user
import app, requests
from app.estrutura_predial.models import Predios, Quartos
from app.estrutura_predial.forms import PredioForm, QuartoForm, AtivoForm
from app import administrador, atendente, gerente, governanca

estrutura_bp = Blueprint('estrutura_bp', __name__, template_folder='templates', static_folder='static', url_prefix='/estrutura')

@estrutura_bp.route('/predios', methods=['GET','POST'])
@login_required
def predios():

	if administrador.can():
		form = AtivoForm()
		predios = Predios.get(ativo=form.ativo.data)
			
		return render_template('lista_predios.html', predios=predios, form=form,
			adm=administrador.can(), atendente=atendente.can(), gerente=gerente.can(), governanca=governanca.can(), usuario=current_user)
	abort(404, 'Seu cargo não permite acesso a esta página')

@estrutura_bp.route('/predios/adicionar', methods=['GET', 'POST'])
@estrutura_bp.route('/predios/editar/<id>', methods=['GET', 'POST'])
@login_required
def editar_predios(id=None):
	
	if administrador.can():
		form = PredioForm(id)
		
		if form.validate_on_submit():
			form.salvar()
			return redirect( url_for('estrutura_bp.predios') )
		return render_template('editar_predios.html', form=form,
			adm=administrador.can(), atendente=atendente.can(), gerente=gerente.can(), governanca=governanca.can(), usuario=current_user)
	abort(404, 'Seu cargo não permite acesso a esta página')

@estrutura_bp.route('/quartos', methods=['GET','POST'])
@login_required
def quartos():

	if administrador.can():
		form = AtivoForm()
		quartos = Quartos.get(ativo=form.ativo.data)
			
		return render_template('lista_quartos.html', quartos=quartos, form=form,
			adm=administrador.can(), atendente=atendente.can(), gerente=gerente.can(), governanca=governanca.can(), usuario=current_user)
	abort(404, 'Seu cargo não permite acesso a esta página')

@estrutura_bp.route('/quartos/adicionar', methods=['GET', 'POST'])
@estrutura_bp.route('/quartos/editar/<id>', methods=['GET', 'POST'])
@login_required
def editar_quartos(id=None):
	
	if administrador.can():
		form = QuartoForm(id)
		
		if form.validate_on_submit():
			form.salvar()
			return redirect( url_for('estrutura_bp.quartos') )
		return render_template('editar_quartos.html', form=form,
			adm=administrador.can(), atendente=atendente.can(), gerente=gerente.can(), governanca=governanca.can(), usuario=current_user)
	abort(404, 'Seu cargo não permite acesso a esta página')

