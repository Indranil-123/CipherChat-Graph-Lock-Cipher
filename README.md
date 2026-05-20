# CipherChat-Graph-Lock-Cipher


<div align="center">

```
 ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗  ██████╗██╗  ██╗ █████╗ ████████╗
██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗██╔════╝██║  ██║██╔══██╗╚══██╔══╝
██║     ██║██████╔╝███████║█████╗  ██████╔╝██║     ███████║███████║   ██║   
██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗██║     ██╔══██║██╔══██║   ██║   
╚██████╗██║██║     ██║  ██║███████╗██║  ██║╚██████╗██║  ██║██║  ██║   ██║   
 ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝  
```

### Real-Time Secure Messaging — Powered by a Custom Graph-Based Encryption Algorithm

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![WebSocket](https://img.shields.io/badge/WebSocket-native-FF6B6B?style=flat-square)](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow?style=flat-square)]()

</div>

---

## What is CipherChat?

CipherChat is a real-time encrypted messaging application built around **GraphLock** — a custom encryption algorithm designed entirely from scratch. GraphLock encodes plaintext onto a weighted graph structure and uses a secret Hamiltonian path as the encryption key.

> **Without the key, decryption requires solving the Hamiltonian Path problem — which is NP-complete.**

This is not a wrapper around AES or RSA. Every algorithm, every mathematical primitive, every cryptographic operation is hand-coded in pure Python. No `cryptography`, no `pycryptodome`, no shortcuts.

---

## The GraphLock Cipher

### Core Idea

```
Plaintext ──► Graph Encoding ──► Hamiltonian Traversal ──► Matrix Permutation ──► Ciphertext
                                        ▲
                                   Secret Key
                                (known path order)
```

### How It Works

**Encryption (fast, O(n²)):**
1. Each character maps to a node; positional relationships become weighted edges
2. Build an `n×n` adjacency matrix from the plaintext
3. Traverse nodes in a key-defined Hamiltonian path order
4. Apply permutation matrix shuffle (key-derived)
5. Apply modular arithmetic over a large prime field
6. Append a graph signature hash for integrity verification

**Decryption with key:** Reverse the permutation → reverse the traversal → decode the matrix → `O(n²)`

**Decryption without key:** Find the Hamiltonian path → `O(2ⁿ · n²)` — exponential. Infeasible for `n > 30`.

### Key Structure

```python
Key = (
    seed_graph,          # Base graph topology (n×n matrix)
    hamiltonian_path,    # Traversal order — the encryption route
    permutation_matrix,  # Row/column shuffle pattern
    mod_prime            # 256-bit prime for field operations
)
```

### Security Basis

| Attack Vector | Problem Class | Best Known | Practical? |
|---|---|---|---|
| Recover traversal order | NP-Complete (Hamiltonian Path) | `O(2ⁿ · n²)` | ✗ |
| Recover permutation | Exponential | `O(n!)` | ✗ |
| Graph isomorphism attack | GI-Complete | Sub-exponential | ✗ |
| Combined brute-force | NP-Hard | Unknown | ✗ |

> ⚠️ GraphLock is a **research-grade academic cipher**. It has not undergone formal cryptanalysis and should not be used in production security-critical systems.

---

## Project Structure

```
cipherchat/
│
├── cipher_engine/              ← The core — 100% from scratch, no crypto libs
│   ├── graph_encoder.py        # Plaintext → weighted adjacency matrix
│   ├── hamiltonian.py          # Backtracking Hamiltonian path finder
│   ├── permutation.py          # Matrix row/col shuffle operations
│   ├── modular_math.py         # Extended GCD, mod exp, Miller-Rabin primality
│   └── graph_hash.py           # Custom DFS-based integrity hash function
│
├── key_exchange/               ← Diffie-Hellman adapted for graph seed agreement
│   └── dh_graph.py             # Seed negotiation + key derivation
│
├── backend/                    ← FastAPI — routes ciphertext, never plaintext
│   ├── app/
│   │   ├── routers/            # auth.py, chat.py, keys.py
│   │   ├── websocket/          # manager.py, session.py
│   │   ├── models/             # user.py, message.py, key.py
│   │   └── auth/               # jwt.py, password.py
│   ├── config.py
│   └── main.py
│
├── frontend/                   ← React + Tailwind
│   └── src/
│       ├── components/         # ChatWindow, MessageBubble, KeyStatus
│       ├── crypto/             # graphlock_client.js (client-side encrypt/decrypt)
│       ├── hooks/              # useWebSocket, useKeyExchange
│       ├── pages/              # Login, Chat, KeyExchange
│       └── services/           # api.js, websocket.js
│
├── storage/                    ← PostgreSQL + Redis
│   ├── db.py                   # SQLAlchemy ORM
│   └── redis_client.py         # Session keys with TTL
│
├── infra/
│   ├── docker-compose.yml
│   └── Dockerfile
│
├── tests/
│   ├── test_graphlock.py
│   ├── test_hamiltonian.py
│   ├── test_api.py
│   └── test_websocket.py
│
└── README.md
```

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Cipher | Pure Python 3.11 | GraphLock — built from scratch |
| Backend | FastAPI | Message routing, auth, WebSocket |
| Real-time | WebSockets (native) | Bidirectional encrypted channel |
| Frontend | React 18 + Tailwind | Chat UI, key exchange visualizer |
| Cache | Redis | Session keys (TTL), WebSocket state |
| Database | PostgreSQL | Encrypted message history |
| Container | Docker + Compose | One-command local setup |

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker + Docker Compose

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/cipherchat.git
cd cipherchat
```

### 2. Set up environment

```bash
cp .env.example .env
# Edit .env — set DB_URL, REDIS_URL, SECRET_KEY
```

### 3. Start with Docker

```bash
docker-compose up --build
```

### 4. Run locally (dev mode)

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`

---

## Algorithms Implemented From Scratch

Every algorithm is hand-coded. No cryptographic libraries used.

```
cipher_engine/
│
├── modular_math.py
│   ├── extended_gcd(a, b)          # Euclidean algorithm — O(log n)
│   ├── mod_inverse(a, m)           # Modular multiplicative inverse
│   ├── fast_mod_exp(base, exp, m)  # Square-and-multiply — O(log exp)
│   └── miller_rabin(n, k)          # Probabilistic primality test — O(k·log²n)
│
├── graph_encoder.py
│   ├── text_to_graph(plaintext)    # Build weighted adjacency matrix
│   ├── graph_to_text(matrix, key)  # Reconstruct plaintext with key
│   └── serialize_matrix(matrix)    # Matrix → base64 ciphertext
│
├── hamiltonian.py
│   ├── find_path(graph, start)     # Backtracking path finder
│   ├── verify_path(graph, path)    # Validate a given path
│   └── path_from_seed(seed, n)     # Deterministic path from key seed
│
├── permutation.py
│   ├── permute_matrix(M, perm)     # Apply row/col permutation
│   ├── inverse_permutation(perm)   # Reverse the shuffle
│   └── generate_permutation(seed)  # Derive permutation from key seed
│
└── graph_hash.py
    ├── dfs_signature(graph)        # DFS traversal-based hash
    └── verify_integrity(ct, tag)   # Verify message was not tampered
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Alice (React)                        │
│   type message → GraphLock.encrypt(msg, key) → ciphertext  │
└────────────────────────────┬────────────────────────────────┘
                             │ WebSocket (TLS)
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
│          routes ciphertext — never sees plaintext           │
└────────────────────────────┬────────────────────────────────┘
                             │ WebSocket (TLS)
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                        Bob (React)                          │
│   receive ciphertext → GraphLock.decrypt(ct, key) → msg    │
└─────────────────────────────────────────────────────────────┘
```

Key exchange happens once at session start via Diffie-Hellman. After that, both sides encrypt/decrypt locally — the server only forwards ciphertext.

---

## Build Plan

| Week | Focus | Deliverable |
|---|---|---|
| 1 | Cipher core | `modular_math.py`, `graph_encoder.py` |
| 2 | Crypto algorithms | `hamiltonian.py`, `permutation.py`, full GraphLock |
| 3 | Key exchange + hash | `dh_graph.py`, `graph_hash.py` |
| 4 | Backend | FastAPI app, WebSocket manager, JWT auth |
| 5 | Frontend | React chat UI, key exchange visualizer |
| 6 | Hardening | Benchmarks, tests, docs, demo |

---

## Why This Exists

Standard encryption tutorials teach you to *use* AES. This project teaches you to *build* one.

By the end of this project you will have implemented:
- A novel cipher based on NP-complete graph problems
- Modular arithmetic from first principles (GCD, mod inverse, fast exp)
- A probabilistic primality test (Miller-Rabin)
- A real-time WebSocket system with end-to-end encryption
- A Diffie-Hellman key exchange (graph-adapted)

This is also a viable research paper topic — a custom cipher grounded in NP-hard problems with benchmarkable decryption complexity.

---

## Contributing

This is an educational/research project. Issues, improvements, and cryptanalysis attempts are welcome.

```bash
# Run tests
pytest tests/ -v

# Test the cipher directly
python -m cipher_engine.graph_encoder
```

---

## License

MIT — see [LICENSE](LICENSE)

---

<div align="center">

Built from scratch by **Indranil** · GraphLock Cipher · 2025

*Encrypt with graphs. Decrypt with math. Break with NP-completeness.*

</div>