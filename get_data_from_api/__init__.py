import requests
import json


class DataApi:
    def __init__(self):
        self.todos = list()
        self.users = list()
        self.API_BASE = 'https://jsonplaceholder.typicode.com'

    def get_users(self):
        try:
            api_response = requests.get(f'{self.API_BASE}/users')
            if api_response.status_code != 200:
                print('Произошла ошибка!')
                print(api_response.status_code)
            else:
                data_users = api_response.text
                self.users = json.loads(data_users)
                return self.users
        except requests.exceptions.Timeout:
            print('Ошибка таймаута')
        except requests.exceptions.ConnectionError:
            print('Ошибка соединения')
        except:
            print('Не опознанная ошибка')

    def get_todos(self):
        try:
            api_response = requests.get(f'{self.API_BASE}/todos')
            if api_response.status_code != 200:
                print('Произошла ошибка!')
                print(api_response.status_code)
            else:
                data_todos = api_response.text
                self.todos = json.loads(data_todos)
                return self.todos
        except requests.exceptions.Timeout:
            print('Ошибка таймаута')
        except requests.exceptions.ConnectionError:
            print('Ошибка соединения')
        except:
            print('Не опознанная ошибка')
