from dataclasses import dataclass, field

from exceptions.exceptions import ProductDataError
from objects.feedback import Feedback


@dataclass
class Product:
    id: int
    root: int = None
    name: str = None
    rating: float = None
    last_update: str = None
    feedbacks: list[Feedback] = field(default_factory=list)

    def get_product_data_from_json(self, product_detail):
        data = product_detail.json()
        try:
            self.root = data['data']['products'][0]['root']

            self.name = (str(data['data']['products'][0]['brand']) + ' ' +
                         str(data['data']['products'][0]['name']))
            self.rating = data['data']['products'][0]['reviewRating']

        except KeyError:
            raise ProductDataError
