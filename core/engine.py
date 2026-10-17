class KernelEngine:
    def __init__(self, memory):
        self.memory = memory

    def process(self, command):
        command = command.strip()
        normalized = command.casefold()

        if normalized in {"exit", "quit"}:
            return "EXIT", "Session ended.", "Exit command matched."

        if normalized == "help":
            return (
                "OK",
                "Commands: help, remember KEY = VALUE, recall KEY, list, exit",
                "Help rule matched.",
            )

        if normalized.startswith("remember "):
            entry = command[len("remember "):]

            if "=" not in entry:
                return "ERROR", "Use: remember KEY = VALUE", "Missing '=' separator."

            key, value = entry.split("=", 1)
            key, value = key.strip(), value.strip()

            if not key or not value:
                return "ERROR", "Key and value cannot be empty.", "Validation failed."

            self.memory.remember(key, value)
            return "OK", f"Stored: {key}", "Memory updated and saved."

        if normalized.startswith("recall "):
            key = command[len("recall "):].strip()

            if not key:
                return "ERROR", "Provide a key to recall.", "Empty key."

            item = self.memory.recall(key)

            if item is not None:
                return "OK", f"{key} = {item['value']}", "Exact key matched."

            return "NOT_FOUND", f"No memory found for: {key}", "No exact key matched."

        if normalized == "list":
            keys = self.memory.list_keys()
            return (
                "OK",
                ", ".join(keys) if keys else "Memory is empty.",
                "Memory keys listed.",
            )

        return "UNKNOWN", "I don't have a rule for that yet. Type 'help'.", "No rule matched."
