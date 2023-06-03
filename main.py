from get_data_from_api import DataApi

if __name__ == '__main__':
    todos = DataApi().get_todos()
    users = DataApi().get_users()
