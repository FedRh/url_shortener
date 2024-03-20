import unittest
import random
from unittest.mock import patch, ANY
from datetime import datetime, timedelta

from url_shortener import shorten_url, expand_url, CHARACTERS


class TestShortenUrl(unittest.TestCase):

    @patch("url_shortener.collection.find_one")
    def test_existing_url_not_expired(self, mock_find_one):
        # database response mock for an existing URL
        mock_find_one.return_value = {
            "original_url": "https://www.ogtesturl.com",
            "short_url": "https://www.shorttesturl.com/AAAAA",
            "expiration_time": datetime.utcnow() + timedelta(days=7)
        }
        original_url = "https://www.ogtesturl.com"
        short_url = shorten_url(original_url)
        self.assertEqual(short_url, mock_find_one.return_value["short_url"])  # Assert returned short URL

    @patch("url_shortener.collection.insert_one")
    def test_shorten_new_url(self, mock_insert_one):
        original_url = "https://www.ogtesturl.com"
        short_url = shorten_url(original_url)
        mock_insert_one.assert_called_once_with(
            {
                "original_url": original_url,
                "short_url": ANY,
                "expiration_time": ANY
            }
        )


class TestExpandUrl(unittest.TestCase):

    @patch("url_shortener.collection.find_one")
    def test_expand_valid_url(self, mock_find_one):
        # database response mock for a valid URL
        mock_find_one.return_value = {
            "original_url": "https://www.ogtesturl.com",
            "short_url": "https://www.shorttesturl.com/AAAAA",
            "expiration_time": datetime.utcnow() + timedelta(days=1)
        }
        short_url = "https://www.shorttesturl.com/AAAAA"
        original_url = expand_url(short_url)
        self.assertEqual(original_url, mock_find_one.return_value["original_url"])

    @patch("url_shortener.collection.find_one")
    def test_expand_expired_url(self, mock_find_one):
        mock_find_one.return_value = {
            "original_url": "https://www.ogtesturl.com",
            "short_url": "https://www.shorttesturl.com/AAAAA",
            "expiration_time": datetime.utcnow() - timedelta(days=1)
        }
        short_url = "https://www.shorttesturl.com/AAAAA"
        original_url = expand_url(short_url)
        self.assertEqual(original_url, "The link has expired.")

    def test_expand_invalid_url(self):
        short_url = "invalid_url"
        original_url = expand_url(short_url)
        self.assertEqual(original_url, "Invalid link.")


# Informative test for short code collision probability
def test_collision_probability(n_trials=10000, code_length=5):
    existing_codes = set()
    collisions = 0
    for _ in range(n_trials):
        code = ''.join(random.choices(CHARACTERS, k=code_length))
        if code in existing_codes:
            collisions += 1
        existing_codes.add(code)
    collision_rate = collisions / n_trials
    print(f"Collision rate for {n_trials} trials with {code_length}-character code length: {collision_rate:.4f} ({collisions} collisions) ")


if __name__ == '__main__':
    unittest.main()

test_collision_probability()
