from app import db

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    sex = db.Column(db.Integer, nullable=False)
    redo = db.Column(db.Integer, nullable=False)
    cpb = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    bsa = db.Column(db.Float, nullable=False)
    hb = db.Column(db.Float, nullable=False)
    probability = db.Column(db.Float, nullable=True)
    prediction = db.Column(db.Float, nullable=True)
    imagem = db.Column(db.Text, nullable=True)


    def __repr__(self):
        return f'<Paciente {self.nome}>'

    @staticmethod
    def validate_sex(value):
        if value not in [0, 1]:
            raise ValueError(f'Valor inválido para campo binário: {value}')
        return value

    @staticmethod
    def validate_age(value):
        if not 0 < value < 140:
            raise ValueError('A idade deve estar entre 0 e 140')
        return value

    @staticmethod
    def validate_redo_cpb(value):
        if value not in [0, 1]:
            raise ValueError(f'Valor inválido para campo binário: {value}')
        return value