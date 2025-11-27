from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json, time
from core.repo import init_repo, store_object, read_ref, update_ref, repo_path
from core.commit import create_commit

app = FastAPI(title='mini-git full API')
class CommitRequest(BaseModel):
    message: str
    files: dict

@app.post('/repo/init')
def api_init():
    init_repo('.'); return {'ok':True}

@app.post('/repo/commit')
def api_commit(req: CommitRequest):
    vcs = repo_path('.')
    if not vcs.exists(): raise HTTPException(status_code=400, detail='no repo')
    file_hashes={}
    for k,v in req.files.items():
        b = v.encode() if isinstance(v,str) else v
        h = store_object(b,'.'); file_hashes[k]=h
    tree_ser = json.dumps(file_hashes, sort_keys=True).encode()
    tree_h = store_object(tree_ser,'.')
    parent = read_ref('.'); parents=[parent] if parent and parent!='null' else []
    ch = create_commit('.', tree_h, parents=parents, message=req.message)
    update_ref('.', 'refs/heads/main', ch)
    return {'commit': ch, 'time_ms': int(time.time()*1000)}
