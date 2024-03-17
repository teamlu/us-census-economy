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


def convert_to_dataframes(series_data_objects):
    dataframes_list = []
    for data in series_data_objects.values():
        if 'seriess' in data:
            df = pd.DataFrame(data['seriess'])
            dataframes_list.append(df)
        else:
            print(f"No 'seriess' key found for one of the categories.")
    return dataframes_list


def write_dataframes_to_csv(dataframes_list, desktop_path):
    for i, df in enumerate(dataframes_list):
        filename = f"category_dataframe_{i}.csv"
        file_path = os.path.join(desktop_path, filename)
        df.to_csv(file_path, index=False)
        print(f"Written to {file_path}")
