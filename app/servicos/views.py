from flask import url_for, Blueprint, render_template, redirect, session, jsonify, request, Response, abort
from flask_login import login_required, current_user
import app, requests
from app.estrutura_predial.models import Predios, Quartos
from app.estrutura_predial.forms import EditarForm
from app import administrador, atendente, gerente, governanca

estrutura_bp = Blueprint('estrutura_bp', __name__, template_folder='templates', static_folder='static', url_prefix='/estrutura')

@estrutura_bp.route('/', methods=['GET',])
def index():
	""" mostra os predios """

	predios = Predios.get()

	return render_template('lista_predios.html', predios=predios)

@estrutura_bp.route('/adicionar', methods=['GET', 'POST'])
@estrutura_bp.route('/editar', methods=['GET', 'POST'])
def editar_predios(id=None):
	
	form = EditarForm(id)
	
	if form.is_submitted():
		return redirect( url_for('estrutura_bp.index') )
	return render_template('editar.html', form=form)

