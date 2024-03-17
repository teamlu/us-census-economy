import pandas as pd
import os


def fetch_category_ids(economic_api):
    series_ids = [
        ('TTLCONS', 'Total Construction Spending'),
        ('USCONS', 'Employees in Construction'),
        ('CES2000000003', 'Average Hourly Earnings of employees in Construction'),
        ('WPUSI012011', 'Average Price Index for Construction')
    ]
    
    category_ids = []
    
    for series_id, description in series_ids:
        categories_data = economic_api.get_series_categories(series_id=series_id, file_type='json')
        if categories_data and 'categories' in categories_data:
            category_id = categories_data['categories'][0]['id'] if categories_data['categories'] else 'Not Found'
            category_ids.append(str(category_id))
            print(f'{description}: {category_id}')
        else:
            category_ids.append('Not Found')
            print(f'{description}: Not Found')
    
    return category_ids


def fetch_series_data_for_categories(economic_api, category_ids_list, date_string):
    series_data_objects = {}

    for category_id in set(category_ids_list):
        series_data = economic_api.get_series_in_category(
            category_id=category_id, 
            realtime_start=date_string,
            file_type='json')
        
        series_data_objects[category_id] = series_data
        
        print(f'Extracted {category_id}\'s series')
    
    return series_data_objects


def fetch_observations(economic_api, dict_of_series, date_string):
    economic_data_json = {}

    for series_id, series_description in dict_of_series.items():
        economic_data = economic_api.get_observations(
            series_id=series_id,
            file_type='json',
            realtime_start=date_string
        )

        economic_data_json[series_id] = economic_data
        print(f"Extracted observations for {series_description}")

    return economic_data_json


def convert_to_dataframes(series_data_objects, nested_key, construction_segments_dict=None):

    dataframes_list = []

    if isinstance(series_data_objects, dict):
        series_data_iterable = series_data_objects.values()
    else:
        series_data_iterable = series_data_objects

    if nested_key == 'observations' and construction_segments_dict:
        series_items = list(construction_segments_dict.items())
        for i, data in enumerate(series_data_iterable):
            if nested_key in data:
                series_code, series_description = series_items[i]
                df = pd.DataFrame(data[nested_key])
                df['code'] = series_code
                df['description'] = series_description
                dataframes_list.append(df)
            else:
                print(f"No '{nested_key}' key found for series at index {i}.")
    else:
        for data in series_data_iterable:
            if nested_key in data:
                df = pd.DataFrame(data[nested_key])
                dataframes_list.append(df)
            else:
                print(f"No '{nested_key}' key found for one of the series data.")

    return dataframes_list


def write_dataframes_to_csv(dataframes_list, desktop_path, save_string):
    for i, df in enumerate(dataframes_list):
        filename = f"{save_string}_{i}.csv"
        file_path = os.path.join(desktop_path, filename)
        df.to_csv(file_path, index=False)
        print(f"Written to {file_path}")

