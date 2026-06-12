import os
import hashlib
import jwt



def decode_token(token):
    return jwt.decode(
        token,
        os.getenv("JWT_SECRET"),
        algorithms="HS256"
    )


def hash_password(password):
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()