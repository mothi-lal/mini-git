import argparse, os, json
from core.repo import init_repo, store_object, update_ref, read_ref, repo_path
from core.commit import create_commit
from core.graph import build_graph_lines
from utils.pack import build_pack, pack_size

parser = argparse.ArgumentParser(prog='mini-git')
sub = parser.add_subparsers(dest='cmd')

sub.add_parser('init')
sub_commit = sub.add_parser('commit'); sub_commit.add_argument('-m','--message', default='commit')
sub_branch = sub.add_parser('branch'); sub_branch.add_argument('name')
sub_log = sub.add_parser('log'); sub_log.add_argument('--graph', action='store_true')
sub_repack = sub.add_parser('repack')

args = parser.parse_args()
if args.cmd=='init':
    init_repo('.'); print('repo initialized')
elif args.cmd=='commit':
    files={}
    for fname in os.listdir('.'):
        if fname.startswith('.') or fname=='mini_git_full_upgrade': continue
        if os.path.isdir(fname): continue
        with open(fname,'rb') as f: data=f.read()
        h=store_object(data,'.'); files[fname]=h
    tree_ser=json.dumps(files, sort_keys=True).encode()
    tree_h=store_object(tree_ser,'.')
    parent=read_ref('.')
    parents=[parent] if parent and parent!='null' else []
    ch=create_commit('.', tree_h, parents=parents, message=args.message)
    update_ref('.', 'refs/heads/main', ch)
    print('Committed', ch)
elif args.cmd=='branch':
    vcs = repo_path('.'); (vcs / 'refs' / 'heads' / args.name).write_text(read_ref('.')); print('branch created')
elif args.cmd=='log':
    head=read_ref('.')
    if args.graph: print(build_graph_lines('.', head))
    else: print('HEAD->', head)
elif args.cmd=='repack':
    p=build_pack('.'); print('pack created', p, 'size', pack_size('.'))
else:
    print('commands: init commit branch log repack')
