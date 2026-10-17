from pathlib import Path

from core.engine import KernelEngine
from memory.memory_store import MemoryStore


ROOT = Path(__file__).resolve().parent
MEMORY_FILE = ROOT / "memory" / "memory.json"


def main():
    memory = MemoryStore(MEMORY_FILE)
    engine = KernelEngine(memory)

    print("Intelligence Kernel v0.2")
    print("Type 'help' for commands.")

    while True:
        try:
            command = input("\nYou > ")
        except (EOFError, KeyboardInterrupt):
            print("\nSession ended.")
            break

        status, response, explanation = engine.process(command)

        print(f"Kernel > {response}")
        print(f"[{status}] {explanation}")

        if status == "EXIT":
            break


if __name__ == "__main__":
    main()
