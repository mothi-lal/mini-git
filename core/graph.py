from core.commit import get_commit
def ancestors(path='.', commit_hash=None):
    if commit_hash is None: return set()
    visited=set()
    stack=[commit_hash]
    while stack:
        c=stack.pop()
        if c in visited: continue
        visited.add(c)
        obj = get_commit(path, c)
        if obj:
            for p in obj.get('parents',[]): stack.append(p)
    return visited

def find_merge_base(path='.', a=None, b=None):
    if not a or not b: return None
    an=ancestors(path,a)
    bn=ancestors(path,b)
    commons=an.intersection(bn)
    return sorted(list(commons))[0] if commons else None

def build_graph_lines(path='.', head=None):
    lines=[]
    seen=set()
    def walk(c, depth=0):
        if not c or c in seen: return
        seen.add(c)
        obj = get_commit(path, c)
        if not obj: return
        lines.append('  '*depth + f'* {c[:8]} - {obj.get("message","")}')
        for p in obj.get('parents',[]):
            walk(p, depth+1)
    walk(head, 0)
    return '\n'.join(lines)
