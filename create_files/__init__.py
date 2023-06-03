class CreateFiles:
    def __init__(self, todos_api: list, users_api: list):
        self.todos = todos_api
        self.users = users_api

    def create(self):
        print(self.todos)
        print(self.users)
