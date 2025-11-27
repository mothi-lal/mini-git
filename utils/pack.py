import zlib, json
from core.repo import repo_path
def build_pack(path='.', pack_name=None):
    vcs = repo_path(path)
    objdir = vcs / 'objects'
    payload = b''
    count=0
    if objdir.exists():
        for p in objdir.iterdir():
            h = p.name
            data = p.read_bytes()
            comp = zlib.compress(data)
            meta = json.dumps({'h':h,'len':len(comp)}).encode()
            payload += meta + b'\n' + comp + b'\n---\n'
            count+=1
    if not pack_name:
        pack_name = f'pack_{count}.pack'
    pf = vcs / 'packs' / pack_name
    pf.write_bytes(payload)
    # remove loose objects (simulate repack)
    for p in list(objdir.iterdir()):
        try: p.unlink()
        except: pass
    return str(pf)

def pack_size(path='.'):
    vcs = repo_path(path)
    total=0
    for p in (vcs/'packs').iterdir():
        total+=p.stat().st_size
    return total
