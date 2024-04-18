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
    last_update: str = None
    feedbacks: list[Feedback] = field(default_factory=list)

    def get_product_data_from_json(self, product_detail):
        data = product_detail.json()
        try:
            self.root = data['data']['products'][0]['root']

            self.name = (str(data['data']['products'][0]['brand']) + ' ' +
                         str(data['data']['products'][0]['name']))
            self.rating = data['data']['products'][0]['reviewRating']

        except KeyError:
            raise ProductDataError

    def get_product_detail_url(self):
        self.url = f'https://card.wb.ru/cards/detail?nm={self.id}'

    def get_feedbacks_urls(self) -> list[str]:
        feedbacks_urls = [f'https://feedbacks{i}.wb.ru/feedbacks/v1/{self.root}' for i in range(1, 3)]
        return feedbacks_urls

    def get_negative_feedbacks(self, feedbacks_urls):
        try:
            for url in feedbacks_urls:
                product_feedbacks = requests.get(url).json()['feedbacks']
                if not product_feedbacks:
                    continue

                new_update = self.last_update
                for pf in product_feedbacks:
                    feedback = Feedback()
                    feedback.get_feedback_data_from_json(feedback_detail=pf)
                    if feedback.is_negative() and feedback.is_new(last_update=self.last_update):
                        self.feedbacks.append(feedback)
                        if feedback.date > new_update:
                            new_update = feedback.date

                self.last_update = new_update

        except Exception:
            raise FeedbackDataError

    def parse_product_data(self):
        self.get_product_detail_url()
        try:
            product_detail = requests.get(self.url)
        except Exception:
            raise ProductDataError
        self.get_product_data_from_json(product_detail=product_detail)
        feedbacks_urls = self.get_feedbacks_urls()
        try:
            self.get_negative_feedbacks(feedbacks_urls=feedbacks_urls)
        except Exception:
            raise FeedbackDataError

    def handle_product_data_parser(self):
        try:
            self.parse_product_data()
            logger.info(f'Product {self.id} has been parsed.')
        except ProductDataError:
            self.status = Status.PRODUCT_DNF
            logger.error(f'Product {self.id} data not found or could not be parsed.')
        except FeedbackDataError:
            self.status = Status.FEEDBACK_DNF
            logger.error(f'Product {self.id} feedback data not found or could not be parsed.')
        except Exception as e:
            self.status = Status.UNKNOWN_E
            logger.error(f'Product {self.id} raised exception {e}.')
