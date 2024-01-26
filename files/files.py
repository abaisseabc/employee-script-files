import os
import datetime
from os.path import getctime

from typing import Tuple, List, Dict

MAX_TASK_TITLE_LEN = 50


class Files:
    def __init__(self, todos_api: list, users_api: list, folder: str):
        self.todos = todos_api
        self.users = users_api
        self.OUT_DIR = folder

    @staticmethod
    def _add_tasks_for_user(user: dict, todo: dict, total: list) -> List[Dict]:
        """
        Вспомогательный метод для добавления задачи к пользователю в общем списке задач
        """
        for task in total:
            if (
                    user['id'] == todo['userId'] and
                    task['id'] == user['id'] and
                    task['id'] == todo['userId']
            ):
                task['tasks'].append(todo)
        return total

    def _search_task(self) -> List[Dict]:
        """
        Метод для поиска и организации задач для каждого пользователя
        """
        total_task_user = list()
        for user in self.users:
            if 'id' in user:
                total_task_user.append({
                    'id': user['id'],
                    'name': user['name'],
                    'username': user['username'],
                    'email': user['email'],
                    'tasks': []
                })
            for todo in self.todos:
                if 'userId' in todo:
                    total_task_user = self._add_tasks_for_user(user, todo, total_task_user)

        return total_task_user

    @staticmethod
    def _create_data_template(user: dict) -> Tuple[dict, dict]:
        """
        Метод для создания данных о завершенных
        и незавершенных задачах пользователя
        """
        completed_task = 0
        outstanding_tasks = 0

        completed_task_template = str()
        outstanding_tasks_template = str()

        for task in user['tasks']:
            if task['completed'] is False:
                outstanding_tasks = outstanding_tasks + 1
                if len(task['title']) <= MAX_TASK_TITLE_LEN:
                    outstanding_tasks_template += f"{task['title']} \n \n"
                else:
                    outstanding_tasks_template += f"{task['title'][:MAX_TASK_TITLE_LEN]} ... \n \n"
            else:
                completed_task = completed_task + 1
                if len(task['title']) <= MAX_TASK_TITLE_LEN:
                    completed_task_template += f"{task['title']} \n \n"
                else:
                    completed_task_template += f"{task['title'][:MAX_TASK_TITLE_LEN]} ... \n \n"

        completed = {
            'length': completed_task,
            'data': completed_task_template
        }

        outstanding = {
            'length': outstanding_tasks,
            'data': outstanding_tasks_template
        }

        return completed, outstanding

    def _create_template(self, user: dict) -> str:
        """
        Метод для создания шаблона отчета для пользователя
        """
        now_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        tasks = self._create_data_template(user)
        completed_task = tasks[0]
        outstanding_tasks = tasks[1]

        template = f"Отчет для {user['username']}. \n" \
                   f"\n" \
                   f"{user['name']} <{user['email']}> {now_time} \n" \
                   f"\n" \
                   f"Всего задач: {len(user['tasks'])} \n" \
                   f"\n" \
                   f"\n" \
                   f"\n" \
                   f"Завершённые задачи ({completed_task['length']}): \n \n" \
                   f"{completed_task['data']} \n" \
                   f"\n" \
                   f"Оставшиеся задачи ({outstanding_tasks['length']}): \n \n" \
                   f"{outstanding_tasks['data']}"

        return template

    def _write_file(self, user: dict) -> None:
        """
        Метод для записи отчета пользователя в файл
        """
        with open(f"{self.OUT_DIR}/{user['username']}.txt", 'w') as f:
            template = self._create_template(user)
            f.write(template)

    def _create_files_by_users(self, data: list) -> None:
        """
        Метод для создания файлов для каждого пользователя
        и обработки существующих файлов
        """
        for user in data:
            if os.path.exists(f"{self.OUT_DIR}/{user['username']}.txt"):
                file_old_name = os.path.join(f"{self.OUT_DIR}/{user['username']}.txt")

                time_old_file = datetime.datetime.fromtimestamp(
                    getctime(f"{self.OUT_DIR}/{user['username']}.txt")
                ).strftime('%Y-%m-%dT%H:%M')

                file_new_name_new_file = os.path.join(f"{self.OUT_DIR}/old_{user['username']}_{time_old_file}.txt")

                os.rename(file_old_name, file_new_name_new_file)

                self._write_file(user)
            else:
                self._write_file(user)

    def create(self) -> None:
        """
        Основной метод для создания отчетов для всех пользователей
        """
        data_for_file = self._search_task()
        self._create_files_by_users(data_for_file)
