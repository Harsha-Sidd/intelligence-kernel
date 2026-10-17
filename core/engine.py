from core.response import KernelResponse
from core.intent_parser import IntentParser


class KernelEngine:
    def __init__(self, memory):
        self.memory = memory
        self.parser = IntentParser()
        self.pending_forget = None

    def process_structured(self, command):
        result = self.process(command)
        return KernelResponse.from_tuple(result)

    def process(self, command):
        intent = self.parser.parse(command)

        action = intent.name
        args = intent.arguments

        # Return validation errors, but let unknown commands reach
        # the UNKNOWN handler below.
        if intent.error and action != "unknown":
            return (
                "ERROR",
                intent.error,
                "Intent validation failed.",
            )

        # Handle a pending deletion before processing other commands.
        if self.pending_forget is not None:
            if action == "confirm":
                key = self.pending_forget
                self.pending_forget = None

                if self.memory.forget(key):
                    return (
                        "OK",
                        f"Forgot: {key}",
                        "Confirmed deletion.",
                    )

                return (
                    "NOT_FOUND",
                    f"No memory found for: {key}",
                    "Key no longer exists.",
                )

            if action == "cancel":
                key = self.pending_forget
                self.pending_forget = None

                return (
                    "OK",
                    f"Deletion cancelled: {key}",
                    "Deletion was cancelled.",
                )

            return (
                "CONFIRMATION_REQUIRED",
                "Type 'confirm' to delete or 'cancel' to keep the entry.",
                "Deletion is awaiting confirmation.",
            )

        if action == "unknown":
            return (
                "UNKNOWN",
                "I don't have a rule for that yet. Type 'help'.",
                "No rule matched.",
            )

        if action in {"exit", "quit"}:
            return (
                "EXIT",
                "Session ended.",
                "Exit command matched.",
            )

        if action == "help":
            return (
                "OK",
                "Commands: help, remember KEY = VALUE, update KEY = VALUE, "
                "recall KEY, forget KEY, search TEXT, list, exit",
                "Help rule matched.",
            )

        if action == "remember":
            key, value = args

            if self.memory.recall(key) is not None:
                return (
                    "EXISTS",
                    f"Memory already exists: {key}. Use update to change it.",
                    "Duplicate key rejected.",
                )

            self.memory.remember(key, value)

            return (
                "OK",
                f"Stored: {key}",
                "Memory saved.",
            )

        if action == "update":
            key, value = args

            if not self.memory.update(key, value):
                return (
                    "NOT_FOUND",
                    f"No memory found for: {key}",
                    "Update target missing.",
                )

            return (
                "OK",
                f"Updated: {key}",
                "Existing memory updated.",
            )

        if action == "recall":
            key = args[0]
            item = self.memory.recall(key)

            if item is not None:
                return (
                    "OK",
                    f"{key} = {item['value']}",
                    "Exact key matched.",
                )

            return (
                "NOT_FOUND",
                f"No memory found for: {key}",
                "No exact key matched.",
            )

        if action == "forget":
            key = args[0]

            if self.memory.recall(key) is None:
                return (
                    "NOT_FOUND",
                    f"No memory found for: {key}",
                    "No exact key matched.",
                )

            self.pending_forget = key

            return (
                "CONFIRMATION_REQUIRED",
                f"Delete '{key}'? Type 'confirm' to delete or 'cancel' to keep it.",
                "Deletion awaits confirmation.",
            )

        if action == "search":
            query = args[0]
            matches = self.memory.search(query)

            if matches:
                return (
                    "OK",
                    ", ".join(matches),
                    f"Found {len(matches)} matching key(s).",
                )

            return (
                "NOT_FOUND",
                "No matching memories found.",
                "Search returned no matches.",
            )

        if action == "list":
            keys = self.memory.list_keys()

            return (
                "OK",
                ", ".join(keys) if keys else "Memory is empty.",
                "Memory keys listed.",
            )

        # Defensive fallback for any intent without an execution rule.
        return (
            "UNKNOWN",
            "I don't have a rule for that yet. Type 'help'.",
            "Intent has no execution rule.",
        )

