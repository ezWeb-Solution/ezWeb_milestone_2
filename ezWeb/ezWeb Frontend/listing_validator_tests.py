import unittest
from listing_validator import validate_property_details

class ListingValidatorTests(unittest.TestCase):
    def test_valid_1(self):
        self.assertEqual(validate_property_details("Condominium\n4 Rooms\n2017\n9 Kallang Pudding Rd, #14-18\nFreehold\n1400 sq ft\n14th floor\n2\n$1,100,000"),
                         "Valid")

    def test_valid_2(self):
        self.assertEqual(validate_property_details("Condominium\n4 Room\n2017\n9 Kallang Pudding Rd, #14-18\n99 years\n1400 sq. ft\n1st floor\n2\n$21,100,000"),
                         "Valid")

    def test_valid_3(self):
        self.assertEqual(validate_property_details("Condominium\n4 rooms\n2017\n9 Kallang Pudding Rd, #14-18\nFreehold\n1400 sq. ft.\n8th floor\n2\n$1138201"),
                         "Valid")

    def test_invalid_price_1(self):
        self.assertEqual(validate_property_details("Condominium\n4 rooms\n2017\n9 Kallang Pudding Rd, #14-18\nFreehold\n1400 sq. ft.\n8th floor\n2\n1231982"),
                         "Your entry for 'Price' is invalid.\n\nPlease submit your property details again and follow one of the following format:\nExample 1: $1,000,000\nExample 2: $1000000")

    def test_invalid_price_2(self):
        self.assertEqual(validate_property_details("Condominium\n4 rooms\n2017\n9 Kallang Pudding Rd, #14-18\nFreehold\n1400 sq. ft.\n8th floor\n2\n$2ee"),
                         "Your entry for 'Price' is invalid.\n\nPlease submit your property details again and follow one of the following format:\nExample 1: $1,000,000\nExample 2: $1000000")

    def test_valid_4(self):
        self.assertEqual(validate_property_details("Condominium\n4 rooms\n2017\n9 Kallang Pudding Rd, #14-18\n99-year\n1400 sq. ft.\n8th floor\n2\n$1138201"),
                         "Valid")

    def test_invalid_year_built_1(self):
        self.assertEqual(validate_property_details("Condominium\n4 rooms\n1900\n9 Kallang Pudding Rd, #14-18\n99-year\n1400 sq. ft.\n8th floor\n2\n$1138201"),
            "Your entry for 'Year Built' is invalid.\n\nPlease submit your property details again and follow the following format:\nExample: 2005")

    def test_invalid_year_built_2(self):
        self.assertEqual(validate_property_details("Condominium\n4 rooms\n3000\n9 Kallang Pudding Rd, #14-18\n99-year\n1400 sq. ft.\n8th floor\n2\n$1138201"),
            "Your entry for 'Year Built' is invalid.\n\nPlease submit your property details again and follow the following format:\nExample: 2005")

    def test_invalid_year_built_3(self):
        self.assertEqual(validate_property_details("Condominium\n4 rooms\n2904\n9 Kallang Pudding Rd, #14-18\n99-year\n1400 sq. ft.\n8th floor\n2\n$1138201"),
            "Your entry for 'Year Built' is invalid.\n\nPlease submit your property details again and follow the following format:\nExample: 2005")

    def test_invalid_tenure_1(self):
        self.assertEqual(validate_property_details("Condominium\n4 rooms\n2017\n9 Kallang Pudding Rd, #14-18\n180\n1400 sq. ft.\n8th floor\n2\n$1138201"),
            "Your entry for 'Tenure' is invalid.\n\nPlease submit your property details again and follow the following format:\nExample 1: 99 Years\nExample 2:Freehold\nExample 3: 999 Years")

    def test_invalid_tenure_2(self):
        self.assertEqual(validate_property_details(
            "Condominium\n4 rooms\n2017\n9 Kallang Pudding Rd, #14-18\nlong\n1400 sq. ft.\n8th floor\n2\n$1138201"),
                         "Your entry for 'Tenure' is invalid.\n\nPlease submit your property details again and follow the following format:\nExample 1: 99 Years\nExample 2:Freehold\nExample 3: 999 Years")

    def test_invalid_area_1(self):
        self.assertEqual(validate_property_details("Condominium\n4 rooms\n2017\n9 Kallang Pudding Rd, #14-18\n99-year\n1400sqft.\n8th floor\n2\n$1138201"),
            "Your entry for 'Total Area' is invalid.\n\nPlease submit your property details again and follow the following format:\nExample 1: 1900 sqft\nExample 2: 1549 sqft\nExample 3: 4900 sqft")

    def test_invalid_area_1(self):
        self.assertEqual(validate_property_details("Condominium\n4 rooms\n2017\n9 Kallang Pudding Rd, #14-18\n99-year\n1400s\n8th floor\n2\n$1138201"),
            "Your entry for 'Total Area' is invalid.\n\nPlease submit your property details again and follow the following format:\nExample 1: 1900 sqft\nExample 2: 1549 sqft\nExample 3: 4900 sqft")

if __name__ == '__main__':
    unittest.main()
