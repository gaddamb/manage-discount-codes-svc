import random
import string
import jwt
from src.config.config import config, logger

def generate_random_code(len=8, percentage='10%'):
    logger.info("Generating random discount codes")
    letters = string.ascii_lowercase
    random_code = ''.join(random.choice(letters) for i in range(len))
    return random_code, percentage

def verify_user_with_token_and_return_user(token):
    decoded_str = None
    try:
        decoded_str = jwt.decode(token, config()['auth0_client_secret'], algorithms='HS256')
    except:
        logger.info("Invalid user")
    return decoded_str