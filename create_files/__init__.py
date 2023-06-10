import os
import datetime
from os import makedirs
from os.path import getctime


class CreateFiles:
    def __init__(self, todos_api: list, users_api: list, folder: str):
        self.todos = todos_api
        self.users = users_api
        self.OUT_DIR = folder
        self.MAX_TASK_TITLE_LEN = 50

    @staticmethod
    def _add_tasks_for_user(user: dict, todo: dict, total: list) -> list:
        for task in total:
            if (
                    user['id'] == todo['userId'] and
                    task['id'] == user['id'] and
                    task['id'] == todo['userId']
            ):
                task['tasks'].append(todo)

        return total

    def _search_task(self):
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

    def _create_template(self, user: dict) -> str:
        now_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

        completed_task = list()
        outstanding_tasks = list()

        completed_task_template = str()
        outstanding_tasks_template = str()

        for task in user['tasks']:
            if task['completed'] is False:
                outstanding_tasks.append(task)
                if len(task['title']) <= self.MAX_TASK_TITLE_LEN:
                    outstanding_tasks_template += f"{task['title']} \n \n"
                else:
                    outstanding_tasks_template += f"{task['title'][:self.MAX_TASK_TITLE_LEN]} ... \n \n"
            else:
                completed_task.append(task)
                if len(task['title']) <= self.MAX_TASK_TITLE_LEN:
                    completed_task_template += f"{task['title']} \n \n"
                else:
                    completed_task_template += f"{task['title'][:self.MAX_TASK_TITLE_LEN]} ... \n \n"

        template = f"Отчет для {user['username']}. \n" \
                   f"\n" \
                   f"{user['name']} <{user['email']}> {now_time} \n" \
                   f"\n" \
                   f"Всего задач: {len(user['tasks'])} \n" \
                   f"\n" \
                   f"\n" \
                   f"\n" \
                   f"Завершённые задачи ({len(completed_task)}): \n \n" \
                   f"{completed_task_template} \n" \
                   f"\n" \
                   f"Оставшиеся задачи ({len(outstanding_tasks)}): \n \n" \
                   f"{outstanding_tasks_template}"

        return template

    def _write_file(self, user: dict):
        with open(f"{self.OUT_DIR}/{user['username']}.txt", 'w') as f:
            template = self._create_template(user)
            f.write(template)

    def _create_files_by_users(self, data: list):
        for user in data:
            if os.path.exists(f"{self.OUT_DIR}/{user['username']}.txt"):

                file_oldname = os.path.join(f"{self.OUT_DIR}/{user['username']}.txt")

                time_old_file = datetime.datetime.fromtimestamp(
                    getctime(f"{self.OUT_DIR}/{user['username']}.txt")).strftime('%Y-%m-%dT%H:%M')

                file_newname_newfile = os.path.join(f"{self.OUT_DIR}/old_{user['username']}_{time_old_file}.txt")

                os.rename(file_oldname, file_newname_newfile)

                self._write_file(user)
            else:
                self._write_file(user)

    def create(self):
        data_for_file = self._search_task()
        self._create_files_by_users(data_for_file)
