from passlib.hash import bcrypt
import string
import random


def encrypt(password):
    """Encrypts a password for the user table."""

    h = bcrypt.encrypt(password)

    return h


def decrypt(hashed_password, password):
    """Decrypts a password from the user table."""

    if bcrypt.verify(password, hashed_password) is True:
        return True
    else:
        return False


def random_string(size=25, chars=string.ascii_uppercase + string.digits + string.punctuation):
    """Generates a random string for the session"""

    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))
