from datetime import datetime
from django.test import TestCase

from authorizenet.cim import extract_form_data, extract_payment_form_data


class ExtractFormDataTests(TestCase):

    """Tests for utility functions converting form data to CIM data"""

    def test_extract_form_data(self):
        new_data = extract_form_data({'word': "1", 'multi_word_str': "2"})
        self.assertEqual(new_data, {'word': "1", 'multiWordStr': "2"})

    def test_extract_payment_form_data(self):
        data = extract_payment_form_data({
            'card_number': "1111",
            'expiration_date': datetime(2020, 5, 1),
            'card_code': "123",
        })
        self.assertEqual(data, {
            'cardNumber': "1111",
            'expirationDate': "2020-05",
            'cardCode': "123",
        })
