from dataclasses import dataclass
from datetime import datetime

from exceptions.exceptions import FeedbackDataError
from settings import DATETIME_TEMPLATE


@dataclass
class Feedback:
    mark: int = None
    text: str = None
    date: float = None

    def get_feedback_data_from_json(self, feedback_detail):
        try:
            self.mark = feedback_detail['productValuation']
            self.text = feedback_detail['text']
            fb_date = feedback_detail['createdDate']
            self.date = datetime.strptime(fb_date, DATETIME_TEMPLATE).timestamp()
        except KeyError:
            raise FeedbackDataError

    def is_new(self, last_update):
        if self.date > last_update:
            return True

    def is_negative(self):
        if 1 <= self.mark <= 4:
            return True


