from pydantic import BaseModel

class User(BaseModel):
    id: int = None
    password: str
    userName: str
    matricula: str