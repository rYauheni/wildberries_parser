import inspect
import logging


class CustomFormatter(logging.Formatter):
    COLORS = {'DEBUG': '\033[94m', 'INFO': '\033[92m', 'WARNING': '\033[93m', 'ERROR': '\033[91m',
              'CRITICAL': '\033[95m'}

    def format(self, record):
        color = self.COLORS.get(record.levelname, '')
        log_fmt = f"{color}%(asctime)s - {color}%(filename)s - {color}%(levelname)s - {color}%(message)s\033[0m"
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logging.basicConfig(
    level=logging.DEBUG,
)
logging.getLogger().handlers[0].setFormatter(CustomFormatter())

logger = logging.getLogger()
