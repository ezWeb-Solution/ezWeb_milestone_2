import re

def validate_property_details(property_details):
    details = property_details.split('\n')
    num_rooms = details[1]
    year_built = details[2]
    tenure = details[4]
    total_area = details[5]
    floor = details[6]
    number_of_storeys = details[7]
    price = details[8]
    if not validate_num_rooms(num_rooms):
        return "Your entry for 'Number of rooms' is invalid.\n\nPlease submit your property details again and follow one of the following formats:\nExample 1: 4 Rooms\nExample 2: 4 Room\nExample 3: 4"
    if not validate_year_built(year_built):
        return "Your entry for 'Year Built' is invalid.\n\nPlease submit your property details again and follow the following format:\nExample: 2005"
    if not validate_tenure(tenure):
        return "Your entry for 'Tenure' is invalid.\n\nPlease submit your property details again and follow the following format:\nExample 1: 99 Years\nExample 2:Freehold\nExample 3: 999 Years"
    if not validate_total_area(total_area):
        return "Your entry for 'Total Area' is invalid.\n\nPlease submit your property details again and follow the following format:\nExample 1: 1900 sqft\nExample 2: 1549 sqft\nExample 3: 4900 sqft"
    if not validate_floor(floor):
        return "Your entry for 'Floor' is invalid.\n\nPlease submit your property details again and follow one of the following formats:\nExample 1: 14th Floor\nExample 2: 14\nExample 3: 8"
    if not validate_number_of_storeys(number_of_storeys):
        return "Your entry for 'Number of Storeys' is invalid.\n\nPlease submit your property details again and follow the following format. (If the property you are listing is a Condominium or HDB, just enter '1' for the 'Number of Storeys' field)\nExample 1: 4\nExample 2:1\nExample 3: 2"
    if not validate_price(price):
        return "Your entry for 'Price' is invalid.\n\nPlease submit your property details again and follow one of the following format:\nExample 1: $1,000,000\nExample 2: $1000000"
    return "Valid"

def validate_price(price):
    if price.isnumeric():
        return False
    info = price.split("$")
    if len(info) != 2:
        return False
    val = info[1]
    if val.isnumeric():
        return True
    if re.fullmatch(r'(\d{0,3},)?(\d{3},)?\d{0,3}', val):
        return True
    return False

def validate_number_of_storeys(number_of_storeys):
    if number_of_storeys.isnumeric():
        return True
    return False

def validate_floor(floor):
    if "floor" in floor or "Floor" in floor:
        info = floor.split(" ")
        if info[0].isnumeric():
            return True
        else:
            if len(info[0]) < 3:
                return False
            number_th = info[0][len(info[0]) - 2:]
            if number_th == "th" or number_th == "nd" or number_th == "st":
                if info[0][0].isnumeric():
                    return True
        return False
    else:
        if floor.isnumeric():
            return True
    return False
def validate_total_area(total_area):
    if "sqft" in total_area or "sq ft" in total_area or "sq. ft." in total_area or "sq. ft" in total_area or "sq ft." in total_area:
        info = total_area.split(" ")
        if info[0].isnumeric():
            return True
    return False

def validate_tenure(tenure):
    if tenure.isnumeric():
        return False
    elif "leasehold" in tenure or "Leasehold" in tenure or "Freehold" in tenure or "freehold" in tenure:
        return True
    elif "Years" in tenure or "years" in tenure:
        info = tenure.split(" ")
        if len(info) == 2:
            num = info[0]
            if num.isnumeric():
                return True
        return False
    elif "Year" in tenure or "year" in tenure:
        info = tenure.split(" ")
        info2 = tenure.split("-")
        if len(info) == 2:
            num = info[0]
            if num.isnumeric():
                return True
        elif len(info2) == 2:
            num = info2[0]
            if num.isnumeric():
                return True
        return False
    else:
        return False

def validate_year_built(year_built):
    if year_built.isnumeric():
        year = int(year_built)
        if year < 2050 and year > 1950:
            return True
    return False

def validate_num_rooms(num_rooms):
    info = num_rooms.split(" ")
    if len(info) == 2:
        room = info[1].lower()
        num = info[0]
        if room == "Room" or room == "room" or room == "Rooms" or room == "rooms":
            if num.isnumeric():
                return True
    elif len(info) == 1:
        if info[0].isnumeric():
            return True
    return False
# validate_property_details("Condominium\n4 rooms\n2017\n9 Kallang Pudding Rd, #14-18\nFreehold\n1400 sq. ft.\n8th floor\n2\n$2ee")
# print(re.fullmatch(r'(\d{0,3},)?(\d{3},)?\d{0,3}', "2ee"))
# print(re.search(r'(\d{0,3},)?(\d{3},)?\d{0,3}', "1000000"))
# print(re.search(r'(\d{0,3},)?(\d{3},)?\d{0,3}', "932832"))
# print(re.search(r'(\d{0,3},)?(\d{3},)?\d{0,3}', "938,320"))
# print(re.search(r'(\d{0,3},)?(\d{3},)?\d{0,3}', "20,938,320"))

