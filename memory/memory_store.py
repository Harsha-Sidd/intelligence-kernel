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

        return data

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

    def list_keys(self):
        return sorted(self.data)
