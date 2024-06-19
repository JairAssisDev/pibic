from pydantic import BaseModel

class Auth(BaseModel):
    matricula: str
    password: str