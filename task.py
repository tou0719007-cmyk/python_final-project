import storage

class task_modle:
    def __init__(self, name, description, due_date, completed):
        self.name = name
        self.description = description
        self.due_date = due_date
        self.completed = completed

task_list=[] #初始为空

task_list = storage.load_task_list() #从文件中加载任务列表

