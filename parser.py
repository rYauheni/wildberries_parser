import requests

from exceptions.exceptions import RootError, ProductDataError, FeedbackDataError
from objects.feedback import Feedback


def get_product_detail_url(pid: int) -> str:
    url = f'https://card.wb.ru/cards/detail?nm={pid}'
    return url


def get_product_feedback_urls(root: int) -> list:
    urls = [f'https://feedbacks{i}.wb.ru/feedbacks/v1/{root}' for i in range(1, 3)]
    return urls


# def parse_product_root(product):
#     product_detail_url = get_product_detail_url(pid=product.id)
#     product_detail = requests.get(product_detail_url)
#     product.get_product_root_from_json(product_detail=product_detail)


# def parse_feedback_count(pid: int) -> (int, None):
#     feedback_count = 0
#
#     root = parse_product_root(pid)
#
#     product_feedback_urls = get_product_feedback_urls(root)
#     for url in product_feedback_urls:
#         product_feedback = requests.get(url)
#         if product_feedback.status_code == 200:
#             f_count = product_feedback.json()['feedbackCount']
#             feedback_count += f_count
#
#     return feedback_count


def parse_product_data(product):
    product_detail_url = get_product_detail_url(pid=product.id)
    product_detail = requests.get(product_detail_url)
    product.get_product_data_from_json(product_detail=product_detail)


def get_product_data(product):
    parse_product_data(product)
    # parse_product_root(product=product)

    product_feedback_urls = get_product_feedback_urls(product.root)
    for url in product_feedback_urls:
        get_negative_feedback_data(product=product, url=url)


def get_negative_feedback_data(product, url):
    last_update = product.last_update
    try:
        product_feedbacks = requests.get(url).json()['feedbacks']
        if not product_feedbacks:
            return
        new_feedbacks = [fb for fb in product_feedbacks if fb['createdDate'] >= last_update]
        for new_feedback in new_feedbacks:
            feedback = Feedback()
            feedback.mark = new_feedback['productValuation']
            feedback.text = new_feedback['text']
            feedback.date = new_feedback['createdDate']
            if feedback.is_negative():
                product.feedbacks.append(feedback)

    except Exception:
        raise FeedbackDataError
