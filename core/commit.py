import json
from typing import List
from utils.hash import sha256
from core.repo import store_object, append_log, read_ref, get_object

def make_tree_from_files(files: dict) -> bytes:
    return json.dumps(files, sort_keys=True).encode()

def create_commit(path='.', tree_hash=None, parents: List[str]=None, message=''):
    parents = parents or []
    commit_obj = {'tree': tree_hash, 'parents': parents, 'message': message}
    ser = json.dumps(commit_obj, sort_keys=True).encode()
    ch = sha256(ser)
    store_object(ser, path)
    append_log(path, ch, commit_obj)
    return ch

def get_commit(path='.', commit_hash=None):
    if commit_hash is None:
        head = read_ref(path)
        if head in (None, 'null'): return None
        commit_hash = head
    data = get_object(commit_hash, path)
    if data is None: return None
    return json.loads(data.decode())
