import task

 # task.task_list.append(task.task_modle("ok","done","da","te")) 跨文件 调用操作 唯一列表 格式

def add_task():
    task_name = input("请输入任务名称：")
    task_status = input("请输入任务状态：")
    task_date = input("请输入任务日期：")
    new_task = task.task_modle(task_name, task_status, task_date)
    task.task_list.append(new_task)
    print("任务已添加！")
#无编号,仅作为测试使用

def view_task():
    print("目前无该功能")
def complete_task():
    print("目前无该功能")
def delete_task():
    print("目前无该功能")
def sreach_task():
    print("目前无该功能")
def statistics():
    print("目前无该功能")
