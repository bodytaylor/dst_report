import pandas as pd
import glob
import os.path

# setting the path for joining multiple files
path = os.path.join(f"data/{quarter}/*dst_revenue.csv")

# list of merged files returned
files = glob.glob(path)

# joining files with concat and read_csv
df_report = pd.concat(map(pd.read_csv, files), ignore_index=True)
df_report = df_report.drop(columns=['Name'])
df_report.head()

# Define function to map prices to packages
def get_package(price):
    package_dict = {
        1500: 'Gopro rental',
        5000: 'Capture Moment Package',
        0: 'Photography Discount',
        9000: 'Moving memories package',
    }
    if price in package_dict:
        return package_dict[price]
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