from models.product import Product


def fill_messages_list(product: Product, messages_list: list) -> list:
    if product.feedbacks:
        for feedback in product.feedbacks:
            message = (f'New negative feedback.\n'
                       f'Product name: {product.name}.\n'
                       f'SKU (ID): {product.id}.\n'
                       f'Mark: {feedback.mark}.\n'
                       f'Feedback: <{feedback.text}>.\n'
                       f'Current rating: {product.rating}.\n')
            messages_list.append(message)
    return messages_list


def create_not_found_negative_feedbacks_message(product=Product) -> str:
    message = (f'Not found new negative feedbacks for:\n'
               f'Product name: {product.name}.\n'
               f'SKU (ID): {product.id}.\n'
               f'Current rating: {product.rating}.\n')
    return message
