from shareds.database.conn import get_connection
from entities.user import User
from shareds.crypto import encrypt_password


def get_user(matricula: str) -> User | None:
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = f"SELECT * FROM users WHERE matricula = %s"
        cursor.execute(query, (matricula,))
        return cursor.fetchall()
    except:
        raise
    finally:
        if 'conexao' in locals():
            conn.close()

def insert_user(data: User):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('INSERT INTO users (username, matricula, password) VALUES (%s, %s, %s)', (data.userName, data.matricula, encrypt_password(data.password)))
        conn.commit()
    except:
        raise
    finally:
        if 'conexao' in locals():
            conn.close()
