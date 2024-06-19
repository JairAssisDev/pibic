import bcrypt

def encrypt_password(data: str):
    result = bcrypt.hashpw(data.encode("utf-8"),  bcrypt.gensalt(rounds=10))
    return result

def check_password(data: str, hash: str):
    return bcrypt.checkpw(data.encode("utf-8"), hash.encode("utf-8"))