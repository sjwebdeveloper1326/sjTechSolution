# project/utils/account_helper.py
import random
import string
from datetime import datetime
from django.contrib.auth.models import User
from django.db import IntegrityError

def _rand_password(length=10):
    """Strong random password generator."""
    chars = string.ascii_letters + string.digits + "@#$%&*!?"
    return "".join(random.choice(chars) for _ in range(length))


def create_username(name: str, unique_code: str) -> str:
    """
    Format requested: <name><MM>M<YY>Y_<NNNN>
    Example: jaspreet11M25Y_0007
    - name: lowercase, spaces removed
    - unique_code: something like 'SJE-0007' -> we take last numeric part
    """
    # clean_name = "".join(name.lower().split())
    first_name = name.strip().split()[0].lower()
    now = datetime.now()
    # date_code = f"{now.month:02d}M{str(now.year)[-2:]}Y"
    # extract digits (last part) from unique_code
    last_part = unique_code
    # last_part = unique_code.split("-")[-1] if unique_code else ""
    # return f"{clean_name}{date_code}_{last_part}"
    return f"{first_name}_{last_part}"


def create_system_user(name: str, email: str, unique_code: str, password_length: int = 10):
    """
    Create a Django User and return (user_obj, username, plain_password).
    If username collides, append a short random suffix until unique.
    """
    # generate base username
    username = create_username(name, unique_code)
    # ensure uniqueness
    attempt = 0
    base_username = username
    while True:
        try:
            # generate a password
            password = _rand_password(password_length)
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=name
            )
            return user, username, password
        except IntegrityError:
            # username exists; tweak username
            attempt += 1
            suffix = ''.join(random.choice(string.digits) for _ in range(3))
            username = f"{base_username}{suffix}"
            if attempt > 5:
                raise
