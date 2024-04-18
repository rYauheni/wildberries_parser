import unittest
from unittest.mock import MagicMock

from exceptions.exceptions import FeedbackDataError
from models.feedback import Feedback


class TestFeedback(unittest.TestCase):
    def setUp(self):
        mock_feedback_detail = MagicMock()
        mock_feedback_detail.json.return_value = {
            'productValuation': 4,
            'text': 'Feedback text',
            'createdDate': '2024-04-04T22:22:22Z'
        }

        self.feedback = Feedback()
        self.feedback.get_feedback_data_from_json(feedback_detail=mock_feedback_detail.json())

    def test_get_feedback_data_from_json_valid(self):
        self.assertEqual(self.feedback.mark, 4)
        self.assertEqual(self.feedback.text, 'Feedback text')
        self.assertEqual(self.feedback.date, '2024-04-04T22:22:22Z')

    def test_get_feedback_data_from_json_invalid(self):
        mock_feedback_detail = MagicMock()
        mock_feedback_detail.json.return_value = {}

        feedback = Feedback()
        with self.assertRaises(FeedbackDataError):
            feedback.get_feedback_data_from_json(mock_feedback_detail.json())

    def test_is_new(self):
        new_last_update = '2024-04-06T22:22:22Z'
        old_last_update = '2024-04-02T22:22:22Z'
        self.assertTrue(self.feedback.is_new(old_last_update))
        self.assertFalse(self.feedback.is_new(new_last_update))

    def test_is_negative(self):
        negative_marks = (1, 2, 3, 4)
        positive_marks = (5,)
        for n_mark in negative_marks:
            self.feedback.mark = n_mark
            self.assertTrue(self.feedback.is_negative())
        for p_mark in positive_marks:
            self.feedback.mark = p_mark
            self.assertFalse(self.feedback.is_negative())


if __name__ == '__main__':
    unittest.main()
