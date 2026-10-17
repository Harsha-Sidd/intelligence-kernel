import json
from datetime import datetime
from pathlib import Path


class MemoryStore:
    def __init__(self, path):
        self.path = Path(path)
        self.data = self.load()

    def load(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            return {}

        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            print("Warning: Memory could not be read.")
            return {}

        if not isinstance(data, dict):
            print("Warning: Memory format is invalid.")
            return {}

        # Keep only entries in the expected format.
        return {
            key: item
            for key, item in data.items()
            if isinstance(key, str)
            and isinstance(item, dict)
            and isinstance(item.get("value"), str)
            and isinstance(item.get("updated_at"), str)
        }

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".tmp")

        temporary.write_text(
            json.dumps(self.data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        temporary.replace(self.path)

    def remember(self, key, value):
        self.data[key] = {
            "value": value,
            "updated_at": datetime.now().astimezone().isoformat(),
        }
        self.save()

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

        del self.data[key]
        self.save()
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
