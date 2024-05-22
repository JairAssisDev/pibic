from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import matplotlib


db = SQLAlchemy()

def create_app():
    matplotlib.use('Agg')
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.Config')
    db.init_app(app)

    with app.app_context():
        # Importar modelos e blueprints
        from app.controllers.controlerpatient import paciente_bp
        from app.controllers.user_controller import user_bp

        app.register_blueprint(user_bp)
        app.register_blueprint(paciente_bp)

        # Criar as tabelas no banco de dados (caso necessário)
        db.create_all()

    return app
