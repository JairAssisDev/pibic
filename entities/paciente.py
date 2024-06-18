from pydantic import BaseModel

age_max = 140
age_min = 0
class Paciente(BaseModel):
    nome:str
    cpf:str
    sex:int
    redo:int
    cpb:int
    age:int
    bsa:float
    hb:float
    probability: str = None
    prediction: str = None
    imagem: str = None 


    def __repr__(self):
        return f'<Paciente {self.nome}>'
    

    @staticmethod
    def validate_sex(value):
        if value not in [0, 1]:
            raise ValueError(f'Valor inválido para campo binário: {value}')
        return value

    @staticmethod
    def validate_age(value):
        if age_min < value and value < age_max :
            raise ValueError('A idade deve estar entre 0 e 140')
        return value

    @staticmethod
    def validate_redo_cpb(value):
        if value not in [0, 1]:
            raise ValueError(f'Valor inválido para campo binário: {value}')
        return value