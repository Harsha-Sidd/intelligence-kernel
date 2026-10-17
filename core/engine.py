class KernelEngine:
    def __init__(self, memory):
        self.memory = memory
        self.pending_forget = None

    def process(self, command):
        command = command.strip()
        normalized = command.casefold()

        # Handle a pending deletion before any other command.
        if self.pending_forget is not None:
            if normalized == "confirm":
                key = self.pending_forget
                self.pending_forget = None

                if self.memory.forget(key):
                    return "OK", f"Forgot: {key}", "Confirmed deletion."

                return "NOT_FOUND", f"No memory found for: {key}", "Key no longer exists."

            if normalized == "cancel":
                key = self.pending_forget
                self.pending_forget = None
                return "OK", f"Deletion cancelled: {key}", "Deletion was cancelled."

            return (
                "CONFIRMATION_REQUIRED",
                "Type 'confirm' to delete or 'cancel' to keep the entry.",
                "Deletion is awaiting confirmation.",
            )

        if normalized in {"exit", "quit"}:
            return "EXIT", "Session ended.", "Exit command matched."

        if normalized == "help":
            return (
                "OK",
                "Commands: help, remember KEY = VALUE, update KEY = VALUE, "
                "recall KEY, forget KEY, search TEXT, list, exit",
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

            if self.memory.recall(key) is not None:
                return (
                    "EXISTS",
                    f"Memory already exists: {key}. Use update to change it.",
                    "Duplicate key rejected.",
                )

            self.memory.remember(key, value)
            return "OK", f"Stored: {key}", "Memory saved."

        if normalized.startswith("update "):
            entry = command[len("update "):]

            if "=" not in entry:
                return "ERROR", "Use: update KEY = VALUE", "Missing '=' separator."

            key, value = entry.split("=", 1)
            key, value = key.strip(), value.strip()

            if not key or not value:
                return "ERROR", "Key and value cannot be empty.", "Validation failed."

            if not self.memory.update(key, value):
                return "NOT_FOUND", f"No memory found for: {key}", "Update target missing."

            return "OK", f"Updated: {key}", "Existing memory updated."

        if normalized.startswith("recall "):
            key = command[len("recall "):].strip()

            if not key:
                return "ERROR", "Provide a key to recall.", "Empty key."

            item = self.memory.recall(key)

            if item is not None:
                return "OK", f"{key} = {item['value']}", "Exact key matched."

            return "NOT_FOUND", f"No memory found for: {key}", "No exact key matched."

        if normalized.startswith("forget "):
            key = command[len("forget "):].strip()

            if not key:
                return "ERROR", "Provide a key to forget.", "Empty key."

            if self.memory.recall(key) is None:
                return "NOT_FOUND", f"No memory found for: {key}", "No exact key matched."

            self.pending_forget = key
            return (
                "CONFIRMATION_REQUIRED",
                f"Delete '{key}'? Type 'confirm' to delete or 'cancel' to keep it.",
                "Deletion awaits confirmation.",
            )

        if normalized == "search":
            return "ERROR", "Provide text to search for.", "Empty search query."

        if normalized.startswith("search "):
            query = command[len("search "):].strip()

            if not query:
                return "ERROR", "Provide text to search for.", "Empty search query."

            matches = self.memory.search(query)

            if matches:
                return "OK", ", ".join(matches), f"Found {len(matches)} matching key(s)."

            return "NOT_FOUND", "No matching memories found.", "Search returned no matches."

        if normalized == "list":
            keys = self.memory.list_keys()
            return (
                "OK",
                ", ".join(keys) if keys else "Memory is empty.",
                "Memory keys listed.",
            )

        return "UNKNOWN", "I don't have a rule for that yet. Type 'help'.", "No rule matched."
