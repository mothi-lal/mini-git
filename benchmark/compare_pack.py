# benchmark/compare_pack.py
import os, json, time
from pathlib import Path
from core.repo import init_repo, repo_path
from utils.pack import build_pack, pack_size

def folder_bytes(path: Path) -> int:
    total = 0
    if not path.exists():
        return 0
    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            total += os.path.getsize(fp)
    return total

def run(n=200):
    # Clean old repo
    if os.path.exists('.vcs'):
        import shutil
        shutil.rmtree('.vcs')

    init_repo('.')

    # base file
    fname = 'data.txt'
    with open(fname, 'w') as f:
        f.write('line\n' * 200)

    # Generate commits
    for i in range(n):
        with open(fname, 'a') as f:
            f.write(f'update {i}\n')
        os.system(f'python3 cli.py commit -m "auto {i}"')

    # 1. Measure naive loose-object size BEFORE repack
    naive_bytes = folder_bytes(Path('.vcs/objects'))

    # 2. Build pack (this deletes loose objects)
    build_pack('.', 'comparison.pack')

    # 3. Measure pack size
    pack_bytes = folder_bytes(Path('.vcs/packs'))

    # 4. Compute reduction
    reduction = None
    if naive_bytes > 0:
        reduction = round((1 - pack_bytes / naive_bytes) * 100, 2)

    out = {
        'n_commits': n,
        'naive_bytes': naive_bytes,
        'pack_bytes': pack_bytes,
        'reduction_pct': reduction
    }

    with open('benchmark_compare.json', 'w') as f:
        json.dump(out, f, indent=2)

    print("DONE:", out)

if __name__ == "__main__":
    run(200)
