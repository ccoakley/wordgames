import unittest
from io import StringIO
from unittest.mock import (
  MagicMock,
  patch
)

from words import (
  Words,
  remove_nonalphanumeric,
  decompose
)

class TestWordsUtilities(unittest.TestCase):
  def test_remove_nonalphanumeric(self):
    ret = remove_nonalphanumeric(' b_2 !b"')
    self.assertEqual(ret, 'b2b')

  @patch('words.requests')
  @patch('sys.stdout', new_callable=StringIO)
  def test_decompose(self, mock_stdout, mock_requests):
    response = MagicMock()
    response.status_code = 200
    response.text = "a\naye\ncab"
    mock_requests.get.return_value = response

    decompose("baye")

    mock_requests.get.assert_called_once()
    self.assertEqual(mock_stdout.getvalue(), "a\naye\n")

class TestWords(unittest.TestCase):
  @patch('words.requests')
  def test_load_words(self, mock_requests):
    words = Words(dictionary_url="https://fakurl.com/")
    response = MagicMock()
    response.status_code = 200
    response.text = "a\naye"
    mock_requests.get.return_value = response

    res = words.load_words()

    mock_requests.get.assert_called_once_with("https://fakurl.com/")
    self.assertEqual(res, ["a", "aye"])


  def test_preprocess_dict(self):
    words = Words(dictionary_url="https://fakurl.com/")
    words.words = ["bad", "dab"]

    ret = words.preprocess_dict()

    self.assertIn("abd", ret)
    self.assertIn("bad", ret["abd"])
    self.assertIn("dab", ret["abd"])

  def test_decompose(self):
    words = Words(dictionary_url="https://fakurl.com/")
    words.words = ["bad", "dab", "cab"]
    words.preprocess_dict()

    ret = words.decompose("bade")

    self.assertIn("bad", ret)
    self.assertIn("dab", ret)
    self.assertNotIn("cab", ret)

if __name__ == '__main__':
    unittest.main()
