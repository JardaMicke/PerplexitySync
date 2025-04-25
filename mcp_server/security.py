import os
from typing import List
from pathlib import Path
import hashlib

# Whitelist/blacklist cest

def is_allowed_path(path: str, allowed_dirs: List[str]) -> bool:
    abs_path = os.path.abspath(os.path.normpath(path))
    for allowed in allowed_dirs:
        allowed_abs = os.path.abspath(os.path.normpath(allowed))
        if abs_path.startswith(allowed_abs):
            return True
    return False

def validate_path(path: str) -> bool:
    # Zakáže directory traversal (..)
    norm = os.path.normpath(path)
    if '..' in norm.split(os.sep):
        return False
    return True

# HMAC logování

def hmac_sign(message: str, key: bytes) -> str:
    return hashlib.pbkdf2_hmac('sha256', message.encode(), key, 100000).hex()
