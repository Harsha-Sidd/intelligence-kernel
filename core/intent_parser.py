
from dataclasses import dataclass


@dataclass(frozen=True)
class Intent:
    name: str
    arguments: tuple[str, ...] = ()
    error: str | None = None


class IntentParser:
    """Recognize kernel commands and extract their arguments."""

    COMMANDS = {
        "help",
        "remember",
        "update",
        "recall",
        "forget",
        "search",
        "list",
        "confirm",
        "cancel",
        "exit",
        "quit",
    }

    def parse(self, command: str) -> Intent:
        command = command.strip()

        if not command:
            return Intent("invalid", error="Command cannot be empty.")

        name, separator, remainder = command.partition(" ")
        normalized = name.casefold()

        if normalized not in self.COMMANDS:
            return Intent("unknown", error="Unrecognized command.")

        if normalized in {"help", "list", "confirm", "cancel", "exit", "quit"}:
            if separator:
                return Intent(
                    "invalid",
                    error=f"'{normalized}' does not accept arguments.",
                )
            return Intent(normalized)

        if not separator or not remainder.strip():
            return Intent(
                normalized,
                error=f"'{normalized}' requires an argument.",
            )

        remainder = remainder.strip()

        if normalized in {"remember", "update"}:
            if "=" not in remainder:
                return Intent(
                    normalized,
                    error=f"Use: {normalized} KEY = VALUE",
                )

            key, value = remainder.split("=", 1)
            key, value = key.strip(), value.strip()

            if not key or not value:
                return Intent(
                    normalized,
                    error="Key and value cannot be empty.",
                )

            return Intent(normalized, (key, value))

        return Intent(normalized, (remainder,))

