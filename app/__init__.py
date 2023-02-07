from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_principal import Principal, Permission, RoleNeed
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_session import Session
from config import Config
import psycopg2, locale, re

db =				SQLAlchemy()
login_manager =		LoginManager()
migrate =			Migrate()
sess =				Session()
principal =			Principal()

# Filtros personalizados
def format_inteiros(valor):
	return locale.format('%d', valor or 0, grouping=True)

def format_float(valor):
	return locale.format('%.2f', valor or 0, grouping=True)

def regex_sub(valor, regex, sub):
	return re.sub(regex,sub,valor)

def format_datetime(valor, formato):
	return valor.strftime(formato)

# Permissoes
administrador =	Permission(RoleNeed('Administrador'))
atendente =		Permission(RoleNeed('Atendente'))
gerente =		Permission(RoleNeed('Gerente'))
governanca =	Permission(RoleNeed('Governança'))

def create():
	app =	Flask(__name__, instance_relative_config=True)
	app.config.from_object(Config)
	
	# idioma e formato de valores locais
	locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
	locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')
	
	# declarar os filtros personalizados
	app.jinja_env.filters['format_inteiros'] = format_inteiros
	app.jinja_env.filters['format_float'] = format_float
	app.jinja_env.filters['regex_sub'] = regex_sub
	app.jinja_env.filters['format_datetime'] = format_datetime

	# Iniciar plugins externos
	db.init_app(app)
	login_manager.init_app(app)
	principal.init_app(app)
	sess.init_app(app)
	migrate.init_app(app, db)

	# Imports das blueprints para rotas
	from app.estrutura_predial.views import estrutura_bp
	from app.usuarios.login import login_bp
	from app.usuarios.views import usuarios_bp, cargos_bp
	from app.reservas.views import reservas_bp
	from app.clientes.views import clientes_bp
	from app.governancas.views import governanca_bp

	with app.app_context():
		login_manager.login_view =	"login_bp.login"
		app.register_blueprint(estrutura_bp)
		app.register_blueprint(login_bp)
		app.register_blueprint(usuarios_bp)
		app.register_blueprint(cargos_bp)
		app.register_blueprint(reservas_bp)
		app.register_blueprint(clientes_bp)
		app.register_blueprint(governanca_bp)
		
		db.create_all()
		return app
