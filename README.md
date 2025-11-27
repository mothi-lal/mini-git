mini-git full upgrade
=====================
Quick:
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  python cli.py init
  echo hello > hello.txt
  python cli.py commit -m "first"
  python benchmark/gen_commits.py
