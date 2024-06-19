from pydantic import BaseModel

class UserBase(BaseModel):
    userName: str
    matricula: str