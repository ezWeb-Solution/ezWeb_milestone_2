import unittest
from ExcelParser import validate_num, validate_year_built, validate_url_image

class ValidationTests(unittest.TestCase):
    def test_year_1(self):
        self.assertEqual(validate_year_built(1950), True)

    def test_year_2(self):
        self.assertEqual(validate_year_built(1970), True)

    def test_year_3(self):
        self.assertEqual(validate_year_built(2000), True)

    def test_year_4(self):
        self.assertEqual(validate_year_built(2010), True)

    def test_year_5(self):
        self.assertEqual(validate_year_built(2060), False)

    def test_year_6(self):
        self.assertEqual(validate_year_built(900), False)

    def test_year_7(self):
        self.assertEqual(validate_year_built(3000), False)

    def test_num_1(self):
        self.assertEqual(validate_num(1), True)

    def test_num_2(self):
        self.assertEqual(validate_num("Err"), False)

    def test_num_3(self):
        self.assertEqual(validate_num("Wow!!"), False)

    def test_validate_url_image_1(self):
        self.assertEqual(validate_url_image("www.google.com"), False)

    def test_validate_url_image_2(self):
        self.assertEqual(validate_url_image("www.reddit.com"), False)

    def test_validate_url_image_3(self):
        self.assertEqual(validate_url_image("https://ibb.co/wSq1XPr"), False)

    def test_validate_url_image_4(self):
        self.assertEqual(validate_url_image("https://i.ibb.co/D9Fnyvg/image-1-768x1055.png"), True)


if __name__ == '__main__':
    unittest.main()

