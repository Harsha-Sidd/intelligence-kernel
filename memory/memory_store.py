
import json
import os
import tempfile
from datetime import datetime
from pathlib import Path


class MemoryLoadError(RuntimeError):
    """Raised when existing memory cannot be safely loaded."""


class MemoryStore:
    def __init__(self, path):
        self.path = Path(path)
        self.data = self.load()

    def load(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            return {}

        try:
            raw = self.path.read_text(encoding="utf-8")
            data = json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError, OSError) as error:
            raise MemoryLoadError(
                f"Memory file could not be safely read: {self.path}"
            ) from error

        if not isinstance(data, dict):
            raise MemoryLoadError(
                "Memory file has an invalid top-level format."
            )

        # Preserve compatibility: ignore malformed individual entries.
        return {
            key: item
            for key, item in data.items()
            if isinstance(key, str)
            and isinstance(item, dict)
            and isinstance(item.get("value"), str)
            and isinstance(item.get("updated_at"), str)
        }

    def _write_atomically(self, destination, content):
        destination.parent.mkdir(parents=True, exist_ok=True)

        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=destination.parent,
                prefix=f".{destination.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary:
                temp_path = Path(temporary.name)
                temporary.write(content)
                temporary.flush()
                os.fsync(temporary.fileno())

            temp_path.replace(destination)
            temp_path = None

        finally:
            if temp_path is not None:
                try:
                    temp_path.unlink(missing_ok=True)
                except OSError:
                    pass

    def _backup_current_file(self):
        if not self.path.exists():
            return

        try:
            original = self.path.read_bytes()
            parsed = json.loads(original.decode("utf-8"))

            if not isinstance(parsed, dict):
                raise ValueError("Memory document is not a dictionary.")

        except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
            raise MemoryLoadError(
                "Existing memory is invalid; refusing to overwrite it."
            ) from error

        backup_path = self.path.with_suffix(".bak")
        backup_temp = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="wb",
                dir=backup_path.parent,
                prefix=f".{backup_path.name}.",
                suffix=".tmp",
                delete=False,
            ) as temporary:
                backup_temp = Path(temporary.name)
                temporary.write(original)
                temporary.flush()
                os.fsync(temporary.fileno())

            backup_temp.replace(backup_path)
            backup_temp = None

        finally:
            if backup_temp is not None:
                try:
                    backup_temp.unlink(missing_ok=True)
                except OSError:
                    pass

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)

        content = json.dumps(
            self.data,
            indent=2,
            ensure_ascii=False,
        ) + "\n"

        # Parse our generated document before touching the existing file.
        try:
            generated = json.loads(content)
        except json.JSONDecodeError as error:
            raise ValueError("Generated memory JSON is invalid.") from error

        if not isinstance(generated, dict):
            raise ValueError("Memory data must be a dictionary.")

        for key, item in generated.items():
            if (
                not isinstance(key, str)
                or not isinstance(item, dict)
                or not isinstance(item.get("value"), str)
                or not isinstance(item.get("updated_at"), str)
            ):
                raise ValueError("Memory contains an invalid entry.")

        # Preserve the last on-disk JSON document before replacing it.
        self._backup_current_file()

        self._write_atomically(self.path, content)

    def remember(self, key, value):
        if not isinstance(key, str) or not key.strip():
            raise ValueError("Memory key must be a non-empty string.")

        if not isinstance(value, str) or not value.strip():
            raise ValueError("Memory value must be a non-empty string.")

        previous = self.data.get(key)

        self.data[key] = {
            "value": value,
            "updated_at": datetime.now().astimezone().isoformat(),
        }

        try:
            self.save()
        except Exception:
            if previous is None:
                self.data.pop(key, None)
            else:
                self.data[key] = previous
            raise

    def recall(self, key):
        return self.data.get(key)

    def update(self, key, value):
        if key not in self.data:
            return False

        self.remember(key, value)
        return True

    def forget(self, key):
        if key not in self.data:
            return False

        previous = self.data.pop(key)

        try:
            self.save()
        except Exception:
            self.data[key] = previous
            raise

        return True

    def search(self, query):
        query = query.casefold()

        if not query:
            return []

        matches = []

        for key, item in self.data.items():
            if query in key.casefold() or query in item["value"].casefold():
                matches.append(key)

        return sorted(matches)

    def list_keys(self):
        return sorted(self.data)

