from enum import Enum, auto


class Status (Enum):
    Pending_for_Return = auto()
    Return_Successfully = auto()

    def __str__(self):
        return self.name.replace('_', ' ')