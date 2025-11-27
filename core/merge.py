import json, difflib
from core.commit import get_commit, create_commit
from core.repo import get_object, store_object
from core.graph import find_merge_base

def three_way_merge(path='.', a=None, b=None, message='Merge commit'):
    base = find_merge_base(path, a, b)
    def load_tree(ch):
        if not ch: return {}
        obj = get_commit(path, ch)
        if not obj: return {}
        th = obj.get('tree')
        if not th: return {}
        data = get_object(th, path)
        if not data: return {}
        return json.loads(data.decode())
    bt = load_tree(base)
    at = load_tree(a)
    bt2 = load_tree(b)
    merged={}
    files = set(list(bt.keys())+list(at.keys())+list(bt2.keys()))
    for f in files:
        base_h = bt.get(f)
        a_h = at.get(f)
        b_h = bt2.get(f)
        if a_h==b_h:
            merged[f]=a_h
        elif a_h==base_h:
            merged[f]=b_h
        elif b_h==base_h:
            merged[f]=a_h
        else:
            a_bytes = get_object(a_h, path) or b''
            b_bytes = get_object(b_h, path) or b''
            merged_content = b'<<<<<<< A\n' + a_bytes + b'=======\n' + b_bytes + b'>>>>>>> B\n'
            h = store_object(merged_content, path)
            merged[f]=h
    tree_ser = json.dumps(merged, sort_keys=True).encode()
    tree_h = store_object(tree_ser, path)
    parents=[a,b]
    ch = create_commit(path, tree_h, parents=parents, message=message)
    return ch
