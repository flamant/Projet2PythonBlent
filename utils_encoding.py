import os
import hashlib
import jwt


JWT_SECRET = "d3fb12750c2eff92120742e1b334479e"

def decode_token(token):
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms="HS256"
    )


def hash_password(password):
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()