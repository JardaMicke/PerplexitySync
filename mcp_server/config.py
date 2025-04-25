import json
from pathlib import Path
from pydantic import BaseModel, ValidationError

class MCPConfig(BaseModel):
    allowed_dirs: list[str]
    max_file_size: int
    enable_write: bool

def load_config(config_path: str) -> MCPConfig:
    with open(config_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return MCPConfig(**data)
