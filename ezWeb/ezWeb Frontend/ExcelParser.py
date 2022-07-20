import pandas as pd
# Open excel file and read
workbook = pd.read_excel('sample-xlsx-file-for-testing.xlsx', sheet_name="Sheet1")
workbook = pd.read_excel('sample-xlsx-file-for-testing.xlsx', sheet_name="Sheet2")

print(workbook['Listing'].iloc[0])

workbook.head()

# Create a new file
name = ['John', 'Mary', 'Sherlock']
age = [11, 12, 13]
df = pd.DataFrame({ 'Name': name, 'Age': age })
df.index.name = 'ID'
df.to_excel('my_file.xlsx')
