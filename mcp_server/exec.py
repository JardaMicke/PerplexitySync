import subprocess
import os
import shlex
from mcp_server.audit_log import AuditLogger
from mcp_server.config import load_config

CONFIG_PATH = 'mcp_server/config.json'
LOG_PATH = 'mcp_server/audit.log'
HMAC_KEY = b'secret_key'

SAFE_COMMANDS = [
    'dir', 'echo', 'type', 'python', 'pip', 'git', 'pytest', 'pytest.exe', 'python.exe', 'build.bat', 'test.bat'
]

def is_safe_command(cmd: str) -> bool:
    parts = shlex.split(cmd)
    base = os.path.basename(parts[0]).lower() if parts else ''
    return base in SAFE_COMMANDS

def exec_cmd_as_admin(command: str, cwd: str = None) -> dict:
    if not is_safe_command(command):
        return {'error': 'Command not allowed'}
    try:
        completed = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=cwd)
        return {
            'stdout': completed.stdout,
            'stderr': completed.stderr,
            'returncode': completed.returncode
        }
    except Exception as e:
        return {'error': str(e)}
