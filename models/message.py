from dataclasses import dataclass

from models.product import Product


@dataclass
class Message:
    def __init__(self, product: Product, text: str = ''):
        self.product = product
        self.text = text

    def set_message_text_for_n_feedback(self, feedback):
        self.text = (f'New negative feedback.\n'
                     f'Product name: {self.product.name}.\n'
                     f'SKU (ID): {self.product.id}.\n'
                     f'Mark: {feedback.mark}.\n'
                     f'Feedback: <{feedback.text}>.\n'
                     f'Current rating: {self.product.rating}.\n')

    def set_message_text_for_not_found_n_feedback(self):
        self.text = (f'Not found new negative feedbacks for:\n'
                     f'Product name: {self.product.name}.\n'
                     f'SKU (ID): {self.product.id}.\n'
                     f'Current rating: {self.product.rating}.\n')


@dataclass
class MessagesList:
    def __init__(self, product: Product):
        self.product = product
        self.messages_list: list = []

    def fill_messages_list(self):
        feedbacks = self.product.feedbacks
        if feedbacks:
            for feedback in feedbacks:
                message = Message(product=self.product)
                message.set_message_text_for_n_feedback(feedback=feedback)
                self.messages_list.append(message)

        else:
            message = Message(product=self.product)
            message.set_message_text_for_not_found_n_feedback()
            self.messages_list.append(message)
