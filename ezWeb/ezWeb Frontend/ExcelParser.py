
import time
import pandas as pd
import validators

from urllib.request import urlopen

# Use a hash to generate a file name.
# df.index.name = 'ID'
# df.to_excel('my_file.xlsx')

# Open excel file and read
def create_excel_template(num):
    file_name = str(num) + '.xlsx'
    df = pd.DataFrame({ 'Listing Title': ["Example"],
                        'Description': ["wer"],
                        'Property Type': ["wer"],
                        'Year Built': [2000],
                        'Price ($)': [5000000],
                        'Address': ["Bukit Timah Drive 15"],
                        'Tenure': ["Freehold"],
                        'Num. of Rooms': [5],
                        'Num. of Floors': [3],
                        'Total Area (sqft)': [3000],
                        'Floor': [6],
                        'Featured Photo': ["https://ibb.co/wSq1XPr"],
                        'Other Photos': ["https://ibb.co/wSq1XPr"]})
    df.to_excel(file_name)
    return file_name

def validate_inputs(filename):
    workbook = pd.read_excel(filename, sheet_name="Sheet1")
    total_rows = len(workbook.index)
    curr_row = 1
    while curr_row < total_rows:
        if workbook['Listing Title'].iloc[curr_row] != workbook['Listing Title'].iloc[curr_row]:
            return "Invalid Title added in row " + str(curr_row + 2)
        elif workbook['Description'].iloc[curr_row] != workbook['Description'].iloc[curr_row]:
            return "Invalid Description added in row " + str(curr_row + 2)
        elif workbook['Property Type'].iloc[curr_row] != workbook['Property Type'].iloc[curr_row]:
            return "Invalid Property Type added in row " + str(curr_row + 2)
        elif workbook['Price ($)'].iloc[curr_row].item() != workbook['Price ($)'].iloc[curr_row].item() or not validate_num(workbook['Price ($)'].iloc[curr_row].item()):
            return "Invalid Price added in row " + str(curr_row + 2)
        elif workbook['Year Built'].iloc[curr_row].item() != workbook['Year Built'].iloc[curr_row].item() or not validate_year_built(workbook['Year Built'].iloc[curr_row].item()):
            return "Invalid Year added in row " + str(curr_row + 2)
        elif workbook['Total Area (sqft)'].iloc[curr_row].item() != workbook['Total Area (sqft)'].iloc[curr_row].item() or not validate_num(workbook['Total Area (sqft)'].iloc[curr_row].item()):
            return "Invalid Total Area added in row " + str(curr_row + 2)
        elif workbook['Num. of Rooms'].iloc[curr_row].item() != workbook['Num. of Rooms'].iloc[curr_row].item() or not validate_num(workbook['Num. of Rooms'].iloc[curr_row].item()):
            return "Invalid Num. of Rooms added in row " + str(curr_row + 2)
        elif workbook['Num. of Floors'].iloc[curr_row].item() != workbook['Num. of Floors'].iloc[curr_row].item() or not validate_num(workbook['Num. of Floors'].iloc[curr_row].item()):
            return "Invalid Num. of Floors added in row " + str(curr_row + 2)
        elif workbook['Floor'].iloc[curr_row].item() != workbook['Floor'].iloc[curr_row].item() or not validate_num(workbook['Floor'].iloc[curr_row].item()):
            return "Invalid Floor added in row " + str(curr_row)
        elif workbook['Featured Photo'].iloc[curr_row] != workbook['Featured Photo'].iloc[curr_row] or not validate_url_image(workbook['Featured Photo'].iloc[curr_row]):
            return "Invalid Featured Photo link added in row " + str(curr_row + 2)
        else:
            other_photos = workbook['Other Photos'].iloc[curr_row]
            if other_photos != other_photos:
                return "Invalid Other Photos link added in row " + str(curr_row + 2)
            photos = other_photos.split("\n")
            num = 1
            for photo in photos:
                if not validate_url_image(photo):
                    return "Invalid Other Photos link added in row " + str(curr_row + 2) + " at line " + str(num)
                num += 1
        curr_row += 1
    return "Valid"

def validate_year_built(year):
    print("Validating year...")
    if year <= 2050 and year >= 1900:
        return True
    return False

def validate_num(num):
    print("Validating num...")
    if isinstance(num, (int, float, complex)):
        return True
    if isinstance(num, str):
        if num.is_numeric():
            return True
    return False

def is_url_image(image_url):
    if "i.ibb.co/" in image_url:
        if image_url.endswith(".png") or image_url.endswith(".jpg") or image_url.endswith(".jpeg") or image_url.endswith(".webp"):
            return True
    return False

def check_url(url):
    return validators.url(url)

def validate_url_image(url):
    print("Validating url/image")
    return check_url(url) and is_url_image(url)

def parse_excel_file(file_name):
    workbook = pd.read_excel(file_name, sheet_name="Sheet1")
    total_rows = len(workbook.index)
    total_rows -= 1
    listings = []
    curr_row = 0
    while curr_row + 1 < total_rows:
        print(workbook['Property Type'].iloc[curr_row])
        listings.append({})
        new_listing = listings[curr_row]
        new_listing['title'] = workbook['Listing Title'].iloc[curr_row]
        new_listing['content'] = workbook['Description'].iloc[curr_row]
        new_listing['property_type'] = workbook['Property Type'].iloc[curr_row]
        new_listing['year_built'] = workbook['Year Built'].iloc[curr_row].item()
        new_listing['price'] = workbook['Price ($)'].iloc[curr_row].item()
        new_listing['address'] = workbook['Address'].iloc[curr_row]
        new_listing['tenure'] = workbook['Tenure'].iloc[curr_row]
        new_listing['number_of_rooms'] = workbook['Num. of Rooms'].iloc[curr_row].item()
        new_listing['level'] = workbook['Num. of Floors'].iloc[curr_row].item()
        new_listing['total_area'] = workbook['Total Area (sqft)'].iloc[curr_row].item()
        new_listing['floor'] = workbook['Floor'].iloc[curr_row].item()
        new_listing['featured_photo_file_path'] = workbook['Featured Photo'].iloc[curr_row]
        other_photos = workbook['Other Photos'].iloc[curr_row]
        photos = other_photos.split('\n')
        new_listing['extra_photos'] = []
        for photo in photos:
            new_listing['extra_photos'].append(photo)
        curr_row += 1
    return listings

#create_excel_template(6)
print(validate_inputs('1001.xlsx'))
#parse_excel_file('6.xlsx')
