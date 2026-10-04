class Tasks:   #定义类名和属性
    def __init__(self, num, title, priority, deadline, status):
        self.num=num
        self.title=title
        self.priority=priority
        self.deadline=deadline
        self._status=status    #属性名前加下划线表示该属性只能通过方法修改

    def __str__(self):    #规范后续列表的输出
        return f"[编号:{self.num}|标题:{self.title}|优先级:{self.priority}|截止日期:{self.deadline}|状态:{self._status}\n]"
    #加上repr避免输出地址
    def __repr__(self):
        return f"[编号:{self.num}|标题:{self.title}|优先级:{self.priority}|截止日期:{self.deadline}|状态:{self._status}\n]"
    #更改任务状态
    def change_status(self):
        while True:
            preloaded_status=input("请输入该任务的状态(未完成/已完成):")   #该变量用于储存状态
            if preloaded_status not in ["未完成","已完成"]:        #判断输入是否规范
                print("请输入正确的状态!")
                continue
            else:
                self._status=preloaded_status
                print("更改完成")
                return
