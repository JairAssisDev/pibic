from patient.services.service import PacienteService
from patient.models.paciente import Paciente
from patient.predictions.predict import predict_and_explain
from flask import jsonify
import json

class PacienteServiceImpl(PacienteService):
    def __init__(self):
        self.pacientes = []

    def criar_paciente(self, dados_paciente):
        paciente = Paciente(**dados_paciente)
        print(self.pacientes)
        self.pacientes.append(paciente.model_dump())
        response, status_code = self.predict(paciente.nome)
        if status_code == 200:
            json_data = json.loads(response.get_data(as_text=True))
            paciente.probability = json_data["prediction"]['true_probability']
            paciente.prediction = json_data["prediction"]['prediction']
            paciente.imagem = json_data["prediction"]['lime_image']
            
        else:
            raise jsonify(f"Erro: {response.get_json()}")



    def obter_todos_pacientes(self):
        return self.pacientes
    

    def obter_paciente_por_nome(self, nome):
        return next((p for p in self.pacientes if p['nome'] == nome), None)
    
    def predict(self, nome):
        paciente = self.obter_paciente_por_nome(nome)
        if paciente:
            sex = paciente['sex']
            redo = paciente['redo']
            cpb = paciente['cpb']
            age = paciente['age']
            bsa = paciente['bsa']
            hb = paciente['hb']

            prediction = predict_and_explain(sex, redo, cpb, age, bsa, hb)
            pred = {'prediction': prediction}
            return jsonify(pred), 200
        else:
            error = {'error': 'Paciente não encontrado'}
            return jsonify(error), 404
