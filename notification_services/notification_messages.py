from objects.product import Product


def create_messages_list(product: Product) -> list:
    messages_list = []
    if product.feedbacks:
        for feedback in product.feedbacks:
            message = (f'New negative review.\n'
                       f'Product name: {product.name}.\n'
                       f'SKU (ID): {product.id}.\n'
                       f'Mark: {feedback.mark}.\n'
                       f'Feedback: <{feedback.text}>.\n'
                       f'Current rating: {product.rating}.\n')
            messages_list.append(message)
    return messages_list
