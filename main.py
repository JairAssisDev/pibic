import matplotlib
from flask import Flask
from flask_cors import CORS
from patient.predict import predict_bp
from patient.patientEntity import patient_bp

matplotlib.use('Agg')
app = Flask(__name__)
CORS(app)

app.register_blueprint(patient_bp)
app.register_blueprint(predict_bp)

if __name__ == "__main__":
    app.run()
