from get_data_from_api import DataApi
from create_files import CreateFiles

if __name__ == '__main__':
    todos = DataApi().get_todos()
    users = DataApi().get_users()

    if todos and users:
        CreateFiles(todos, users).create()
    else:
        print('Данные не были получены')
