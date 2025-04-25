import os
from pathlib import Path
import hashlib
import json
from typing import List

CACHE_PATH = os.path.join(os.environ.get('APPDATA', ''), 'PerplexitySync', 'codebase_cache.json')

def get_codebase_snapshot(root: str, file_types: List[str], max_file_size=100_000) -> dict:
    codebase = {}
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if any(fname.endswith(ext) for ext in file_types):
                fpath = os.path.join(dirpath, fname)
                try:
                    if os.path.getsize(fpath) > max_file_size:
                        continue
                    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                        codebase[os.path.relpath(fpath, root)] = f.read()
                except Exception:
                    continue
    return codebase

def codebase_hash(codebase: dict) -> str:
    m = hashlib.sha256()
    for k in sorted(codebase.keys()):
        m.update(k.encode('utf-8'))
        m.update(codebase[k].encode('utf-8'))
    return m.hexdigest()

def get_or_cache_codebase(root: str, file_types: List[str]) -> dict:
    codebase = get_codebase_snapshot(root, file_types)
    h = codebase_hash(codebase)
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, 'r', encoding='utf-8') as f:
            cache = json.load(f)
        if cache.get('hash') == h:
            return cache['codebase']
    with open(CACHE_PATH, 'w', encoding='utf-8') as f:
        json.dump({'hash': h, 'codebase': codebase}, f)
    return codebase

def inject_codebase_to_query(query: str, root: str, file_types: List[str]) -> str:
    codebase = get_or_cache_codebase(root, file_types)
    codebase_str = '\n'.join([f'## {k}\n```\n{v}\n```\n' for k, v in codebase.items()])
    return f'{query}\n\n[CODEBASE CONTEXT]\n{codebase_str}'
