from fastapi import FastAPI, HTTPException, UploadFile, File, Query, Response, Body
from mcp_server.config import load_config, MCPConfig
from mcp_server.security import is_allowed_path, validate_path
from mcp_server.audit_log import AuditLogger
from mcp_server.exec import exec_cmd_as_admin
from pathlib import Path
import os

CONFIG_PATH = 'mcp_server/config.json'
LOG_PATH = 'mcp_server/audit.log'
HMAC_KEY = b'secret_key'  # TODO: bezpečně načíst

app = FastAPI()
config: MCPConfig = load_config(CONFIG_PATH)
audit = AuditLogger(LOG_PATH, HMAC_KEY)

@app.get('/file')
def get_file(path: str = Query(...)):
    if not is_allowed_path(path, config.allowed_dirs) or not validate_path(path):
        audit.log('READ_DENIED', path)
        raise HTTPException(403, detail='Access denied')
    if not os.path.isfile(path):
        raise HTTPException(404, detail='File not found')
    audit.log('READ', path)
    with open(path, 'rb') as f:
        content = f.read()
    return Response(content, media_type='application/octet-stream')

@app.post('/file')
def post_file(path: str = Query(...), file: UploadFile = File(...)):
    if not config.enable_write:
        raise HTTPException(403, detail='Write disabled')
    if not is_allowed_path(path, config.allowed_dirs) or not validate_path(path):
        audit.log('WRITE_DENIED', path)
        raise HTTPException(403, detail='Access denied')
    content = file.file.read()
    if len(content) > config.max_file_size:
        raise HTTPException(413, detail='File too large')
    with open(path, 'wb') as f:
        f.write(content)
    audit.log('WRITE', path)
    return {'status': 'ok'}

@app.get('/list')
def list_dir(dir: str = Query(...)):
    if not is_allowed_path(dir, config.allowed_dirs) or not validate_path(dir):
        audit.log('LIST_DENIED', dir)
        raise HTTPException(403, detail='Access denied')
    if not os.path.isdir(dir):
        raise HTTPException(404, detail='Directory not found')
    audit.log('LIST', dir)
    return {'files': os.listdir(dir)}

@app.post('/exec')
def exec_cmd(command: str = Body(...), cwd: str = Body(None)):
    result = exec_cmd_as_admin(command, cwd)
    audit.log('EXEC', command)
    if 'error' in result:
        raise HTTPException(403, detail=result['error'])
    return result
