import requests

from exceptions.exceptions import RootError, ProductDataError, FeedbackDataError
from objects.feedback import Feedback
from objects.product import Product


def get_product_detail_url(pid: int) -> str:
    url = f'https://card.wb.ru/cards/detail?nm={pid}'
    return url


def get_product_feedback_urls(root: int) -> list:
    urls = [f'https://feedbacks{i}.wb.ru/feedbacks/v1/{root}' for i in range(1, 3)]
    return urls


def parse_product_root(pid: int) -> int:
    product_detail_url = get_product_detail_url(pid=pid)
    product_detail = requests.get(product_detail_url)
    if not product_detail.status_code == 200:
        raise RootError
    root = product_detail.json()['data']['products'][0]['root']
    return root


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
    if not product_detail.status_code == 200:
        raise ProductDataError
    product_data = product_detail.json()
    product.name = (str(product_data['data']['products'][0]['brand']) + ' ' +
                    str(product_data['data']['products'][0]['name']))
    product.rating = product_data['data']['products'][0]['reviewRating']


# def get_messages(pid: int, app_state_service) -> (list, None):
#     root = parse_product_root(pid)
#     last_update = app_state_service.get_app_state_data(pid)
#     if not root:
#         return
#
#     product_feedback_urls = get_product_feedback_urls(root)
#     for url in product_feedback_urls:
#         try:
#             product_feedback = requests.get(url)
#             messages = []
#             if product_feedback.status_code == 200:
#                 feedbacks = product_feedback.json()['feedbacks']
#                 new_feedbacks = [fb for fb in feedbacks if fb['createdDate'] >= last_update]
#                 for feedback in new_feedbacks:
#                     mark = feedback['productValuation']
#                     last_data = feedback['createdDate']
#                     if last_data > last_update:
#                         app_state_service.update_app_state_data(pid=pid, last_update=last_data)
#                     if 1 <= mark <= 4:
#                         text = feedback['text']
#                         product_data = parse_product_data(pid)
#                         try:
#                             product_name = product_data['product_name']
#                             product_rating = product_data['product_rating']
#                         except KeyError:
#                             product_name, product_rating = None, None
#                         msg = (f'Негативный отзыв/Товар: {product_name}/SKU: {pid}/Оценка: {mark}/Отзыв: {text}/'
#                                f'Текущий рейтинг товара: {product_rating}')
#                         messages.append(msg)
#             return messages
#         except TypeError:
#             return


def get_product_data(product):
    parse_product_data(product)
    product.root = parse_product_root(product.id)

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
