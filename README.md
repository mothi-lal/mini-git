mini-git: Lightweight Version Control Engine with Packfile Compression
=====================
mini-git is a compact, production-style version-control engine inspired by Git’s internal architecture.
It implements content-addressed storage, commit DAGs, branching, merging, and an optimised packfile system for storage reduction.
The project includes:
Custom object store (SHA-256 addressed)
Branching + merge commits
Packfile-based delta compression
API (FastAPI) for remote commit ingestion
CLI tools (init, commit, log, repack)
Benchmark suite to evaluate storage + performance

**Features**
1. **Content-Addressed Storage**
Every blob, tree, and commit object is stored by SHA-256.
Identical content is deduplicated automatically.
2. **Commit Objects + History DAG**
Each commit stores:
Tree hash
Parent commit(s)
Commit message
DAG supports branching & merging.
3. **Packfile Compression (Core Innovation)**
Implements a simplified Git-style packfile with:
Zlib compression
Metadata headers
Loose-object cleanup
Single-pack concatenation of all blobs

**Benchmark Result (200 Commits)**
| Metric                  | Value             |
| ----------------------- | ----------------- |
| Naive loose-object size | **585,199 bytes** |
| Packfile size           | **224,704 bytes** |
| **Total reduction**     | **61.6%**         |


**Benchmarks**
Run the benchmark from project root: python -m benchmark.compare_pack

This generates benchmark_compare.json: {
                                          "n_commits": 200,
                                          "naive_bytes": 585199,
                                          "pack_bytes": 224704,
                                          "reduction_pct": 61.6
                                      }

**CLI Usage**

Initialise a repository:  python cli.py init

Create a file and commit: echo "hello" > hello.txt
                          python cli.py commit -m "first commit"

View commit graph: python cli.py log --graph

Repack repository (optimise storage): python cli.py repack

**API (FastAPI)**

Run server: uvicorn api.server:app --reload

Open interactive docs: http://127.0.0.1:8000/docs


**Endpoints**

POST /repo/init
POST /repo/commit

**Architecture Overview**

mini_git/
├── api/                # FastAPI server for remote operations
├── core/
│   ├── repo.py         # object store, refs, HEAD, logging
│   ├── commit.py       # commit creation + serialization
│   ├── graph.py        # DAG traversal, merge-base logic
│   └── merge.py        # three-way merge
├── utils/
│   ├── hash.py         # SHA256 utilities
│   └── pack.py         # zlib packfile generator
├── benchmark/          # synthetic load generators
├── cli.py              # command-line interface
└── README.md

**Technologies Used**

Python 3.11
FastAPI
Uvicorn
Zlib compression
SHA-256 hashing
Custom filesystem-based storage

**Packaging & Deployment**

Build Docker container: docker build -t mini-git
                        docker run -p 8000:8000 mini-git


**Author**

Mothial Jadhav


