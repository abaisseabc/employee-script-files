from os import makedirs
import datetime


class CreateFiles:
    def __init__(self, todos_api: list, users_api: list):
        self.todos = todos_api
        self.users = users_api
        self.OUT_DIR = 'tasks'

    def _create_directory(self):
        try:
            makedirs(self.OUT_DIR, exist_ok=True)
        except OSError:
            raise OSError(f"Не удается создать каталог назначения {self.OUT_DIR}!")

    @staticmethod
    def _add_tasks_for_user(user, todo, total):
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

    @staticmethod
    def _create_template(user):
        now_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

        completed_task = list()
        outstanding_tasks = list()

        completed_task_template = str()
        outstanding_tasks_template = str()

        for task in user['tasks']:
            if task['completed'] is False:
                outstanding_tasks.append(task)
                outstanding_tasks_template += f"{task['title']} \n \n"
            else:
                completed_task.append(task)
                completed_task_template += f"{task['title']} \n \n"

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

    def _create_files_by_users(self, data: list):
        for user in data:
            with open(f"{self.OUT_DIR}/{user['username']}.txt", 'w') as f:
                template = self._create_template(user)
                f.write(template)

    def create(self):
        self._create_directory()
        data_for_file = self._search_task()
        self._create_files_by_users(data_for_file)
