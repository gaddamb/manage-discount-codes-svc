import random
import string

def generate_random_code(len=8, percentage='10%'):
    letters = string.ascii_lowercase
    random_code = ''.join(random.choice(letters) for i in range(len))
    return random_code, percentage
