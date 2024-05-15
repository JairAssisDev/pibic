from pydantic import ValidationError
from flask import Blueprint, request, jsonify
from patient.services.impl.service_impl import PacienteServiceImpl


patient_bp = Blueprint('patientEntity', __name__, url_prefix='/patient')
paciente_service = PacienteServiceImpl()

@patient_bp.route("/", methods=["POST"])
def criar_paciente():
    dados_paciente = request.get_json()
    try:
        paciente_service.criar_paciente(dados_paciente)
    except ValidationError as e:
        return jsonify({"erro": str(e)}), 400
    return jsonify({'mensagem': 'Paciente criado com sucesso'}), 201


@patient_bp.route("/", methods=["GET"])
def obter_todos_pacientes():
    return jsonify(paciente_service.obter_todos_pacientes())


@patient_bp.route("/predict/<nome>", methods=["GET"])
def predict(nome):
    return paciente_service.predict(nome)
