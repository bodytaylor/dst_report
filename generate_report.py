import pandas as pd
import glob
from get_file_from_bucket import quarter, year
import os.path

# setting the path for joining multiple files
files = os.path.join("*dst_revenue.csv")

# list of merged files returned
files = glob.glob(files)

# joining files with concat and read_csv
df_report = pd.concat(map(pd.read_csv, files), ignore_index=True)
df_report = df_report.drop(columns=['Name'])
df_report.head()

# Define function to map prices to packages
def get_package(price):
    if price == 1500:
        return 'Gopro rental'
    elif price == 5000:
        return 'Capture Moment Package'
    elif price == 0:
        return 'Photography Discount'
    elif price == 9000:
        return 'Moving memories package'
    elif price > 9000 and price <= 15000:
        return 'Rare Experience Package'
    elif price > 36000:
        return 'Your Soneva Journey Package'
    else:
        return 'Custom Package'

# Apply mapping function to "Debit" column to create new "Package" column
df_report['Package'] = df_report['Debit'].apply(get_package)


# Save the dataframe to an Excel file
writer = pd.ExcelWriter(f'{year}_q{quarter}_dst_report.xlsx')
df_report.to_excel(writer, index=False)
writer.save()