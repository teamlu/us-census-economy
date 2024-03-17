# %% exploration.py
# SETUP
import os
import sys
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.api_manager import EconomicDataAPI

load_dotenv()

API_KEY = os.getenv('ECONOMIC_DATA_API_KEY')

economic_api = EconomicDataAPI(API_KEY)

# %%
# EXTRACTION
categories_data = economic_api.get_series_categories(
    # series_id='TTLCONS',       # Total Construction Spending 32436
    # series_id='USCONS',        # Employees in Construction   32310
    # series_id='CES2000000003', # Average Hourly Earnings of employees in Construction  32310
    series_id='WPUSI012011',   # Average Hourly Earnings of employees in Construction  33580 
    file_type='json'
    )
print(categories_data)

series_in_category_data = economic_api.get_series_in_category(
    # category_id=32436, 
    category_id=32310, 
    # category_id=33580, 
    file_type='json')
print(series_in_category_data)


# Low Priority: return series by series_id   

# economic_data = economic_api.get_economic_series(
#     # series_id='TTLCONS', 
#     series_id='CES2000000003',
#     file_type='json'
#     )
# print(economic_data)

# Low Priority: return category children by category_id

# child_categories_data = economic_api.get_category_children(category_id=32436, file_type='json')
# print(child_categories_data)

# %%
