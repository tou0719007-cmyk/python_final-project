import get_time     #导入模块
import task
class SystemManager:
    #定义类名,属性
    version = 1.0
    name ="任务管理系统"
    def __init__(self):
        self._task_list=[]
    #添加任务
    def add_task(self,):
        while True:
            try:
                #输入基本信息
                new_task= input("请输入任务的编号:")
                new_num=new_task
                new_title= input("请输入任务的标题:")
                new_priority = input("请输入任务的优先级(低/中/高):")
                new_deadline=get_time.get_datetime()       #命令有点长,放进get_time.py文件了
                new_status = input("请输入任务当前状态(未完成/已完成):")
                # 检查用户的输入是否规范,不规范则重新输入(while True循环)
                if (new_priority not in ["低", "中","高"]
                    or new_status not in ["未完成", "已完成"]):
                    print("输入错误,请重新输入")
                # 添加一个任务对象
                else:
                    new_task = task.Tasks(new_num, new_title, new_priority, new_deadline, new_status)
                    self._task_list.append(new_task)
                    break
            except Exception:
                print("输入错误,请重试")
    #输出所有的任务
    def view_tasks(self):
        for tasks in self._task_list:
            print(tasks)
     #更改任务状态为完成
    def complete_task(self):
        while True:
            try:
                target_task = input("请输入想更改的任务编号:")
                for tasks in self._task_list:     #遍历列表找到目标任务
                    if tasks.num == target_task:
                        tasks.change_status()
                        return
                print("该任务不存在")      #如果存在该任务,遍历列表时会触发return,没有则进入print语句
            except Exception:
                print("输入错误,请重新输入")
    #删除任务
    def delete_task(self):
        while True:
            try:
                target_task=input("请输入想删除的任务编号:")
                for tasks in self._task_list:      #遍历列表
                    if tasks.num==target_task:
                        self._task_list.remove(tasks)
                        print("删除成功")
                        return
                    print("该任务不存在,删除失败")
            except Exception:
                print("输入错误,请重新输入")

    def search_tasks(self):




