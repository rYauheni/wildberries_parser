from dataclasses import dataclass,field

from objects.feedback import Feedback


@dataclass
class Product:
    id: int
    root: int = None
    name: str = None
    rating: float = None
    last_update: str = None
    feedbacks: list[Feedback] = field(default_factory=list)
