import unittest
from ExcelParser import validate_inputs

class TestExcelParser(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(validate_inputs("Valid.xlsx"), "Valid")  # add assertion here

    def test_invalid_area(self):
        self.assertEqual(validate_inputs("InvalidArea.xlsx"), "Invalid Total Area added in row 4")

    def test_invalid_description(self):
        self.assertEqual(validate_inputs("InvalidDescription.xlsx"), "Invalid Description added in row 4")

    def test_invalid_featured_photo(self):
        self.assertEqual(validate_inputs("InvalidFeaturedPhoto.xlsx"), "Invalid Featured Photo link added in row 4")

    def test_invalid_num_of_floors(self):
        self.assertEqual(validate_inputs("InvalidNumOfFloors.xlsx"), "Invalid Num. of Floors added in row 6")

    def test_invalid_other_photo(self):
        self.assertEqual(validate_inputs("InvalidOtherPhoto.xlsx"), "Invalid Other Photos link added in row 6 at line 2")

    def test_invalid_price(self):
        self.assertEqual(validate_inputs("InvalidPrice.xlsx"), "Invalid Price added in row 3")

    def test_invalid_room(self):
        self.assertEqual(validate_inputs("InvalidRoom.xlsx"), "Invalid Num. of Rooms added in row 6")

    def test_invalid_title(self):
        self.assertEqual(validate_inputs("InvalidTitle.xlsx"), "Invalid Title added in row 3")

    def test_invalid_year(self):
        self.assertEqual(validate_inputs("InvalidYear.xlsx"), "Invalid Year added in row 5")

    def test_invalid_floor(self):
        self.assertEqual(validate_inputs("InvalidFloor.xlsx"), "Invalid Floor added in row 3")

if __name__ == '__main__':
    unittest.main()
