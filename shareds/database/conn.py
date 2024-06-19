import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
      conect = mysql.connector.connect(
        host="db",
        user="IFPEBPT",
        password="IFPEBPT",
        database="IFPEBPT",
        raise_on_warnings=True)
      return conect
    
    except mysql.connector.Error as erro:
      print(f'Erro ao conectar ao MySQL: {erro}')
      


