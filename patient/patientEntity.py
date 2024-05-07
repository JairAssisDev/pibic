from flask import Blueprint, request, jsonify
from pydantic import BaseModel, validator, ValidationError
from patient.predict import predict_and_explain


patient_bp = Blueprint('patientEntity', __name__, url_prefix='/patient')

class Patient(BaseModel):
    id : int 
    nome : str
    cpf : str
    sex : int
    redo : int
    cpb : int 
    age : int
    bsa : float
    hb : float 


    @validator('sex')
    def validate_sex(cls, value):
        if value != 0 and value != 1:
            raise ValueError('invalid sex') 
        return value
    
    @validator('redo')
    def validate_redo(cls, value):
        if value != 0 and value != 1:
            raise ValueError('invalid redo') 
        return value
    
    @validator('cpb')
    def validate_cpb(cls, value):
        if value != 0 and value != 1:
            raise ValueError('invalid cpb') 
        return value
    
    @validator('age')
    def validate_age(cls, value):
        if value <= 0 or value >= 140:
            raise ValueError('invalid age') 
        return value
    

patient = Patient(id=1, nome="jair", cpf="232323", sex=1 ,redo=1,cpb=0,age=12,bsa=1.70,hb=22.2)

lista=[]
lista.append(patient.dict())

@patient_bp.route("/", methods=["POST"])
def createPatient():
    patient_data = request.get_json()  # Obter dados do request
    try:
        patient = Patient(**patient_data)  # Criar um objeto Patient com os dados
        lista.append(patient.dict())
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400  # Retorna um erro 400 com a mensagem de erro
    return jsonify({'message': 'Paciente cadastrado com sucesso'}), 201


@patient_bp.route("/", methods=["GET"])
def getAllPatient():
    return jsonify(lista)

@patient_bp.route("/predict/<nome>", methods=["GET"])
def predict(nome):
    paciente = next((p for p in lista if p['nome'] == nome), None)

    if paciente:
        sex = paciente['sex']
        redo = paciente['redo']
        cpb = paciente['cpb']
        age = paciente['age']
        bsa = paciente['bsa']
        hb = paciente['hb']

        prediction = predict_and_explain(sex, redo, cpb, age, bsa, hb)

        return jsonify({'prediction': prediction})
    else:
        return jsonify({'error': 'Paciente não encontrado'}), 404