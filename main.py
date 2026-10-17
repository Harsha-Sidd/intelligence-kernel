
from pathlib import Path

from core.engine import KernelEngine
from memory.memory_store import MemoryStore


ROOT = Path(__file__).resolve().parent
MEMORY_FILE = ROOT / "memory" / "memory.json"

VERSION = "0.6.0"


def print_banner():
    print("=" * 42)
    print(f"       INTELLIGENCE KERNEL v{VERSION}")
    print("=" * 42)
    print("Type 'help' to see available commands.")
    print("Type 'exit' or 'quit' to end the session.")
    print("")


def main():
    memory = MemoryStore(MEMORY_FILE)
    engine = KernelEngine(memory)

    print_banner()

    while True:
        try:
            command = input("You > ")
        except (EOFError, KeyboardInterrupt):
            print("\nKernel > Session ended.")
            break

        # Ignore blank input without invoking the engine.
        if not command.strip():
            continue

        try:
            status, response, explanation = engine.process(command)
        except Exception as error:
            # Keep unexpected command failures from crashing the session.
            print("Kernel > An internal error occurred.")
            print(f"[ERROR] {type(error).__name__}")
            continue

        print(f"Kernel > {response}")
        print(f"[{status}] {explanation}")

        if status == "EXIT":
            break

    print("Intelligence Kernel session closed.")


if __name__ == "__main__":
    main()

