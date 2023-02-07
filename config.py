import os
from dotenv import load_dotenv

class Config():
	load_dotenv(verbose=True, override=True)
	
	# Sistema
	TESTING =			os.environ.get('TESTING')
	DEBUG = 			os.environ.get('DEBUG')
	SECRET_KEY =		os.environ.get('SECRET_KEY')
	SERVER_NAME =		os.environ.get('SERVER_NAME')
	SESSION_TYPE =		os.environ.get('SESSION_TYPE')

	# Database
	DB =								os.environ.get('DB')
	USER =								os.environ.get('USER')
	PASS =								os.environ.get('PASS')
	SERVER = 							os.environ.get('SERVER')
	PORT =								os.environ.get('PORT')
	SQLALCHEMY_DATABASE_URI =			'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(USER, PASS, SERVER, PORT, DB)
	SQLALCHEMY_TRACK_MODIFICATIONS =	os.environ.get('TRACK')

