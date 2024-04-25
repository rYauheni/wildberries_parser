import requests

from exceptions.exceptions import ProductDataError, FeedbackDataError, RootError
from logger_utils.logger_utils import logger
from models.feedback import Feedback
from models.product import Product, Status


def create_product(pid: int, product_last_update: float):
    product_url = f'https://card.wb.ru/cards/detail?nm={pid}'
    product_status = Status.GOOD
    product_root = None
    product_name = None
    product_rating = None
    product_last_update = product_last_update
    product_feedbacks = None

    try:
        try:
            product_detail = parse_product_data(product_url=product_url)
            product_root = product_root_from_json(product_detail=product_detail)
            product_name = product_name_from_json(product_detail=product_detail)
            product_rating = product_rating_from_json(product_detail=product_detail)
            logger.info(f'Product {pid} has been parsed.')
        except ProductDataError:
            product_status = Status.PRODUCT_DNF
            logger.error(f'Product {pid} data not found or could not be parsed.')

        feedbacks_urls = get_feedbacks_urls(product_root=product_root)

        if product_status == Status.GOOD:
            try:
                product_feedbacks = parse_product_feedbacks(feedbacks_urls=feedbacks_urls,
                                                            product_last_update=product_last_update)
                logger.info(f'Product {pid} feedbacks has been parsed.')
            except FeedbackDataError:
                product_status = Status.FEEDBACK_DNF
                logger.error(f'Product {pid} feedbacks could not be parsed.')

        if product_status == Status.GOOD:
            product_last_update = update_product_last_update(n_feedbacks=product_feedbacks,
                                                             product_last_update=product_last_update)
    except Exception as e:
        product_status = Status.UNKNOWN_E
        logger.error(f'Product {pid} raised exception {e}.')

    product = Product(
        id=pid,
        status=product_status,
        url=product_url,
        root=product_root,
        name=product_name,
        rating=product_rating,
        last_update=product_last_update,
        feedbacks=product_feedbacks
    )

    return product


def parse_product_data(product_url: str):
    try:
        product_detail = requests.get(product_url)
    except Exception:
        raise ProductDataError
    return product_detail.json()


def product_root_from_json(product_detail):
    try:
        product_root = product_detail['data']['products'][0]['root']
    except KeyError:
        raise RootError
    return product_root


def product_name_from_json(product_detail):
    try:
        product_name = (str(product_detail['data']['products'][0]['brand']) + ' ' +
                        str(product_detail['data']['products'][0]['name']))
    except KeyError:
        raise ProductDataError
    return product_name


def product_rating_from_json(product_detail):
    try:
        product_rating = product_detail['data']['products'][0]['reviewRating']
    except KeyError:
        raise ProductDataError
    return product_rating


def parse_product_feedbacks(feedbacks_urls, product_last_update):
    try:
        negative_feedbacks = get_negative_feedbacks(feedbacks_urls=feedbacks_urls,
                                                    product_last_update=product_last_update)
    except Exception:
        raise FeedbackDataError
    return negative_feedbacks


def get_feedbacks_urls(product_root) -> list[str]:
    feedbacks_urls = [f'https://feedbacks{i}.wb.ru/feedbacks/v1/{product_root}' for i in range(1, 3)]
    return feedbacks_urls


def get_negative_feedbacks(feedbacks_urls, product_last_update):
    negative_feedbacks = []
    try:
        for url in feedbacks_urls:
            product_feedbacks = requests.get(url).json()['feedbacks']
            if not product_feedbacks:
                continue
            for pf in product_feedbacks:
                feedback = Feedback()
                feedback.get_feedback_data_from_json(feedback_detail=pf)
                if feedback.is_negative() and feedback.is_new(last_update=product_last_update):
                    negative_feedbacks.append(feedback)
            return negative_feedbacks
    except Exception:
        raise FeedbackDataError


def update_product_last_update(n_feedbacks, product_last_update):
    new_update = product_last_update
    for n_feedback in n_feedbacks:
        if n_feedback.date > new_update:
            new_update = n_feedback.date
    return new_update
