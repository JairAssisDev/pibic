import matplotlib
from flask import Flask
from flask_cors import CORS
from patient.controllers.controlerpatient import patient_bp

matplotlib.use('Agg')
app = Flask(__name__)
CORS(app)

app.register_blueprint(patient_bp)

if __name__ == "__main__":
    app.run(debug=True)
