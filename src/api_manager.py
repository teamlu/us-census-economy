# api_manager.py

import requests

class EconomicDataAPI:

    BASE_URL = 'https://api.stlouisfed.org/fred/'


    def __init__(self, api_key):
        self.api_key = api_key
        

    def get_series_in_category(self, category_id, file_type='json', realtime_start=None, realtime_end=None, limit=1000, offset=0, order_by='series_id', sort_order='asc', filter_variable=None, filter_value=None, tag_names=None, exclude_tag_names=None):
        endpoint_url = f'category/series?category_id={category_id}&api_key={self.api_key}&file_type={file_type}&limit={limit}&offset={offset}&order_by={order_by}&sort_order={sort_order}'

        if realtime_start:
            endpoint_url += f'&realtime_start={realtime_start}'
        if realtime_end:
            endpoint_url += f'&realtime_end={realtime_end}'
        if filter_variable:
            endpoint_url += f'&filter_variable={filter_variable}'
        if filter_value:
            endpoint_url += f'&filter_value={filter_value}'
        if tag_names:
            endpoint_url += f'&tag_names={tag_names}'
        if exclude_tag_names:
            endpoint_url += f'&exclude_tag_names={exclude_tag_names}'

        response = requests.get(self.BASE_URL + endpoint_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
        
    def get_series_categories(self, series_id, file_type='json'):
        endpoint_url = f'series/categories?series_id={series_id}&api_key={self.api_key}&file_type={file_type}'

        response = requests.get(self.BASE_URL + endpoint_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        

    def get_economic_series(self, series_id, file_type='json', realtime_start=None, realtime_end=None):
        endpoint_url = f'series?series_id={series_id}&api_key={self.api_key}&file_type={file_type}'
        if realtime_start:
            endpoint_url += f'&realtime_start={realtime_start}'
        if realtime_end:
            endpoint_url += f'&realtime_end={realtime_end}'

        response = requests.get(self.BASE_URL + endpoint_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

        
    def get_category_children(self, category_id, file_type='json'):
        endpoint_url = f'category/children?category_id={category_id}&api_key={self.api_key}&file_type={file_type}'

        response = requests.get(self.BASE_URL + endpoint_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None    
    
    