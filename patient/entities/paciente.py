from pydantic import BaseModel, validator

class Paciente(BaseModel):
    id: int
    nome: str
    cpf: str
    sex: int
    redo: int
    cpb: int
    age: int
    bsa: float
    hb: float
    

    @validator('sex', 'redo', 'cpb')
    def validar_binario(cls, valor):
        if valor not in [0, 1]:
            raise ValueError(f'Valor inválido para campo binário: {valor}')
        return valor

    @validator('age')
    def validar_idade(cls, valor):
        if not 0 < valor < 140:
            raise ValueError('A idade deve estar entre 0 e 140')
        return valor