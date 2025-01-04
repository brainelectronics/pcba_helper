#!/usr/bin/env python3

"""Common helper functions"""
import logging
from pathlib import Path
from typing import Dict

import bcrypt
from jinja2 import Environment

LOG_LEVELS = {
    0: logging.CRITICAL,
    1: logging.ERROR,
    2: logging.WARNING,
    3: logging.INFO,
    4: logging.DEBUG,
}

def read_file(filename: Path, mode: str = "r") -> str:
    with open(filename, mode) as file:
        return file.read()

def save_file(filename: Path, content: str, mode: str = "w") -> None:
    """
    Save a file to the specified path with the given content.

    The file and its parent directories will be created if necessary
    """
    Path(filename.parent).mkdir(parents=True, exist_ok=True)

    # save rendered file
    with open(filename, mode) as file:
        file.write(content)


def render(env: Environment, template: str, content: Dict[str, str]) -> str:
    return env.get_template(str(template)).render(content)


def create_hash(password: str) -> str:
    # equivalent to PHP's password_hash()
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def verify_password(password: str, hash: str) -> bool:
    # equivalent to PHP's password_verify()
    return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))
