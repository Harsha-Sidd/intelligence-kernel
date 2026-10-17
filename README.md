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

## Version 0.3

Version 0.3 improves memory management, input validation, and deletion safety.

### Memory features

- **Remember:** Store a key-value entry.
- **Update:** Change the value of an existing entry.
- **Recall:** Retrieve an entry by its exact key.
- **Search:** Find entries by matching text in their keys or values.
- **List:** Display stored memory keys.
- **Forget:** Request deletion of an entry, with explicit confirmation.
- **Cancel deletion:** Cancel a pending deletion without removing the entry.
- **Input validation:** Reject empty keys, empty values, and invalid commands.
- **Memory validation:** Ignore malformed entries when loading stored memory.
- **Persistence:** Save memory locally in JSON format.
- **Safer saving:** Write to a temporary file before replacing the memory file.

### Commands

Run the program:

    python main.py

Available commands:

    help
    remember KEY = VALUE
    update KEY = VALUE
    recall KEY
    search TEXT
    list
    forget KEY
    confirm
    cancel
    exit

Example session:

    remember project = Intelligence Kernel
    update project = Intelligence Kernel v0.3
    recall project
    search intelligence
    forget project
    cancel
    exit

After `forget KEY`, type `confirm` to delete the entry or `cancel` to preserve it.

### Testing

Run the automated test suite:

    python -m unittest discover -s tests -v

The v0.3 test suite contains 15 tests covering persistence, validation, updates, duplicate entries, deletion confirmation, search, and malformed memory entries.

### Local memory and privacy

Personal memory is stored locally in `memory/memory.json`. This file is excluded from Git tracking through `.gitignore` and should not be committed to the public repository.

### Project status

Version 0.3 is a rule-based Python prototype. It is an early foundation for a larger, independently developed assistant; it is not yet a trained language model or a general-purpose conversational AI.

## Version 0.3

Version 0.3 improves memory management, input validation, and deletion safety.

### Memory features

- **Remember:** Store a key-value entry.
- **Update:** Change the value of an existing entry.
- **Recall:** Retrieve an entry by its exact key.
- **Search:** Find entries by matching text in their keys or values.
- **List:** Display stored memory keys.
- **Forget:** Request deletion of an entry, with explicit confirmation.
- **Cancel deletion:** Cancel a pending deletion without removing the entry.
- **Input validation:** Reject empty keys, empty values, and invalid commands.
- **Memory validation:** Ignore malformed entries when loading stored memory.
- **Persistence:** Save memory locally in JSON format.
- **Safer saving:** Write to a temporary file before replacing the memory file.

### Commands

Run the program:

    python main.py

Available commands:

    help
    remember KEY = VALUE
    update KEY = VALUE
    recall KEY
    search TEXT
    list
    forget KEY
    confirm
    cancel
    exit

Example session:

    remember project = Intelligence Kernel
    update project = Intelligence Kernel v0.3
    recall project
    search intelligence
    forget project
    cancel
    exit

After `forget KEY`, type `confirm` to delete the entry or `cancel` to preserve it.

### Testing

Run the automated test suite:

    python -m unittest discover -s tests -v

The v0.3 test suite contains 15 tests covering persistence, validation, updates, duplicate entries, deletion confirmation, search, and malformed memory entries.

### Local memory and privacy

Personal memory is stored locally in `memory/memory.json`. This file is excluded from Git tracking through `.gitignore` and should not be committed to the public repository.

### Project status

Version 0.3 is a rule-based Python prototype. It is an early foundation for a larger, independently developed assistant; it is not yet a trained language model or a general-purpose conversational AI.

## Version 0.3

Version 0.3 improves memory management, input validation, and deletion safety.

### Memory features

- **Remember:** Store a key-value entry.
- **Update:** Change the value of an existing entry.
- **Recall:** Retrieve an entry by its exact key.
- **Search:** Find entries by matching text in their keys or values.
- **List:** Display stored memory keys.
- **Forget:** Request deletion of an entry, with explicit confirmation.
- **Cancel deletion:** Cancel a pending deletion without removing the entry.
- **Input validation:** Reject empty keys, empty values, and invalid commands.
- **Memory validation:** Ignore malformed entries when loading stored memory.
- **Persistence:** Save memory locally in JSON format.
- **Safer saving:** Write to a temporary file before replacing the memory file.

### Commands

Run the program:

    python main.py

Available commands:

    help
    remember KEY = VALUE
    update KEY = VALUE
    recall KEY
    search TEXT
    list
    forget KEY
    confirm
    cancel
    exit

Example session:

    remember project = Intelligence Kernel
    update project = Intelligence Kernel v0.3
    recall project
    search intelligence
    forget project
    cancel
    exit

After `forget KEY`, type `confirm` to delete the entry or `cancel` to preserve it.

### Testing

Run the automated test suite:

    python -m unittest discover -s tests -v

The v0.3 test suite contains 15 tests covering persistence, validation, updates, duplicate entries, deletion confirmation, search, and malformed memory entries.

### Local memory and privacy

Personal memory is stored locally in `memory/memory.json`. This file is excluded from Git tracking through `.gitignore` and should not be committed to the public repository.

### Project status

Version 0.3 is a rule-based Python prototype. It is an early foundation for a larger, independently developed assistant; it is not yet a trained language model or a general-purpose conversational AI.
