from data_api.data_api import DataApi
from files.files import Files
from os import makedirs

OUT_DIR = 'tasks'


def create_directory_tasks():
    try:
        makedirs(OUT_DIR, exist_ok=True)
    except OSError:
        raise OSError(f"Не удается создать каталог назначения {OUT_DIR}!")


def main():
    create_directory_tasks()

    todos = DataApi('todos').get()
    users = DataApi('users').get()

    if todos and users:
        Files(todos, users, OUT_DIR).create()
    else:
        print('Данные о пользователях и задачах не были получены')


if __name__ == '__main__':
    main()
