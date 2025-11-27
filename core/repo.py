from pathlib import Path
from typing import Optional
from utils.hash import sha256
import json

VCS_DIRNAME = ".vcs"

def repo_path(path='.') -> Path:
    return Path(path) / VCS_DIRNAME

def init_repo(path='.'):
    vcs = repo_path(path)
    (vcs / 'objects').mkdir(parents=True, exist_ok=True)
    (vcs / 'packs').mkdir(parents=True, exist_ok=True)
    (vcs / 'refs' / 'heads').mkdir(parents=True, exist_ok=True)
    (vcs / 'refs' / 'tags').mkdir(parents=True, exist_ok=True)
    head = vcs / 'HEAD'
    if not head.exists(): head.write_text('refs/heads/main')
    main_ref = vcs / 'refs' / 'heads' / 'main'
    if not main_ref.exists(): main_ref.write_text('null')
    log = vcs / 'log.json'
    if not log.exists(): log.write_text(json.dumps({}))
    return vcs

def read_ref(path='.', ref='HEAD') -> Optional[str]:
    vcs = repo_path(path)
    f = vcs / ref
    if not f.exists(): return None
    return f.read_text().strip()

def update_ref(path='.', ref_name='refs/heads/main', value='null'):
    vcs = repo_path(path)
    target = vcs / ref_name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(value)

def store_object(data: bytes, path='.') -> str:
    vcs = repo_path(path)
    h = sha256(data)
    obj_path = vcs / 'objects' / h
    if not obj_path.exists():
        obj_path.parent.mkdir(parents=True, exist_ok=True)
        obj_path.write_bytes(data)
    return h

def get_object(h: str, path='.') -> Optional[bytes]:
    vcs = repo_path(path)
    obj_path = vcs / 'objects' / h
    if obj_path.exists(): return obj_path.read_bytes()
    return None

def append_log(path='.', commit_hash=None, meta=None):
    vcs = repo_path(path)
    logf = vcs / 'log.json'
    data = json.loads(logf.read_text()) if logf.exists() else {}
    data[commit_hash] = meta or {}
    logf.write_text(json.dumps(data, indent=2))

def list_objects(path='.'):
    vcs = repo_path(path)
    objs = []
    objdir = vcs / 'objects'
    if objdir.exists():
        for p in objdir.iterdir(): objs.append(p.name)
    return objs
