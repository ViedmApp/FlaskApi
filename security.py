from models.usuario import Users_Model
from werkzeug.security import safe_str_cmp
from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)


def encrypt_password(password):
    return pwd_context.encrypt(password)


def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and check_encrypted_password(password, user.password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
