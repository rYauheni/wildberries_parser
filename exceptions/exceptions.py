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


class RootError(ValueError):

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
