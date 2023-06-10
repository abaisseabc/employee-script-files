from get_data_from_api import DataApi
from create_files import CreateFiles
from os import makedirs

OUT_DIR = 'tasks'


def create_directory_tasks():
    try:
        makedirs(OUT_DIR, exist_ok=True)
    except OSError:
        raise OSError(f"Не удается создать каталог назначения {OUT_DIR}!")


def main():
    create_directory_tasks()

    todos = DataApi().get_todos()
    users = DataApi().get_users()

    if todos and users:
        CreateFiles(todos, users, OUT_DIR).create()
    else:
        print('Данные о пользователях и задачах не были получены')


if __name__ == '__main__':
    main()
