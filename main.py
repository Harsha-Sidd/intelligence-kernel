
from core.config import APP_NAME, VERSION, MEMORY_FILE
from core.engine import KernelEngine
from core.logging_setup import configure_logging
from core.response import KernelResponse
from memory.memory_store import MemoryStore


def print_banner():
    print("=" * 42)
    print(f"       {APP_NAME.upper()} v{VERSION}")
    print("=" * 42)
    print("Type 'help' to see available commands.")
    print("Type 'exit' or 'quit' to end the session.")
    print()


def main():
    logger = configure_logging()
    logger.info("Session started")

    try:
        memory = MemoryStore(MEMORY_FILE)
        engine = KernelEngine(memory)

        print_banner()

        while True:
            try:
                command = input("You > ")
            except (EOFError, KeyboardInterrupt):
                print("\nKernel > Session ended.")
                break

            if not command.strip():
                continue

            try:
                result: KernelResponse = engine.process_structured(command)
            except Exception as error:
                logger.error(
                    "Command processing failed: %s",
                    type(error).__name__,
                )
                print("Kernel > An internal error occurred.")
                print(f"[ERROR] {type(error).__name__}")
                continue

            print(f"Kernel > {result.message}")
            print(f"[{result.status}] {result.explanation}")

            if result.status == "EXIT":
                break

    except Exception as error:
        logger.error(
            "Application startup or session failure: %s",
            type(error).__name__,
        )
        print("Kernel > The application encountered an internal error.")

    finally:
        logger.info("Session ended")
        print("Intelligence Kernel session closed.")


if __name__ == "__main__":
    main()

