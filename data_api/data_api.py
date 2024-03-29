import requests
import json

API_BASE = 'https://jsonplaceholder.typicode.com'


class DataApi:
    def __init__(self, parameter: str):
        self.parameter = parameter

    def get(self) -> list:
        try:
            api_response = requests.get(f'{API_BASE}/{self.parameter}')
            if api_response.status_code != 200:
                print('Произошла ошибка!')
                print(api_response.status_code)
            else:
                query_result = api_response.text
                result = json.loads(query_result)
                return result
        except requests.exceptions.Timeout:
            print('Ошибка таймаута')
        except requests.exceptions.ConnectionError:
            print('Ошибка соединения')
        except:
            print('Не опознанная ошибка')
