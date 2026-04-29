from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os


JWT_SECRET = "d3fb12750c2eff92120742e1b334479e"

def decode_token(token):
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms="HS256"
    )


def hash_password(password: str) -> tuple[bytes, bytes]:
    salt = os.urandom(16)  # Random salt for uniqueness
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,  # OWASP recommended minimum
    )
    
    hashed = kdf.derive(password.encode())
    return salt, hashed