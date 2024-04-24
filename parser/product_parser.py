import requests

from exceptions.exceptions import ProductDataError, FeedbackDataError
from models.feedback import Feedback


class ProductParser:
    def __init__(self, pid: int, last_update: float):
        self.product_last_update = last_update
        self.product_url = f'https://card.wb.ru/cards/detail?nm={pid}'
        self.product_data = self.parse_product_data()

    # def get_product_data_from_json(self, product_detail):
    #     data = product_detail.json()
    #     try:
    #         self.root = data['data']['products'][0]['root']
    #
    #         self.name = (str(data['data']['products'][0]['brand']) + ' ' +
    #                      str(data['data']['products'][0]['name']))
    #         self.rating = data['data']['products'][0]['reviewRating']
    #
    #     except KeyError:
    #         raise ProductDataError

    def parse_product_data(self):
        try:
            product_detail = requests.get(self.product_url)
        except Exception:
            raise ProductDataError
        return product_detail.json()

    def product_root_from_json(self):
        try:
            product_root = self.product_data['data']['products'][0]['root']
        except KeyError:
            raise ProductDataError
        return product_root

    def product_name_from_json(self):
        try:
            product_name = (str(self.product_data['data']['products'][0]['brand']) + ' ' +
                            str(self.product_data['data']['products'][0]['name']))
        except KeyError:
            raise ProductDataError
        return product_name

    def product_rating_from_json(self):
        try:
            product_rating = self.product_data['data']['products'][0]['reviewRating']
        except KeyError:
            raise ProductDataError
        return product_rating

    # def get_product_detail_url(self):
    #     self.url = f'https://card.wb.ru/cards/detail?nm={self.id}'

    def parse_product_feedbacks(self):
        feedbacks_urls = self.get_feedbacks_urls()
        try:
            negative_feedbacks = self.get_negative_feedbacks(feedbacks_urls=feedbacks_urls)
        except Exception:
            raise FeedbackDataError
        return negative_feedbacks

    def get_feedbacks_urls(self) -> list[str]:
        product_root = self.product_root_from_json()
        feedbacks_urls = [f'https://feedbacks{i}.wb.ru/feedbacks/v1/{product_root}' for i in range(1, 3)]
        return feedbacks_urls

    def get_negative_feedbacks(self, feedbacks_urls):
        negative_feedbacks = []
        try:
            for url in feedbacks_urls:
                product_feedbacks = requests.get(url).json()['feedbacks']
                if not product_feedbacks:
                    continue

                new_update = self.product_last_update
                for pf in product_feedbacks:
                    feedback = Feedback()
                    feedback.get_feedback_data_from_json(feedback_detail=pf)
                    if feedback.is_negative() and feedback.is_new(last_update=self.product_last_update):
                        negative_feedbacks.append(feedback)
                        if feedback.date > new_update:
                            new_update = feedback.date

                self.product_last_update = new_update

                return negative_feedbacks

        except Exception:
            raise FeedbackDataError

    # def parse_product_data(self):
    #     try:
    #         product_detail = requests.get(self.product_url)
    #     except Exception:
    #         raise ProductDataError
    #     return product_detail

        # self.get_product_data_from_json(product_detail=product_detail)
        # feedbacks_urls = self.get_feedbacks_urls()
        # try:
        #     self.get_negative_feedbacks(feedbacks_urls=feedbacks_urls)
        # except Exception:
        #     raise FeedbackDataError

    # def handle_product_data_parser(self):
    #     try:
    #         self.parse_product_data()
    #         logger.info(f'Product {self.id} has been parsed.')
    #     except ProductDataError:
    #         self.status = Status.PRODUCT_DNF
    #         logger.error(f'Product {self.id} data not found or could not be parsed.')
    #     except FeedbackDataError:
    #         self.status = Status.FEEDBACK_DNF
    #         logger.error(f'Product {self.id} feedback data not found or could not be parsed.')
    #     except Exception as e:
    #         self.status = Status.UNKNOWN_E
    #         logger.error(f'Product {self.id} raised exception {e}.')
