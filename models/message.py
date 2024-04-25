from dataclasses import dataclass

from app_state_data_service.app_state_data_service import AppStateDataService
from exceptions.exceptions import NotificationError
from logger_utils.logger_utils import logger
from models.product import Product, Status
from notification_services.notification_manager import NotificationManager


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

    def set_e_message_for_for_product_data_not_found(self):
        self.text = (f'Product SKU (ID): {self.product.id}.\n'
                     f'The application did not find a product data '
                     f'or the product data could not be parsed.\n'
                     f'Contact the application administrator.')

    def set_e_message_for_for_feedback_data_not_found(self):
        self.text = (f'Product SKU (ID): {self.product.id}.\n'
                     f'The application did not find a product feedback data '
                     f'or the product feedback data could not be parsed.\n'
                     f'Contact the application administrator.')

    def set_e_message_for_for_unknown_e(self):
        self.text = (f'Product SKU (ID): {self.product.id}.\n'
                     f'The application raised an exception.\n'
                     f'Contact the application administrator.')


@dataclass
class MessagesList:
    def __init__(self, product: Product):
        self.product = product
        self.messages_list: list = []

    def fill_messages_list(self):
        if self.product.status != Status.GOOD:
            self.create_message_for_exception()
            return
        feedbacks = self.product.feedbacks
        if not feedbacks:
            self.create_message_for_feedback_nor_found()
            return
        self.create_messages_for_feedbacks(feedbacks=feedbacks)

    def create_messages_for_feedbacks(self, feedbacks):
        for feedback in feedbacks:
            message = Message(product=self.product)
            message.set_message_text_for_n_feedback(feedback=feedback)
            self.messages_list.append(message)

    def create_message_for_feedback_nor_found(self):
        message = Message(product=self.product)
        message.set_message_text_for_not_found_n_feedback()
        self.messages_list.append(message)

    def create_message_for_exception(self):
        message = Message(product=self.product)
        match self.product.status:
            case Status.PRODUCT_DNF:
                message.set_e_message_for_for_product_data_not_found()
            case Status.FEEDBACK_DNF:
                message.set_e_message_for_for_feedback_data_not_found()
            case Status.UNKNOWN_E:
                message.set_e_message_for_for_unknown_e()
        self.messages_list.append(message)

    def send_messages(self, notification_manager: NotificationManager):
        for message in self.messages_list:
            try:
                notification_manager.send_message(message=message.text)
            except NotificationError:
                raise

    def handle_messages_sender(self, notification_manager: NotificationManager):
        try:
            self.send_messages(notification_manager=notification_manager)
            logger.info(f'Product {self.product.id}. Messages ware sent successfully.')
        except NotificationError:
            logger.critical(f'Product {self.product.id}. Messages did not be sent.')
            raise
