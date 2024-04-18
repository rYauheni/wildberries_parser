import requests
import unittest

from models.product import Product


class TestWildberriesConnections(unittest.TestCase):
    def setUp(self):
        self.product = Product(id=54978961)
        self.product.root = 41071242

    def test_connect_product_detail_url_success(self):
        self.product.get_product_detail_url()
        response = requests.get(self.product.url)
        self.assertEqual(response.status_code, 200)

    def test_connect_feedbacks_urls_success(self):
        feedbacks_urls = self.product.get_feedbacks_urls()
        for url in feedbacks_urls:
            response = requests.get(url)
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
