from flask import Flask
from flask_cors import CORS
import matplotlib

def create_app():

    matplotlib.use('Agg')
    app = Flask(__name__)
    CORS(app)

    with app.app_context():
        from controllers.controlerpatient import paciente_bp
        from controllers.controller_user import user_bp

        app.register_blueprint(paciente_bp)
        app.register_blueprint(user_bp)

    return app
