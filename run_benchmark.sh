#!/bin/bash
python3 -m venv venv || true
source venv/bin/activate
pip install -r requirements.txt
python benchmark/gen_commits.py
cat benchmark_results.json
