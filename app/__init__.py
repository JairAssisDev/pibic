from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import matplotlib
import mysql.connector
from app.config import Config

db = SQLAlchemy()

def create_database():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root'
    )
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS BPTDB")
    cursor.close()
    connection.close()

def create_app():
    create_database()  # Chama a função para criar o banco de dados se não existir
    
    matplotlib.use('Agg')
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        # Importar modelos e blueprints
        from app.models.paciente import Paciente  # Certifique-se de que o caminho está correto
        from app.controllers.controlerpatient import paciente_bp

        app.register_blueprint(paciente_bp)

        # Criar as tabelas no banco de dados (caso necessário)
        db.create_all()

    return app
