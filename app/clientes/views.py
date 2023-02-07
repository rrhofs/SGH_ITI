from flask import url_for, Blueprint, render_template, redirect, session, jsonify, request, Response, abort
from flask_login import login_required, current_user
import app, requests, re
from app.clientes.models import Clientes
from app.clientes.forms import ClientesForm, PesquisaForm
from app.estrutura_predial.forms import AtivoForm
from app import administrador, atendente, gerente, governanca

clientes_bp = Blueprint('clientes_bp', __name__, template_folder='templates', static_folder='static', url_prefix='/clientes')

@clientes_bp.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
	
	form = 			AtivoForm()
	pesquisa_form =	PesquisaForm()

	clientes = Clientes.get(ativo=form.ativo.data)

	return render_template('lista_clientes.html', title='Clientes', clientes=clientes, form=form, pesquisa_form=pesquisa_form,
		adm=administrador.can(), atendente=atendente.can(), gerente=gerente.can(), governanca=governanca.can(), usuario=current_user)


@clientes_bp.route('/adicionar', methods=['GET', 'POST'])
@clientes_bp.route('/editar/<id>', methods=['GET', 'POST'])
@login_required
def editar_clientes(id=None):
	
	form = ClientesForm(id)
	
	if form.validate_on_submit():
		form.salvar()
		return redirect( url_for('clientes_bp.dashboard') )

	return render_template('editar.html', title='Formulário Clientes', form=form,
		adm=administrador.can(), atendente=atendente.can(), gerente=gerente.can(), governanca=governanca.can(), usuario=current_user)

@clientes_bp.route('/pesquisar_clientes', methods=['GET',])
@clientes_bp.route('/pesquisar_clientes/<termo>', methods=['GET',])
@clientes_bp.route('/pesquisar_clientes/<termo>/<ativo>', methods=['GET',])
@login_required
def pesquisar_clientes(termo=None, ativo=False):
	if ativo == 'false':
		ativo = False
	
	if termo == 'None':
		termo =	None

	clientes = Clientes.get(ativo=ativo, termo=termo)
	dados = []
	for cliente in clientes:
		
				
		if len(cliente.cnpj_cpf) == 11:
			doc =	re.sub(r'(\d{3})(\d{3})(\d{3})(\d{2})','\g<1>.\g<2>.\g<3>-\g<4>', cliente.cnpj_cpf)
		else:
			doc =	re.sub(r'(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})','\g<1>.\g<2>.\g<3>/\g<4>-\g<5>', cliente.cnpj_cpf)

		if len(cliente.telefone) == 11:
			tel =	re.sub(r'(\d{2})(\d{5})(\d{4})','(\g<1>) \g<2>-\g<3>', cliente.telefone)
		else:
			tel =	re.sub(r'(\d{2})(\d{4})(\d{4})','(\g<1>) \g<2>-\g<3>', cliente.telefone)
		
		cep =	re.sub(r'(\d{5})(\d{3})', '\g<1>-\g<2>', cliente.cep)
		acoes =	"""<a href="{}"><img src="{}" style="height:15px;"></a><a href="{}"><img src="{}" style="height:15px;"></a>""".format( url_for('clientes_bp.editar_clientes', id=cliente.cnpj_cpf), url_for('static', filename='img/editar.png'),
					url_for('reservas_bp.adicionar_reservas', cliente_id=cliente.cnpj_cpf), url_for('static', filename='img/adicionar_pedido.png') )

		c = {'cnpj_cpf': doc, 'nome': cliente.nome, 'cep': cep, 'logradouro': cliente.logradouro, 'numero': cliente.numero,
			'complemento': cliente.complemento, 'telefone': tel, 'email': cliente.email, 'ativo': cliente.ativo, 'acoes': acoes}
		dados.append(c)

	return jsonify(dados)
