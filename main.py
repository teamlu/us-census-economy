# main.py

import os
from dotenv import load_dotenv

from src.api_manager import EconomicDataAPI
from src.helpers import (
    fetch_category_ids,
    fetch_series_data_for_categories,
    fetch_observations,
    convert_to_dataframes,
    write_dataframes_to_csv
)

load_dotenv()

# Pre-curated after exploring the category dataframes
construction_segments = {
    'TLAMUSCONS': 'Total Construction Spending: Amusement and recreation',
    'TLCADCONS': 'Total Construction Spending: Conservation and development',
    'TLCMUCONS': 'Total Construction Spending: Communication',
    'TLCOMCONS': 'Total Construction Spending: Commercial',
    'TLEDUCONS': 'Total Construction Spending: Educational',
    'TLHLTHCONS': 'Total Construction Spending: Health Care',
    'TLHWYCONS': 'Total Construction Spending: Highway and street',
    'TLLODGCONS': 'Total Construction Spending: Lodging',
    'TLMFGCONS': 'Total Construction Spending: Manufacturing',
    'TLNRESCONS': 'Total Construction Spending: Nonresidential',
    'TLOFCONS': 'Total Construction Spending: Office',
    'TLPWRCONS': 'Total Construction Spending: Power',
    'TLRELCONS': 'Total Construction Spending: Religious',
    'TLRESCONS': 'Total Construction Spending: Residential',
    'TLSWDCONS': 'Total Construction Spending: Sewage and waste disposal',
    'TLTRANSCONS': 'Total Construction Spending: Transportation',
    'TLWSCONS': 'Total Construction Spending: Water Supply',
    'TTLCONS': 'Total Construction Spending'
}

def main():
    
    # Get environment vars
    API_KEY = os.getenv('ECONOMIC_DATA_API_KEY')
    PATH = 'datasets/generated_by_main/'

    # Initialize api manager
    economic_api = EconomicDataAPI(API_KEY)
    date_start_input = input("Enter series start date, as YYYY-MM-DD: ")
    
    # Gather unique identifiers for categories based on prompt
    category_ids_list = fetch_category_ids(economic_api)
    print(category_ids_list)

    # Compile economic data based on the identified categories
    all_series = fetch_series_data_for_categories(economic_api, category_ids_list, date_start_input)

    # Get data observations
    full_observations = fetch_observations(economic_api, construction_segments, date_start_input)
    
    # Organize the economic data into dataframes
    category_dataframes = convert_to_dataframes(all_series, nested_key='seriess')
    observations_dataframes = convert_to_dataframes(full_observations, nested_key='observations', construction_segments_dict=construction_segments)

    # Write files for analysis
    write_dataframes_to_csv(category_dataframes, PATH, save_string='category_dataframe')
    write_dataframes_to_csv(observations_dataframes, PATH, save_string='observation_dataframe')
    
if __name__ == '__main__':
    main()
