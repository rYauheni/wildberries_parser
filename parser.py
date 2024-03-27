import requests

from condition_data import get_condition, update_condition


def get_product_detail_url(pid: int) -> str:
    url = f'https://card.wb.ru/cards/detail?nm={pid}'
    return url


def get_product_feedback_urls(root: int) -> list:
    urls = [f'https://feedbacks{i}.wb.ru/feedbacks/v1/{root}' for i in range(1, 3)]
    return urls


def parse_product_root(pid: int) -> int:
    product_detail_url = get_product_detail_url(pid=pid)
    product_detail = requests.get(product_detail_url)
    if product_detail.status_code == 200:
        root = product_detail.json()['data']['products'][0]['root']
    else:
        root = 0
    return root


def parse_feedback_count(pid: int) -> (int, None):
    feedback_count = 0

    root = parse_product_root(pid)
    if not root:
        return

    product_feedback_urls = get_product_feedback_urls(root)
    for url in product_feedback_urls:
        product_feedback = requests.get(url)
        if product_feedback.status_code == 200:
            f_count = product_feedback.json()['feedbackCount']
            feedback_count += f_count

    return feedback_count


def parse_product_data(pid: int) -> (int, None):
    product_detail_url = get_product_detail_url(pid=pid)
    product_detail = requests.get(product_detail_url)
    product_data = {}
    if product_detail.status_code == 200:
        product = product_detail.json()
        product_name = str(product['data']['products'][0]['brand']) + ' ' + str(product['data']['products'][0]['name'])
        product_rating = product['data']['products'][0]['reviewRating']
        product_data['product_name'] = product_name
        product_data['product_rating'] = product_rating
    return product_data


def get_messages(pid: int) -> (list, None):
    root = parse_product_root(pid)
    last_update = get_condition(pid)
    if not root:
        return

    product_feedback_urls = get_product_feedback_urls(root)
    for url in product_feedback_urls:
        try:
            product_feedback = requests.get(url)
            messages = []
            if product_feedback.status_code == 200:
                feedbacks = product_feedback.json()['feedbacks']
                new_feedbacks = [fb for fb in feedbacks if fb['createdDate'] >= last_update]
                for feedback in new_feedbacks:
                    mark = feedback['productValuation']
                    last_data = feedback['createdDate']
                    if last_data > last_update:
                        update_condition(pid, last_update=last_data)
                    if 1 <= mark <= 4:
                        text = feedback['text']
                        product_data = parse_product_data(pid)
                        try:
                            product_name = product_data['product_name']
                            product_rating = product_data['product_rating']
                        except KeyError:
                            product_name, product_rating = None, None
                        msg = (f'Негативный отзыв/Товар: {product_name}/SKU: {pid}/Оценка: {mark}/Отзыв: {text}/'
                               f'Текущий рейтинг товара: {product_rating}')
                        messages.append(msg)
            return messages
        except TypeError:
            return
