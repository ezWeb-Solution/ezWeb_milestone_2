
import time
import pandas as pd
# Open excel file and read
workbook = pd.read_excel('sample-xlsx-file-for-testing.xlsx', sheet_name="Sheet1")
workbook = pd.read_excel('sample-xlsx-file-for-testing.xlsx', sheet_name="Sheet2")

listings = []
curr_row = 2
while workbook['Property Name'].iloc[curr_row] is not None:
    listings.append({})
    new_listing = listings[curr_row - 2]
    new_listing['property_type'] = workbook['Property Type'].iloc[curr_row]
    new_listing['year_built'] = workbook['Year Built'].iloc[curr_row]
    new_listing['price'] = workbook['Price'].iloc[curr_row]
    new_listing['address'] = workbook['Address'].iloc[curr_row]
    new_listing['tenure'] = workbook['Tenure'].iloc[curr_row]
    new_listing['num_rooms'] = workbook['Num. of Rooms'].iloc[curr_row]
    new_listing['number_of_storeys'] = workbook['Num. of Floors'].iloc[curr_row]
    new_listing['total_area'] = workbook['Total Area (sqft)'].iloc[curr_row]
    new_listing['floor'] = workbook['Floor'].iloc[curr_row]
    new_listing['featured_photo'] = workbook['Featured Photo'].iloc[curr_row]
    other_photos = workbook['Other Photos'].iloc[curr_row]
    photos = other_photos.split('\n')
    new_listing['other_photos'] = []
    for photo in photos:
        new_listing['other_photos'].append(photo)
    curr_row += 1
print(workbook['Property Name'].iloc[0])

# Output
for listing in listings:
    ## Calls create listing and sends listing to the backend.
    #create_new_listing(listing)
    time.sleep(10)
workbook.head()


# Create a new file

df = pd.DataFrame({ 'Property Type': [],
                    'Year Built': [],
                    'Price': [],
                    'Address': [],
                    'Tenure': [],
                    'Num. of Rooms': [],
                    'Num. of Floors': [],
                    'Total Area (sqft)': [],
                    'Floor': [],
                    'Featured_Photo': [],
                    'Other Photos': []})

# Use a hash to generate a file name.
df.index.name = 'ID'
df.to_excel('my_file.xlsx')

