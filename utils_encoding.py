import os
import hashlib


JWT_SECRET = "d3fb12750c2eff92120742e1b334479e"

def decode_token(token):
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms="HS256"
    )


#def hash_password(password: str) -> tuple[bytes, bytes]:
#    salt = os.urandom(16)  # Random salt for uniqueness
    
#    kdf = PBKDF2HMAC(
#        algorithm=hashes.SHA256(),
#        length=32,
#        salt=salt,
#        iterations=480000,  # OWASP recommended minimum
#    )
    
#    hashed = kdf.derive(password.encode())
#    return salt, hashed


def hash_password(password):
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()