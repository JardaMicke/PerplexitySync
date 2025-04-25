import time
import json
from .security import hmac_sign

class AuditLogger:
    def __init__(self, log_path: str, hmac_key: bytes):
        self.log_path = log_path
        self.hmac_key = hmac_key

    def log(self, operation: str, path: str, user: str = "system"):  # user může být rozšířen
        entry = {
            'timestamp': time.time(),
            'operation': operation,
            'path': path,
            'user': user
        }
        entry['hmac'] = hmac_sign(json.dumps(entry, sort_keys=True), self.hmac_key)
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
