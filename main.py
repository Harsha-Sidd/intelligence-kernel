import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
MEMORY_FILE = ROOT / "memory" / "memory.json"


def load_memory():
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not MEMORY_FILE.exists():
        return {}

    try:
        return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        print("Warning: Memory could not be read.")
        return {}


def save_memory(memory):
    temporary = MEMORY_FILE.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(memory, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    temporary.replace(MEMORY_FILE)


def process(command, memory):
    command = command.strip()
    normalized = command.casefold()

    if normalized in {"exit", "quit"}:
        return "EXIT", "Session ended.", "Exit command matched."

    if normalized == "help":
        return "OK", "Commands: help, remember KEY = VALUE, recall KEY, list, exit", "Help rule matched."

    if normalized.startswith("remember "):
        entry = command[len("remember "):]

        if "=" not in entry:
            return "ERROR", "Use: remember KEY = VALUE", "Missing '=' separator."

        key, value = entry.split("=", 1)
        key, value = key.strip(), value.strip()

        if not key or not value:
            return "ERROR", "Key and value cannot be empty.", "Validation failed."

        memory[key] = {
            "value": value,
            "updated_at": datetime.now().astimezone().isoformat(),
        }
        save_memory(memory)
        return "OK", f"Stored: {key}", "Memory updated and saved."

    if normalized.startswith("recall "):
        key = command[len("recall "):].strip()

        if key in memory:
            return "OK", f"{key} = {memory[key]['value']}", "Exact key matched."

        return "NOT_FOUND", f"No memory found for: {key}", "No exact key matched."

    if normalized == "list":
        keys = sorted(memory)
        return "OK", ", ".join(keys) if keys else "Memory is empty.", "Memory keys listed."

    return "UNKNOWN", "I don't have a rule for that yet. Type 'help'.", "No rule matched."


def main():
    memory = load_memory()
    print("Intelligence Kernel v0.1")
    print("Type 'help' for commands.")

    while True:
        try:
            command = input("\nYou > ")
        except (EOFError, KeyboardInterrupt):
            print("\nSession ended.")
            break

        status, response, explanation = process(command, memory)
        print(f"Kernel > {response}")
        print(f"[{status}] {explanation}")

        if status == "EXIT":
            break


if __name__ == "__main__":
    main()
