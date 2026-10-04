import task
import storage
import task_manager
import report
import chart
import os


def show(): #菜单打印
    caidan='''
    ===== 命令行任务管理系统 =====
    1. 添加任务
    2. 查看任务
    3. 完成任务
    4. 删除任务
    5. 搜索/筛选任务
    6. 任务统计
    7. 导出 HTML 报告
    8. 保存任务
    0. 退出
    输入前面的序号
    '''
    print(caidan)

def clear_windows(): #清屏
    os.system('cls' if os.name == 'nt' else 'clear')

def end(): #结束程序
    print("感谢使用任务管理系统！") #有这句吗?
    return 0

while True:
    show()
    choice = input("请输入您的选择: ")
    if choice == '1':
        clear_windows()
        task_manager.add_task()
    elif choice == '2':
        clear_windows()
        task_manager.view_tasks()
    elif choice == '3':
        clear_windows()
        task_manager.complete_task()
    elif choice == '4':
        clear_windows()
        task_manager.delete_task()
    elif choice == '5':
        clear_windows()
        task_manager.search_tasks()
    elif choice == '6':
        clear_windows()
        task_manager.statistics()
    elif choice == '7':
        clear_windows()
        report.generate_report()
    elif choice == '8':
        clear_windows()
        storage.save_tasks()
    elif choice == '0':
        clear_windows()
        end()
        break
    else:
        clear_windows()
        print("无效的选择，请重新输入。")


