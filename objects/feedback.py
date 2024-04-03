from dataclasses import dataclass


@dataclass
class Feedback:
    mark: int = None
    text: str = None
    date: str = None

    def is_negative(self):
        if 1 <= self.mark <= 4:
            return True
