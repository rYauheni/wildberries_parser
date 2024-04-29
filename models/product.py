from dataclasses import dataclass, field
from enum import Enum
import requests

from exceptions.exceptions import ProductDataError, FeedbackDataError
from logger_utils.logger_utils import logger
from models.feedback import Feedback


class Status(Enum):
    GOOD = 'good'
    PRODUCT_DNF = 'product_dnf'
    FEEDBACK_DNF = 'feedback_dnf'
    UNKNOWN_E = 'unknown_e'


@dataclass
class Product:
    id: int
    status: Status = Status.GOOD
    url: str = None
    root: int = None
    name: str = None
    rating: float = None
    last_update: float = None
    feedbacks: list[Feedback] = field(default_factory=list)

