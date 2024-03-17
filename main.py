# main.py

import os
from dotenv import load_dotenv

from src.api_manager import EconomicDataAPI
from src.helpers import (
    fetch_category_ids,
    fetch_series_data_for_categories,
    convert_to_dataframes,
    write_dataframes_to_csv
)

load_dotenv()


def main():
    
    # Get environment vars
    API_KEY = os.getenv('ECONOMIC_DATA_API_KEY')
    PATH = 'datasets/generated_by_main/'

    # Initialize api manager
    economic_api = EconomicDataAPI(API_KEY)
    
    # Gather unique identifiers for categories based on prompt
    category_ids_list = fetch_category_ids(economic_api)
    print(category_ids_list)

    # Compile economic data based on the identified categories
    all_series = fetch_series_data_for_categories(economic_api, category_ids_list)

    # Organize the economic data into dataframes
    category_dataframes = convert_to_dataframes(all_series)

    # Write files for analysis
    write_dataframes_to_csv(category_dataframes, PATH)
    
    
if __name__ == '__main__':
    main()
