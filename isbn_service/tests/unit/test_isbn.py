import unittest

from isbn_service import isbn_service


class IsbnTest(unittest.TestCase):
    def test_isbn_format(self):
        isbn13 = isbn_service.format_isbn("978-0060977580")
        self.assertEqual(isbn13, "9780060977580")

    def test_isbn_validate(self):
        with self.assertRaises(isbn_service.InvalidISBN):
            isbn_service.validate_isbn("1")

        with self.assertRaises(isbn_service.InvalidISBN):
            isbn_service.validate_isbn("a")


if __name__ == '__main__':
    unittest.main()
