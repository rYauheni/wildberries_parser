class FileError(Exception):

    def __init__(self, *args):
        if args:
            self.message = args
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'FileError:  No matching file found. Detail: {self.message}.'
        else:
            return 'FileError:  No matching file found.'


class RootError(Exception):

    def __init__(self, *args):
        if args:
            self.message = args
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'RootError: Product root not found. Detail: {self.message}.'
        else:
            return 'RootError:  Product root not found.'


class ProductDataError(Exception):

    def __init__(self, *args):
        if args:
            self.message = args
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'ProductDataError: Product data not found. Detail: {self.message}.'
        else:
            return 'ProductDataError:  Product data not found.'


class FeedbackDataError(Exception):

    def __init__(self, *args):
        if args:
            self.message = args
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'FeedbackDataError: Feedback not found. Detail: {self.message}.'
        else:
            return 'FeedbackDataError:  Feedback not found.'


class NotificationError(Exception):

    def __init__(self, *args):
        if args:
            self.message = args
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'NotificationError: The application could not send the message. Detail: {self.message}.'
        else:
            return 'NotificationError:  The application could not send the message.'