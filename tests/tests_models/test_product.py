import unittest
from unittest.mock import MagicMock

from exceptions.exceptions import ProductDataError, FeedbackDataError
from models.product import Product


class TestProductMethods(unittest.TestCase):

    def test_get_product_data_from_json_valid(self):
        mock_product_detail = MagicMock()
        mock_product_detail.json.return_value = {
            'data': {
                'products': [{
                    'root': 123,
                    'brand': 'Brand',
                    'name': 'Product Name',
                    'reviewRating': 4.5
                }]
            }
        }

        product = Product(id=111)
        product.get_product_data_from_json(mock_product_detail)

        self.assertEqual(product.root, 123)
        self.assertEqual(product.name, 'Brand Product Name')
        self.assertEqual(product.rating, 4.5)

    def test_get_product_data_from_json_invalid(self):
        mock_product_detail = MagicMock()
        mock_product_detail.json.return_value = {}

        product = Product(111)
        with self.assertRaises(ProductDataError):
            product.get_product_data_from_json(mock_product_detail)

    def test_get_product_detail_url(self):
        product = Product(id=111)

        product.get_product_detail_url()

        expected_url = 'https://card.wb.ru/cards/detail?nm=111'
        self.assertEqual(product.url, expected_url)

    def test_get_feedbacks_urls(self):
        product = Product(id=111, root=123)

        feedbacks_urls = product.get_feedbacks_urls()

        expected_urls = [
            'https://feedbacks1.wb.ru/feedbacks/v1/123',
            'https://feedbacks2.wb.ru/feedbacks/v1/123'
        ]
        self.assertEqual(feedbacks_urls, expected_urls)

    def test_get_negative_feedbacks_valid(self):
        # Подготовка данных для теста
        product = Product(id=111)
        product.last_update = '2024-01-01T01:01:01Z'
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'root': 123,
            'feedbacks': [{
                'createdDate': '2024-01-02T01:01:01Z',
                'text': 'Negative feedback',
                'productValuation': 1,
            }]
        }
        mock_get = MagicMock(return_value=mock_response)
        feedbacks_urls = ['https://feedbacks1.wb.ru/feedbacks/v1/123']

        with unittest.mock.patch('requests.get', mock_get):
            product.get_negative_feedbacks(feedbacks_urls)

        self.assertEqual(len(product.feedbacks), 1)
        self.assertEqual(product.last_update, '2024-01-02T01:01:01Z')

    def test_get_negative_feedbacks_invalid(self):
        product = Product(id=111)
        mock_get = MagicMock(side_effect=Exception())
        feedbacks_urls = ['https://feedbacks1.wb.ru/feedbacks/v1/123']

        with unittest.mock.patch('requests.get', mock_get):
            with self.assertRaises(FeedbackDataError):
                product.get_negative_feedbacks(feedbacks_urls)

    def test_parse_product_data_valid(self):
        mock_response = MagicMock()

        mock_product_detail = MagicMock()
        mock_product_detail.json.return_value = {
            'data': {
                'products': [{
                    'root': 123,
                    'brand': 'Brand',
                    'name': 'Product Name',
                    'reviewRating': 4.5
                }]
            }
        }

        product = Product(id=111)
        product.get_product_data_from_json(mock_product_detail)

        mock_get = MagicMock(return_value=mock_response)
        mock_get_feedbacks = MagicMock(return_value=['https://feedbacks1.wb.ru/feedbacks/v1/123'])
        product.get_product_detail_url = MagicMock()
        product.get_product_data_from_json = MagicMock()
        product.get_feedbacks_urls = MagicMock(return_value=['https://feedbacks1.wb.ru/feedbacks/v1/123'])

        with unittest.mock.patch('requests.get', mock_get):
            with unittest.mock.patch.object(product, 'get_negative_feedbacks', mock_get_feedbacks):
                product.parse_product_data()

        self.assertEqual(product.root, 123)
        self.assertEqual(product.name, 'Brand Product Name')
        self.assertEqual(product.rating, 4.5)

    def test_parse_product_data_invalid_request(self):
        product = Product(id=111)
        mock_get = MagicMock(side_effect=Exception())

        with unittest.mock.patch('requests.get', mock_get):
            with self.assertRaises(ProductDataError):
                product.parse_product_data()

#
# if __name__ == '__main__':
#     unittest.main()
