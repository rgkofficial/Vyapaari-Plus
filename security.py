import hashlib
import secrets

PBKDF2_ITERATIONS = 600_000

def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    if not isinstance(password, str) or not password:
        raise ValueError("password must be a non-empty string")
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), PBKDF2_ITERATIONS
    ).hex()
    return hashed, salt

def verify_password(password: str, hashed: str, salt: str) -> bool:
    new_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(new_hash, hashed)
