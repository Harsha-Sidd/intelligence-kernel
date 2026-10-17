# Intelligence Kernel

An experimental intelligence system built from scratch, exploring rule-based processing, persistent memory, and future learning algorithms.

## Current Version

**v0.2 — Modular architecture**

## Current Features

- Command-based interaction
- Rule-based command processing
- Persistent local memory stored as JSON
- Memory retrieval and key listing
- Input validation and basic error handling
- Automated tests using Python's built-in unittest framework

## Architecture

```text
IntelligenceKernel/
├── core/
│   ├── __init__.py
│   └── engine.py
├── memory/
│   ├── __init__.py
│   ├── memory_store.py
│   └── memory.json
├── tests/
│   ├── __init__.py
│   └── test_kernel.py
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

- `core/engine.py` processes commands and coordinates responses.
- `memory/memory_store.py` manages persistent memory.
- `main.py` starts the interactive session.
- `tests/` contains automated tests.

## Requirements

- Python 3.10 or newer
- No external Python packages are currently required.

## Run

```bash
python main.py
```

## Available Commands

| Command | Purpose |
|---|---|
| `help` | Display available commands |
| `remember KEY = VALUE` | Store a value |
| `recall KEY` | Retrieve a value |
| `list` | List stored keys |
| `exit` | End the session |

## Run Tests

```bash
python -m unittest discover -s tests -v
```

## Data and Privacy

Memory is stored locally in `memory/memory.json`. The `.gitignore` file excludes this runtime data from Git. Do not store passwords, tokens, or other secrets in the kernel's memory.

## Project Status

This is an early-stage experimental project. The current implementation uses explicit rules and persistent storage; it is not yet a general-purpose AI system. Learning and reasoning capabilities remain future development goals.

## License

No license has been selected yet. Until a license is added, the project remains subject to applicable copyright law.
