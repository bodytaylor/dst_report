# Get date time infomation
from datetime import date
today = date.today()
year = today.year
quarter = (today.month - 1) // 3 + 1
