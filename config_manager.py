import os
import json
import win32crypt
from pathlib import Path
from typing import Dict, Any

CONFIG_DIR = os.path.join(os.environ.get('APPDATA', ''), 'PerplexitySync')
CONFIG_PATH = os.path.join(CONFIG_DIR, 'projects.json')

class ProjectConfig:
    def __init__(self, spaceId: str, localPath: str, lastSynced: str, fileMappings: Dict[str, str]):
        self.spaceId = spaceId
        self.localPath = localPath
        self.lastSynced = lastSynced
        self.fileMappings = fileMappings

    def to_dict(self):
        return {
            'spaceId': self.spaceId,
            'localPath': self.localPath,
            'lastSynced': self.lastSynced,
            'fileMappings': self.fileMappings
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        return ProjectConfig(
            spaceId=data['spaceId'],
            localPath=data['localPath'],
            lastSynced=data['lastSynced'],
            fileMappings=data['fileMappings']
        )

def encrypt_data(data: bytes) -> bytes:
    # CryptProtectData vrací tuple (description, data)
    result = win32crypt.CryptProtectData(data, None, None, None, None, 0)
    return result[1] if isinstance(result, tuple) else result

def decrypt_data(data: bytes) -> bytes:
    # CryptUnprotectData vrací tuple (description, data)
    result = win32crypt.CryptUnprotectData(data, None, None, None, 0)
    return result[1] if isinstance(result, tuple) else result

def save_configs(configs: Dict[str, ProjectConfig]):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    # Pouze localPath bude šifrován, ostatní zůstanou plain
    serializable = {k: v.to_dict() for k, v in configs.items()}
    for v in serializable.values():
        v['localPath'] = encrypt_data(v['localPath'].encode('utf-8')).hex()
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(serializable, f, indent=2)

def load_configs() -> Dict[str, ProjectConfig]:
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for v in data.values():
        v['localPath'] = decrypt_data(bytes.fromhex(v['localPath'])).decode('utf-8')
    return {k: ProjectConfig.from_dict(v) for k, v in data.items()}

def save_psync_file(spaceId: str, localRoot: str, encryptionKey: str, fileTypes: list, path: str):
    psync = {
        'spaceId': spaceId,
        'localRoot': localRoot,
        'encryptionKey': encryptionKey,
        'fileTypes': fileTypes
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(psync, f, indent=2)
