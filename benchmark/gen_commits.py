import os, time, json
from core.repo import init_repo, repo_path
from utils.pack import build_pack, pack_size

def run(n=500):
    if os.path.exists('.vcs'): import shutil; shutil.rmtree('.vcs')
    init_repo('.')
    fname='data.txt'
    with open(fname,'w') as f: f.write('line\n'*200)
    times=[]
    for i in range(n):
        with open(fname,'a') as f: f.write(f'update {i}\n')
        t0=time.time()
        os.system('python3 cli.py commit -m "auto %d"' % i)
        t1=time.time(); times.append(t1-t0)
    p=build_pack('.','bench.pack')
    naive = 0
    objdir = repo_path('.')/'objects'
    if objdir.exists():
        for pth in objdir.iterdir(): naive += pth.stat().st_size
    stats = {'n':n, 'avg_commit_s': sum(times)/len(times), 'naive_size': naive, 'pack_size': pack_size('.')}
    with open('benchmark_results.json','w') as f: json.dump(stats,f,indent=2)
    print('done', stats)

if __name__=='__main__':
    run(200)
