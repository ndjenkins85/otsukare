from itsdangerous import URLSafeTimedSerializer
from otsukare.config import BaseConfig

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(BaseConfig.SECRET_KEY)
    return serializer.dumps(email, salt=BaseConfig.SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(BaseConfig.SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=BaseConfig.SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except:
        return False
    return email