from dataclasses import dataclass


@dataclass
class Feedback:
    mark: int = None
    text: str = None
    date: str = None

    def get_feedback_data_from_json(self, feedback_detail):
        self.mark = feedback_detail['productValuation']
        self.text = feedback_detail['text']
        self.date = feedback_detail['createdDate']

    def is_new(self, last_update):
        if self.date > last_update:
            return True

    def is_negative(self):
        if 1 <= self.mark <= 4:
            return True


