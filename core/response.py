
from dataclasses import dataclass


@dataclass(frozen=True)
class KernelResponse:
    status: str
    message: str
    explanation: str

    @classmethod
    def from_tuple(cls, result):
        if not isinstance(result, tuple) or len(result) != 3:
            raise ValueError(
                "Expected a three-item result: status, message, explanation."
            )

        status, message, explanation = result

        if not all(
            isinstance(value, str)
            for value in (status, message, explanation)
        ):
            raise TypeError("All response fields must be strings.")

        return cls(
            status=status,
            message=message,
            explanation=explanation,
        )

    def to_tuple(self):
        return self.status, self.message, self.explanation

    def to_dict(self):
        return {
            "status": self.status,
            "message": self.message,
            "explanation": self.explanation,
        }

    @property
    def successful(self):
        return self.status == "OK"

